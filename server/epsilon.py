import os, sys
DIR = "__EPSILON_PREFIX__/server"
sys.path.append(DIR)

import argparse
import hashlib
import yaml
import datetime
import time
import functools
import re
import io
from flask import Flask, g, redirect, abort, render_template, url_for as real_url_for, request, session, send_from_directory, send_file
from data import Contest, ScoreboardTeamProblem, Balloon
from models import db, Submission, SubmissionQueue, Balloon as BalloonModel


app = Flask(__name__)
app.secret_key = "V=7Km+XXkg:}>4dT0('cV>Rp1TG82QEjah+X'v;^w:)a']y)^%"

verdict_explanation =  {
    'QU': 'in queue',
    'AC': 'accepted',
    'PE': 'presentation error',
    'WA': 'wrong answer',
    'CE': 'compile time error',
    'RE': 'runtime error',
    'TL': 'time limit exceeded',
    'ML': 'memory limit exceeded',
    'OL': 'output limit exceeded',
    'SE': 'submission error',
    'RF': 'restricted function',
    'CJ': 'cannot judge',
}

# TODO: make this work for internal redirects
def url_for(path, **values):
    res = real_url_for(path, **values)
    if opts.prefix:
        return opts.prefix + res
    else:
        return res

def is_logged_in():
    return 'team' in session and session['team'] in contest.teams

def judge_is_logged_in():
    return 'judge' in session and session['judge'] in contest.judges

def get_team():
    if not is_logged_in(): return None
    return contest.teams.get(session['team'])

def get_judge():
    if not judge_is_logged_in(): return None
    return contest.judges.get(session['judge'])

def login_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated

