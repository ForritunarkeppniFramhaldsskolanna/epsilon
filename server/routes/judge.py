import io
import json
import datetime
from flask import redirect, abort, render_template, request, session, send_file, Blueprint, current_app as app
from server.data import Contest, ScoreboardTeamProblem, Balloon, verdict_explanation
from lib.models import Submission, SubmissionQueue, Balloon as BalloonModel
from server.util import judge_only, judge_is_logged_in, url_for

judge = Blueprint("judge", __name__, template_folder="../templates")

# judge.context_processor(context_processor)


@judge.route('/')
@judge_only
def index():
    return render_template('judge/index.html')


@judge.route('/login/', methods={'GET', 'POST'})
def login():
    goto = request.args.get('next', url_for('judge.index'))
    judge_name = ''
    bad_login = False
    if judge_is_logged_in():
        return redirect(goto)
    if request.method == 'POST':
        # TODO: make sure 'team' and 'password' are in request.form
        judge_name = request.form['judge']
        password = request.form['password']
        if judge_name in app.contest.judges and app.contest.judges[judge_name].password == password:
            session['judge'] = judge_name
            return redirect(goto)
        else:
            session.pop('judge', '')
            bad_login = True
    return render_template('judge/login.html', judge_name=judge_name, bad_login=bad_login)


@judge.route('/logout/')
@judge_only
def logout():
    session.pop('judge', '')
    return redirect(url_for('judge.login'))


@judge.route('/reload/')
@judge_only
def reload():
    app.contest = Contest.load(app.opts.contest)
    return redirect(url_for('judge.index'))


@judge.route('/scoreboard/', defaults={'opts': ''})
@judge.route('/scoreboard/<opts>/')
def view_scoreboard(opts):
    phase = app.contest.get_current_phase()
    if not phase.scoreboard_problems:
        abort(404)

    opts = {s.split('=', 1)[0]: (s.split('=', 1)[1] if '=' in s else True) for s in opts.split(',')}
    opts['groups'] = set(opts.get('groups', '+'.join(app.contest.groups.keys())).split('+'))

    cur_time = datetime.datetime.now()
    subs = Submission.query.filter(Submission.submitted <= cur_time).filter(Submission.problem.in_(phase.scoreboard_problems)).order_by(Submission.submitted).all()
    sb = {team: {problem: ScoreboardTeamProblem() for problem in phase.scoreboard_problems} for team, v in app.contest.teams.items() if len(v.groups & opts['groups']) > 0}

    for sub in subs:
        if sub.problem not in phase.scoreboard_problems:
            continue

        if sub.team not in sb:
            continue

        cur = sb[sub.team][sub.problem]

        if sub.verdict == 'QU':
            cur.submit_new()
        elif sub.verdict not in {'SE', 'RF', 'CJ', 'CE'}:
            cur.submit((sub.submitted - app.contest.start).total_seconds(), sub.verdict == 'AC')

    ssb = sorted((-sum(sb[team][problem].is_solved() for problem in phase.scoreboard_problems),
                  sum(sb[team][problem].time_penalty() for problem in phase.scoreboard_problems),
                  team) for team in sb.keys())

    sb = [(s[2], -s[0], s[1], sb[s[2]]) for s in ssb]

    return render_template('judge/scoreboard.html', scoreboard=sb)


@judge.route('/submissions/', defaults={'team_name': None})
@judge.route('/submissions/<team_name>/')
@judge_only
def list_submissions(team_name):
    cur_time = datetime.datetime.now()
    submissions = Submission.query
    if team_name is not None:
        submissions = submissions.filter_by(team=team_name)

    submissions = submissions.filter(Submission.submitted <= cur_time).order_by(Submission.submitted).all()

    def format_verdict_classes(vs):
        vs = set(vs.split('+'))
        if vs <= {'QU'}:
            return 'info'
        if vs <= {'AC'}:
            return 'success'
        if vs <= {'SE', 'RF', 'CJ', 'CE'}:
            return 'warning'
        if vs <= {'PE', 'WA', 'RE', 'TL', 'ML', 'OL'}:
            return 'danger'
        return ''

    label_class = {
        'QU': 'info',
        'AC': 'success',
        'PE': 'warning',
        'WA': 'danger',
        'CE': 'warning',
        'RE': 'danger',
        'TL': 'danger',
        'ML': 'danger',
        'OL': 'danger',
        'SE': 'default',
        'RF': 'default',
        'CJ': 'default',
    }

    def label_class_for(v):
        return "label label-" + label_class.get(v, 'default')

    return render_template('judge/submissions.html',
                           submissions=reversed(submissions),
                           format_verdict_classes=format_verdict_classes,
                           label_class_for=label_class_for,
                           )


