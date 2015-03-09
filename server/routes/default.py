import re
import os
import datetime
import lib.text as text
from flask import redirect, abort, render_template, request, session, send_from_directory, Blueprint, current_app as app
from server.data import ScoreboardTeamProblem, Contest
from lib.models import Submission, SubmissionQueue
from server.util import url_for, get_team, is_logged_in, login_required

default = Blueprint("default", __name__, template_folder="../templates")

# default.context_processor(context_processor)


@default.route('/scoreboard/', defaults={'opts': ''})
@default.route('/scoreboard/<opts>/')
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

        if (phase.frozen is not None and sub.submitted >= app.contest.second_format(60.0 * phase.frozen) and (not is_logged_in() or get_team().name != sub.team)) or sub.verdict == 'QU':
            cur.submit_new()
        elif sub.verdict not in {'SE', 'RF', 'CJ', 'CE'}:
            cur.submit((sub.submitted - app.contest.start).total_seconds(), sub.verdict == 'AC')

    ssb = sorted((-sum(sb[team][problem].is_solved() for problem in phase.scoreboard_problems),
                  sum(sb[team][problem].time_penalty() for problem in phase.scoreboard_problems),
                  team) for team in sb.keys())

    sb = [(s[2], -s[0], s[1], sb[s[2]]) for s in ssb]

    if opts.get('full', False):
        return render_template('scoreboard_full.html', scoreboard=sb)
    else:
        return render_template('scoreboard.html', scoreboard=sb)


@default.route('/submissions/')
@login_required
def list_submissions():
    team = get_team()
    cur_time = datetime.datetime.now()
    submissions = Submission.query.filter_by(team=team.name).filter(Submission.submitted <= cur_time).order_by(Submission.submitted).all()

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
        'SE': 'inverse',
        'RF': 'inverse',
        'CJ': 'inverse',
    }

    def label_class_for(v):
        return "label label-" + label_class.get(v, 'default')

    return render_template('submissions.html',
                           submissions=reversed(submissions),
                           format_verdict_classes=format_verdict_classes,
                           label_class_for=label_class_for
                           )


@default.route('/submission/<int:sub_id>/')
@login_required
def view_submission(sub_id):
    team = get_team()
    sub = Submission.query.filter_by(id=sub_id).first()
    if not sub or sub.team != team.name:
        abort(404)
    return render_template('submission.html', submission=sub)


@default.route('/problem/<problem_id>/', methods={'GET', 'POST'})
def view_problem(problem_id):

    problem = app.contest.problems.get(problem_id)
    phase = app.contest.get_current_phase()
    if not problem:
        abort(404)
    if request.method == 'POST':

        if problem_id not in phase.submit_problems:
            abort(404)

        if not is_logged_in():
            return redirect(url_for('default.login', next=request.path))

        team = get_team()
        if (
                'language' in request.form and
                ('source_file' in request.files or 'source_code' in request.form) and
                request.form['language'] in app.contest.languages):

            if 'source_file' in request.files:
                code = request.files['source_file'].read()
                try:
                    code = code.decode('utf-8')
                except UnicodeDecodeError:
                    code = text.bytes2unicode(code)

            if 'source_file' not in request.files or not code:
                code = request.form['source_code']

            sub = Submission(
                team=team.name,
                problem=problem_id,
                language=request.form['language'],
                file=code,
                submitted=datetime.datetime.now()
            )

            team.last_used_language = request.form['language']

            app.db.session.add(sub)
            app.db.session.flush()
            app.db.session.add(SubmissionQueue(submission_id=sub.id))
            app.db.session.commit()
        else:
            abort(400)

        return redirect(url_for('default.list_submissions'))

    if problem_id not in phase.visible_problems:
        abort(404)
    return render_template('problem.html', problem=problem)


@default.route('/problem/<problem_id>/assets/<path:asset>')
def get_problem_asset(problem_id, asset):
    problem = app.contest.problems.get(problem_id)
    phase = app.contest.get_current_phase()
    if not problem or problem_id not in phase.visible_problems:
        abort(404)

    if not problem.assets:
        abort(404)
    return send_from_directory(problem.assets, asset)


@default.route('/login/', methods={'GET', 'POST'})
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
        if team_name in app.contest.teams and app.contest.teams[team_name].password == password:
            session['team'] = team_name
            return redirect(goto)
        else:
            session.pop('team', '')
            bad_login = True
    return render_template('login.html', team_name=team_name, bad_login=bad_login, registered=registered)


@default.route('/logout/')
def logout():
    session.pop('team', '')
    return redirect(url_for('index'))


def _register_team(name, password):
    global opts
    global contest

    with open(os.path.join(app.opts.contest, 'teams.yml'), 'r') as f:
        inp = f.read()

    with open(os.path.join(app.opts.contest, 'teams.yml'), 'w') as f:
        for line in inp.strip().split('\n'):
            f.write(line + '\n')
            if line.strip() == 'teams:':
                f.write('    "%s": {pass: "%s", location: unknown, groups:[all]}\n' % (name, password))

    app.contest = Contest.load(app.opts.contest)


@default.route('/register/', methods={'GET', 'POST'})
def register():
    global contest
    if not app.contest.register or is_logged_in():
        abort(404)

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

        if team_name in app.contest.teams:
            error.append('Team name is already taken.')

        rx = '^[-_A-Za-z0-9 ]{5,20}$'
        if not re.match(rx, password):
            error.append('Password is illegal (it must match %s).' % rx)

        if password != confirm_password:
            error.append('Password confirmation was incorrect.')

        if not error:
            _register_team(team_name, password)
            return redirect(url_for('default.login', register='True'))

    return render_template('register.html', team_name=team_name, error=error)