def judge_only(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if not judge_is_logged_in():
            return redirect(url_for('judge_login', next=request.path))
        return f(*args, **kwargs)
    return decorated

@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: time.time() - g.request_start_time

@app.context_processor
def context_processor():

    solved = set()
    tried = set()
    team = get_team()
    judge = get_judge()

    if team:
        cur_time = contest.time_elapsed()
        subs = Submission.query.filter(Submission.submitted <= cur_time).filter_by(team=team.name).all()
        for sub in subs:
            if sub.verdict == 'AC':
                solved.add(sub.problem)
                tried.add(sub.problem)
            elif sub.verdict not in {'SE','RF','CJ','QU','CE'}:
                tried.add(sub.problem)

    return dict(
        contest=contest,
        phase=contest.get_current_phase(),
        team=team,
        judge=judge,
        solved=solved,
        tried=tried,
        problem=None,
        verdict_explanation=verdict_explanation,
        sorted=sorted,
        reversed=lambda x: list(reversed(x)),
        int=int,
        enumerate=enumerate,
        len=len,
        map=map,
        url_for=url_for,
    )

@app.template_filter('format_time')
def template_format_time(time):
    # return '%02d:%02d:%02d' % (int(time//60//60), int(time//60)%60, int(time)%60)
    return '%02d:%02d' % (int(time//60), int(time)%60)

@app.route('/scoreboard/', defaults={'opts':''})
@app.route('/scoreboard/<opts>/')
def view_scoreboard(opts):
    phase = contest.get_current_phase()
    if not phase.scoreboard_problems:
        abort(404)

    opts = { s.split('=', 1)[0]: ( s.split('=', 1)[1] if '=' in s else True ) for s in opts.split(',') }
    opts['groups'] = set(opts.get('groups', '+'.join(contest.groups.keys())).split('+'))

    cur_time = contest.time_elapsed()
    subs = Submission.query.filter(Submission.submitted <= cur_time).filter(Submission.problem.in_(phase.scoreboard_problems)).order_by(Submission.submitted).all()
    sb = { team: { problem: ScoreboardTeamProblem() for problem in phase.scoreboard_problems } for team, v in contest.teams.items() if len(v.groups & opts['groups']) > 0 }

    for sub in subs:
        if sub.problem not in phase.scoreboard_problems:
            continue

        if sub.team not in sb:
            continue

        cur = sb[sub.team][sub.problem]

        if (phase.frozen is not None and sub.submitted >= 60.0 * phase.frozen and (not is_logged_in() or get_team().name != sub.team)) or sub.verdict == 'QU':
            cur.submit_new()
        elif sub.verdict not in {'SE','RF','CJ','CE'}:
            cur.submit(sub.submitted, sub.verdict == 'AC')

    ssb = sorted(( -sum( sb[team][problem].is_solved() for problem in phase.scoreboard_problems ),
                   sum( sb[team][problem].time_penalty() for problem in phase.scoreboard_problems ),
                   team ) for team in sb.keys() )

    sb = [ (s[2], -s[0], s[1], sb[s[2]]) for s in ssb ]

    if opts.get('full', False):
        return render_template('scoreboard_full.html', scoreboard=sb)
    else:
        return render_template('scoreboard.html', scoreboard=sb)

@app.route('/submissions/')
@login_required
def list_submissions():
    team = get_team()
    cur_time = contest.time_elapsed()
    submissions = Submission.query.filter_by(team=team.name).filter(Submission.submitted <= cur_time).order_by(Submission.submitted).all()

    def format_verdict_classes(vs):
        vs = set(vs.split('+'))
        if vs <= {'QU'}: return 'info'
        if vs <= {'AC'}: return 'success'
        if vs <= {'SE','RF','CJ','CE'}: return 'warning'
        if vs <= {'PE','WA','RE','TL','ML','OL'}: return 'error'
        return ''

    label_class = {
        'QU': 'info',
        'AC': 'success',
        'PE': 'warning',
        'WA': 'important',
        'CE': 'warning',
        'RE': 'important',
        'TL': 'important',
        'ML': 'important',
        'OL': 'important',
        'SE': 'inverse',
        'RF': 'inverse',
        'CJ': 'inverse',
    }

    def label_class_for(v):
        return "label label-" + label_class.get(v, 'default')

    return render_template('submissions.html',
        submissions=reversed(submissions),
        format_verdict_classes=format_verdict_classes,
        label_class_for=label_class_for,
    )

@app.route('/submission/<int:sub_id>/')
@login_required
def view_submission(sub_id):
    team = get_team()
    sub = Submission.query.filter_by(id=sub_id).first()
    if not sub or sub.team != team.name: abort(404)
    return render_template('submission.html', submission=sub)

@app.route('/problem/<problem_id>/', methods={'GET', 'POST'})
def view_problem(problem_id):

    problem = contest.problems.get(problem_id)
    phase = contest.get_current_phase()
    if not problem: abort(404)
    if request.method == 'POST':

        if problem_id not in phase.submit_problems: abort(404)

        if not is_logged_in():
            return redirect(url_for('login', next=request.path))

        team = get_team()
        if ('language' in request.form and
            ('source_file' in request.files or 'source_code' in request.form) and
            request.form['language'] in contest.languages):

            if 'source_file' in request.files:
                code = request.files['source_file'].read().decode('utf-8')

            if 'source_file' not in request.files or not code:
                code = request.form['source_code']

            sub = Submission(
                team=team.name,
                problem=problem_id,
                language=request.form['language'],
                file=code,
                submitted=(datetime.datetime.now() - contest.start).total_seconds(),
            )

            team.last_used_language = request.form['language']

            db.session.add(sub)
            db.session.flush()
            db.session.add(SubmissionQueue(submission_id=sub.id))
            db.session.commit()
        else:
            abort(400)

        return redirect(url_for('list_submissions'))

    if problem_id not in phase.visible_problems: abort(404)
    return render_template('problem.html', problem=problem)

@app.route('/problem/<problem_id>/assets/<path:asset>')
def get_problem_asset(problem_id, asset):
    problem = contest.problems.get(problem_id)
    phase = contest.get_current_phase()
    if not problem or problem_id not in phase.visible_problems: abort(404)

    if not problem.assets: abort(404)
    return send_from_directory(problem.assets, asset)

@app.route('/login/', methods={'GET', 'POST'})
def login():
    goto = request.args.get('next', url_for('index'))
    registered = request.args.get('register', 'False') == 'True'
    team_name = ''
    bad_login = False
    if is_logged_in():
        return redirect(goto)
    if request.method == 'POST':
        # TODO: make sure 'team' and 'password' are in request.form
        team_name = request.form['team']
        password = request.form['password']
        if team_name in contest.teams and contest.teams[team_name].password == password:
            session['team'] = team_name
            return redirect(goto)
        else:
            session.pop('team', '')
            bad_login = True
    return render_template('login.html', team_name=team_name, bad_login=bad_login, registered=registered)

@app.route('/logout/')
def logout():
    session.pop('team', '')
    return redirect(url_for('index'))

def _register_team(name, password):
    global opts
    global contest

    with open(os.path.join(opts.contest, 'teams.yml'), 'r') as f:
        inp = f.read()

    with open(os.path.join(opts.contest, 'teams.yml'), 'w') as f:
        for line in inp.strip().split('\n'):
            f.write(line + '\n')
            if line.strip() == 'teams:':
                f.write('    "%s": {pass: "%s", location: unknown, groups:[all]}\n' % (name, password))

    contest = Contest.load(opts.contest)

@app.route('/register/', methods={'GET', 'POST'})
def register():
    global contest
    if not contest.register or is_logged_in(): abort(404)

    team_name = ''
    error = []

    if request.method == 'POST':
        # TODO: make sure 'team' and 'password' are in request.form
        team_name = request.form['team']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        rx = '^[-_A-Za-z0-9 ]{3,20}$'
        if not re.match(rx, team_name):
           error.append('Team name is illegal (it must match %s).' % rx)

        if team_name in contest.teams:
           error.append('Team name is already taken.')

        rx = '^[-_A-Za-z0-9 ]{5,20}$'
        if not re.match(rx, password):
           error.append('Password is illegal (it must match %s).' % rx)

        if password != confirm_password:
           error.append('Password confirmation was incorrect.')

        if not error:
            _register_team(team_name, password)
            return redirect(url_for('login', register='True'))

    return render_template('register.html', team_name=team_name, error=error)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/judge/')
@judge_only
def judge_index():
    return render_template('judge/index.html')

@app.route('/judge/login/', methods={'GET', 'POST'})
def judge_login():
    goto = request.args.get('next', url_for('judge_index'))
    judge_name = ''
    bad_login = False
    if judge_is_logged_in():
        return redirect(goto)
    if request.method == 'POST':
        # TODO: make sure 'team' and 'password' are in request.form
        judge_name = request.form['judge']
        password = request.form['password']
        if judge_name in contest.judges and contest.judges[judge_name].password == password:
            session['judge'] = judge_name
            return redirect(goto)
        else:
            session.pop('judge', '')
            bad_login = True
    return render_template('judge/login.html', judge_name=judge_name, bad_login=bad_login)

@app.route('/judge/logout/')
@judge_only
def judge_logout():
    session.pop('judge', '')
    return redirect(url_for('judge_login'))

@app.route('/judge/reload/')
@judge_only
def judge_reload():
    global contest
    contest = Contest.load(opts.contest)
    return redirect(url_for('judge_index'))

@app.route('/judge/scoreboard/', defaults={'opts':''})
@app.route('/judge/scoreboard/<opts>/')
def judge_view_scoreboard(opts):
    phase = contest.get_current_phase()
    if not phase.scoreboard_problems:
        abort(404)

    opts = { s.split('=', 1)[0]: ( s.split('=', 1)[1] if '=' in s else True ) for s in opts.split(',') }
    opts['groups'] = set(opts.get('groups', '+'.join(contest.groups.keys())).split('+'))

    cur_time = contest.time_elapsed()
    subs = Submission.query.filter(Submission.submitted <= cur_time).filter(Submission.problem.in_(phase.scoreboard_problems)).order_by(Submission.submitted).all()
    sb = { team: { problem: ScoreboardTeamProblem() for problem in phase.scoreboard_problems } for team, v in contest.teams.items() if len(v.groups & opts['groups']) > 0 }

    for sub in subs:
        if sub.problem not in phase.scoreboard_problems:
            continue

        if sub.team not in sb:
            continue

        cur = sb[sub.team][sub.problem]

        if sub.verdict == 'QU':
            cur.submit_new()
        elif sub.verdict not in {'SE','RF','CJ','CE'}:
            cur.submit(sub.submitted, sub.verdict == 'AC')

    ssb = sorted(( -sum( sb[team][problem].is_solved() for problem in phase.scoreboard_problems ),
                   sum( sb[team][problem].time_penalty() for problem in phase.scoreboard_problems ),
                   team ) for team in sb.keys() )

    sb = [ (s[2], -s[0], s[1], sb[s[2]]) for s in ssb ]

    return render_template('judge/scoreboard.html', scoreboard=sb)

@app.route('/judge/submissions/', defaults={'team_name':None})
@app.route('/judge/submissions/<team_name>/')
@judge_only
def judge_list_submissions(team_name):
    cur_time = contest.time_elapsed()
    submissions = Submission.query
    if team_name is not None:
        submissions = submissions.filter_by(team=team_name)

    submissions = submissions.filter(Submission.submitted <= cur_time).order_by(Submission.submitted).all()

    def format_verdict_classes(vs):
        vs = set(vs.split('+'))
        if vs <= {'QU'}: return 'info'
        if vs <= {'AC'}: return 'success'
        if vs <= {'SE','RF','CJ','CE'}: return 'warning'
        if vs <= {'PE','WA','RE','TL','ML','OL'}: return 'error'
        return ''

    label_class = {
        'QU': 'info',
        'AC': 'success',
        'PE': 'warning',
        'WA': 'important',
        'CE': 'warning',
        'RE': 'important',
        'TL': 'important',
        'ML': 'important',
        'OL': 'important',
        'SE': 'inverse',
        'RF': 'inverse',
        'CJ': 'inverse',
    }

    def label_class_for(v):
        return "label label-" + label_class.get(v, 'default')

    return render_template('judge/submissions.html',
        submissions=reversed(submissions),
        format_verdict_classes=format_verdict_classes,
        label_class_for=label_class_for,
    )

@app.route('/judge/submission/<int:sub_id>/', methods={'GET', 'POST'})
@judge_only
def judge_view_submission(sub_id):
    sub = Submission.query.filter_by(id=sub_id).first()
    if not sub: abort(404)

    if request.method == 'POST':
        if 'verdict' in request.form and 'judge_response' in request.form:
            v = request.form['verdict'].split('+')
            if not (len(v) == len(set(v)) and set(v) <= set(verdict_explanation.keys())):
                abort(400)

            sub.verdict = request.form['verdict']
            sub.judge_response = request.form['judge_response']

            if sub.verdict == 'QU':
                qsub = SubmissionQueue.query.filter_by(submission_id=sub.id).first()
                if qsub:
                    qsub.last_announce = None
                else:
                    db.session.add(SubmissionQueue(sub.id))

            db.session.commit()
            return redirect(url_for('judge_view_submission', sub_id=sub_id))
        else:
            abort(400)

    return render_template('judge/submission.html', submission=sub)

@app.route('/judge/teams/')
@judge_only
def judge_list_teams():
    return render_template('judge/teams.html',
            teams=sorted(contest.teams.values(), key=lambda team: team.title)
        )

@app.route('/judge/balloons/', defaults={'id':None})
@app.route('/judge/balloons/deliver/<int:id>/')
@judge_only
def judge_balloons(id):
    if id is not None:
        balloon = BalloonModel.query.filter_by(balloon_id=id).first()
        if balloon:
            balloon.delivered = True
            db.session.commit()
        return redirect(url_for('judge_balloons'))

    submissions = { sub.id: sub for sub in Submission.query.all() }
    dballoons = BalloonModel.query.all()
    balloons = []
    for balloon in dballoons:
        sub = submissions[balloon.submission_id]
        team = contest.teams[sub.team]
        problem = contest.problems[sub.problem]
        balloons.append(Balloon(balloon.balloon_id, sub, team, problem, balloon.delivered))

    return render_template('judge/balloons.html',
            balloons=sorted(balloons, key=lambda balloon: balloon.submission.submitted)
        )

@app.route('/judge/resolver/', defaults={'no':None})
@app.route('/judge/resolver/generate/<int:no>/')
@judge_only
def judge_resolver(no):
    if no is not None:
        # out = io.StringIO()
        out = io.BytesIO()

        out.write(('''<?xml version="1.0" encoding="UTF-8"?>
<contest>
    <info>
        <length>%(duration)s</length>
        <penalty>20</penalty>
        <started>True</started>
        <title>%(title)s</title>
    </info>
''' % {
        'duration': '%02d:%02d:%02d' % (contest.duration // 60 // 60, (contest.duration // 60) % 60, contest.duration % 60),
            'title': contest.title,
        }).encode('utf-8'))

        teams = {}
        problems = {}

        for name, team in contest.teams.items():
            teams[name] = len(teams) + 1

        for name in contest.phases[-1][1].scoreboard_problems:
            problems[name] = len(problems) + 1

        for name, id in problems.items():
            out.write(('''
    <problem>
        <id>%(id)d</id>
        <name>%(name)s</name>
    </problem>''' % { 'id': id, 'name': name }).encode('utf-8'))

        for name, id in teams.items():
            out.write(('''
    <team>
        <id>%(id)d</id>
        <name>%(name)s</name>
    </team>''' % { 'id': id, 'name': name }).encode('utf-8'))

        subs = Submission.query.filter(Submission.verdict != 'QU').all()
        for no, sub in enumerate(sorted(subs, key=lambda sub: sub.submitted)):
            out.write(('''
    <run>
        <id>%(no)d</id>
        <judged>False</judged>
        <problem>%(problem_id)d</problem>
        <status>fresh</status>
        <team>%(team_id)d</team>
        <time>%(time)f</time>
    </run>
    <run>
        <id>%(no)d</id>
        <judged>True</judged>
        <penalty>%(penalty)s</penalty>
        <problem>%(problem_id)d</problem>
        <result>%(verdict)s</result>
        <solved>%(solved)s</solved>
        <status>done</status>
        <team>%(team_id)d</team>
        <time>%(time)f</time>
    </run>
''' % {
                'no': no + 1,
                'penalty': 'True' if set(sub.verdict.split('+')) <= {'RE','TL','ML','WA','PE'} else 'False',
                'problem_id': problems[sub.problem],
                'verdict': sub.verdict,
                'solved': 'True' if sub.verdict == 'AC' else 'False',
                'team_id': teams[sub.team],
                'time': sub.submitted,
            }).encode('utf-8'))

        out.write(('''
</contest>
''').encode('utf-8'))

        out.seek(0)
        return send_file(out,

                as_attachment=True,
                mimetype='application/xml')

    return render_template('judge/resolver.html')


def main(argv):
    global opts, contest, conn
    parser = argparse.ArgumentParser(description='A minimalistic programming contest environment.')
    parser.add_argument('contest', help='the contest directory')
    parser.add_argument('-p', '--port', default=31415, type=int, help='the port to listen on')
    parser.add_argument('-H', '--host', default='', help='the host to listen on')
    parser.add_argument('-d', '--debug', default=False, action='store_true', help='run in debug mode')
    parser.add_argument('--prefix', default=None, help='run under prefix')
    parser.add_argument('--droptables', default=False, action='store_true', help='drop database tables and exit')
    opts = parser.parse_args(argv)
    contest = Contest.load(opts.contest)
    app.config['SQLALCHEMY_DATABASE_URI'] = contest.db

    for table in db.metadata.tables.values():
        table.name = '%s_%s' % (contest.id, table.name)

    db.init_app(app)

    if opts.droptables:
        print('You are about to drop the database tables for contest %s!!!' % contest.id)
        if input('Are you sure you want to continue? (y/N) ').lower() == 'y':
            db.drop_all(app=app)

        return 0

    db.create_all(app=app)
    app.run(host=opts.host, port=opts.port, debug=opts.debug)

if __name__ == '__main__':
    main(sys.argv[1:])

