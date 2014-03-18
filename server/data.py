import os
import yaml
import datetime
import markdown
import mdx_mathjax
from os.path import join as pjoin

processor = markdown.Markdown(extensions=['mathjax'])

def load(path):
    with open(path) as f:
        return yaml.load(f)

def read(path):
    try:
        with open(path) as f:
            return f.read()
    except:
        return None

class Language:
    def __init__(self, name, filename, compile, execute, highlight, template):
        self.name = name
        self.filename = filename
        self.compile = compile
        self.execute = execute
        self.highlight = highlight
        self.template = template

    @staticmethod
    def load_all(path):
        langs = []
        for name, lang in load(pjoin(path, 'languages.yml')).items():

            langs.append(Language(
                name=name,
                filename=lang['filename'],
                compile=lang.get('compile'),
                execute=lang['execute'],
                highlight=lang['highlight'],
                template=lang.get('template', '')))
        return langs

class Team:
    def __init__(self, name, title, password, location, groups):
        self.name = name
        self.title = title
        self.password = password
        self.location = location
        self.groups = groups
        self.last_used_language = None

    @staticmethod
    def load_all(path):
        teams = []
        data = load(pjoin(path, 'teams.yml'))
        groups = data['groups']

        for name, d in data['teams'].items():
            teams.append(Team(
                name=name,
                title=d.get('title', name),
                password=d['pass'],
                location=d.get('location', 'unknown'),
                groups=set(d.get('groups', [])),
            ))

        return teams, groups

class Judge:
    def __init__(self, name, password):
        self.name = name
        self.password = password

    @staticmethod
    def load_all(path):
        judges = []
        data = load(pjoin(path, 'judges.yml'))

        for name, d in data.items():
            judges.append(Judge(
                name=name,
                password=d['pass'],
            ))

        return judges

class Example:
    def __init__(self, input, output, explanation=None, display='normal'):
        self.input = input
        self.output = output
        self.explanation = explanation
        self.display = display

        if self.explanation is not None:
            self.explanation = processor.convert(self.explanation)

class Problem:
    def __init__(self, id, title, statement, examples, assets):
        self.id = id
        self.title = title
        self.statement = statement
        self.examples = examples
        self.assets = assets

    def __repr__(self):
        return '<Problem %s>' % repr(self.title)

    @staticmethod
    def load(path, id):
        path = os.path.abspath(path)

        problem = load(path)
        md = os.path.splitext(path)[0] + '.md'
        if not os.path.isfile(md):
            md = pjoin(os.path.dirname(path), 'statement.md')

        with open(md, encoding='utf-8') as f:
            statement = f.read()

        statement = processor.convert(statement)

        if os.path.isdir(pjoin(os.path.dirname(path), 'assets')):
            assets = pjoin(os.path.dirname(path), 'assets')
        elif os.path.isdir(pjoin(path, 'assets')):
            assets = pjoin(path, 'assets')
        else:
            assets = None

        return Problem(
            # id=os.path.splitext(os.path.basename(path))[0],
            id=id,
            title=problem['title'],
            # statement=problem['statement'],
            statement=statement,
            examples=[
                Example(
                    input=x.get('input', ''),
                    output=x.get('output', ''),
                    explanation=x.get('explanation'),
                    display=x.get('display','normal')
                ) for x in problem.get('examples', [])
            ],
            assets=assets
        )

    @staticmethod
    def load_all(path):
        problems = []
        problem_dir = pjoin(path, 'problems')
        for p in os.listdir(problem_dir):
            if p.endswith('.yml'):
                problems.append(Problem.load(pjoin(problem_dir, p), os.path.splitext(p)[0]))
            elif os.path.isdir(pjoin(problem_dir, p)) and os.path.isfile(pjoin(problem_dir, p, 'problem.yml')):
                problems.append(Problem.load(pjoin(problem_dir, p, 'problem.yml'), p))
        return problems