@judge.route('/submission/<int:sub_id>/', methods={'GET', 'POST'})
@judge_only
def view_submission(sub_id):
    sub = Submission.query.filter_by(id=sub_id).first()
    if not sub:
        abort(404)

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
                    qsub.dequeued_at = None
                else:
                    app.db.session.add(SubmissionQueue(sub.id))

            app.db.session.commit()
            return redirect(url_for('judge.view_submission', sub_id=sub_id))
        else:
            abort(400)

    return render_template('judge/submission.html', submission=sub)


@judge.route('/teams/')
@judge_only
def list_teams():
    return render_template('judge/teams.html',
                           teams=sorted(app.contest.teams.values(), key=lambda team: team.title)
                           )


@judge.route('/balloons/', defaults={'id': None})
@judge.route('/balloons/deliver/<int:id>/')
@judge_only
def balloons(id):
    if id is not None:
        balloon = BalloonModel.query.filter_by(balloon_id=id).first()
        if balloon:
            balloon.delivered = True
            app.db.session.commit()
        return redirect(url_for('judge.balloons'))

    submissions = {sub.id: sub for sub in Submission.query.all()}
    dballoons = BalloonModel.query.all()
    balloons = []
    for balloon in dballoons:
        sub = submissions[balloon.submission_id]
        team = app.contest.teams[sub.team]
        problem = app.contest.problems[sub.problem]
        balloons.append(Balloon(balloon.balloon_id, sub, team, problem, balloon.delivered))

    return render_template('judge/balloons.html',
                           balloons=sorted(balloons, key=lambda balloon: balloon.submission.submitted)
                           )


@judge.route('/resolver/')
@judge_only
def resolver():
    return render_template('judge/resolver.html')


@judge.route('/export/', defaults={'no': None})
@judge.route('/export/generate/<int:no>/')
@judge_only
def export(no):
    if no is not None:

        if no == 1:
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
                'duration': '%02d:%02d:%02d' % (app.contest.duration // 60, app.contest.duration % 60, 0),
                'title': app.contest.title,
            }).encode('utf-8'))

            teams = {}
            problems = {}

            for name, team in app.contest.teams.items():
                teams[name] = len(teams) + 1

            for name in app.contest.phases[-1][1].scoreboard_problems:
                problems[name] = len(problems) + 1

            for name, id in problems.items():
                out.write(('''
        <problem>
            <id>%(id)d</id>
            <name>%(name)s</name>
        </problem>''' % {'id': id, 'name': name}).encode('utf-8'))

            for name, id in teams.items():
                out.write(('''
        <team>
            <id>%(id)d</id>
            <name>%(name)s</name>
        </team>''' % {'id': id, 'name': app.contest.teams[name].title}).encode('utf-8'))

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
                    'penalty': 'True' if set(sub.verdict.split('+')) <= {'RE', 'TL', 'ML', 'WA', 'PE'} else 'False',
                    'problem_id': problems[sub.problem],
                    'verdict': sub.verdict,
                    'solved': 'True' if sub.verdict == 'AC' else 'False',
                    'team_id': teams[sub.team],
                    'time': (sub.submitted - app.contest.start).total_seconds(),
                }).encode('utf-8'))

            out.write(('''
    </contest>
    ''').encode('utf-8'))

            out.seek(0)
            return send_file(out,
                             attachment_filename=app.contest.id + '_resolver.xml',
                             as_attachment=True,
                             mimetype='application/xml')

        elif no == 3:
            res = {}
            res['info'] = {
                'length': '%02d:%02d:%02d' % (app.contest.duration // 60, app.contest.duration % 60, 0),
                'penalty': 20,
                'started': True,
                'title': app.contest.title,
            }

            teams = {}
            problems = {}

            for name, team in app.contest.teams.items():
                teams[name] = len(teams) + 1

            for name in app.contest.phases[-1][1].scoreboard_problems:
                problems[name] = len(problems) + 1

            res['problems'] = []
            for name, id in sorted(problems.items(), key=lambda x: x[1]):
                res['problems'].append(
                    {
                        'id': id,
                        'name': name,
                    }
                )

            res['teams'] = []
            for name, id in teams.items():
                res['teams'].append(
                    {
                        'id': id,
                        'name': app.contest.teams[name].title,
                    }
                )

            subs = Submission.query.filter(Submission.verdict != 'QU').all()
            res['runs'] = []
            for no, sub in enumerate(sorted(subs, key=lambda sub: sub.submitted)):
                res['runs'].append(
                    {
                        'no': no + 1,
                        'penalty': 'True' if set(sub.verdict.split('+')) <= {'RE', 'TL', 'ML', 'WA', 'PE'} else 'False',
                        'problem_id': problems[sub.problem],
                        'verdict': sub.verdict,
                        'solved': 'True' if sub.verdict == 'AC' else 'False',
                        'team_id': teams[sub.team],
                        'time': sub.submitted,
                    }
                )

            out = io.BytesIO()
            out.write(json.dumps(res).encode('utf-8'))

            out.seek(0)
            return send_file(out,
                             attachment_filename=app.contest.id + '_resolver.json',
                             as_attachment=True,
                             mimetype='application/json')

    return render_template('judge/export.html')