class Phase:
    def __init__(self, contest, start, status, countdown, visible_problems, submit_problems, scoreboard_problems, problem_list, frozen):
        self.contest = contest
        self.start = start
        self.status = status
        self.countdown = countdown
        self.visible_problems = visible_problems
        self.submit_problems = submit_problems
        self.scoreboard_problems = scoreboard_problems
        self.problem_list = problem_list
        self.frozen = frozen

    def current_countdown(self):
        if self.countdown is None: return None
        return 60.0 * self.countdown - (self.contest.time_elapsed() - 60.0 * self.start)

    def load(contest, start, d):

        visible_problems = set()
        submit_problems = set()
        scoreboard_problems = []
        problem_list = []

        for problem in d.get('problems', []):

            if type(problem) is str:
                problem_list.append(('text', problem))
            else:
                assert len(problem) == 1

                for k, v in problem.items():
                    pid = k
                    opts = v

                if 'visible' in opts:
                    visible_problems.add(pid)
                    problem_list.append(('problem', pid))

                if 'submit' in opts: submit_problems.add(pid)
                if 'scoreboard' in opts: scoreboard_problems.append(pid)

        return Phase(
            contest=contest,
            start=start,
            status=d.get('status', None),
            countdown=d.get('countdown', None),
            visible_problems=visible_problems,
            submit_problems=submit_problems,
            scoreboard_problems=scoreboard_problems,
            problem_list=problem_list,
            frozen=d.get('frozen', None),
        )

class Contest:
    BEFORE_START = 0
    RUNNING = 1
    FINISHED = 2

    def __init__(self, id, title, db, start, duration, teams, problems, languages, phases, groups, judges, register=False):
        self.id = id
        self.title = title
        self.db = db
        self.start = start
        self.duration = duration
        self.teams = teams
        self.problems = problems
        self.languages = languages
        self.phases = phases
        self.groups = groups
        self.register = register
        self.judges = judges

    def time_elapsed(self):
        return (datetime.datetime.now() - self.start).total_seconds()

    def time_remaining(self):
        return self.time_total() - self.time_elapsed()

    def time_total(self):
        return 60.0 * self.duration

    def time_to_start(self):
        return (self.start - datetime.datetime.now()).total_seconds()

    def status(self):
        if self.time_remaining() < 0: return Contest.FINISHED
        if self.time_elapsed() >= 0: return Contest.RUNNING
        return Contest.BEFORE_START

    def get_current_phase(self):
        now = self.time_elapsed()
        res = Phase.load(self, None, {})
        for k, v in self.phases:
            if now < 60.0 * k:
                break
            res = v
        return res

    @staticmethod
    def load(path):
        contest = load(pjoin(path, 'contest.yml'))
        teams, groups = Team.load_all(path)
        judges = Judge.load_all(path)
        res = Contest(
            id=contest['id'],
            title=contest['title'],
            db=contest['db'],
            start=contest['start'],
            duration=contest['duration'],
            teams={ team.name: team for team in teams },
            groups=groups,
            problems={ problem.id: problem for problem in Problem.load_all(path) },
            languages={ lang.name: lang for lang in Language.load_all(os.path.join('__EPSILON_PREFIX__', 'config')) },
            phases=None,
            judges={ judge.name: judge for judge in judges },
            register=contest.get('register', False),
        )

        res.phases = [ (k, Phase.load(res, k, v)) for k,v in sorted(contest['phases'].items()) ]
        return res

class ScoreboardTeamProblem:
    def __init__(self):
        self.solved_at = None
        self.try_count = 0
        self.new_submissions = 0

    def submit(self, at, solved):
        if self.solved_at is None:
            if solved:
                self.solved_at = at
            else:
                self.try_count += 1

    def submit_new(self):
        if self.solved_at is None:
            self.new_submissions += 1

    def is_solved(self):
        return self.solved_at is not None

    def time_penalty(self):
        if not self.is_solved(): return 0
        return self.solved_at + self.try_count * 20.0 * 60.0

class Balloon:
    def __init__(self, id, submission, team, problem, delivered):
        self.id = id
        self.submission = submission
        self.team = team
        self.problem = problem
        self.delivered = delivered

