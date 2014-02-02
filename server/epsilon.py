#!/usr/bin/python3
import os, sys
DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(DIR)

import argparse
import hashlib
import yaml
import datetime
import time
import functools
from flask import Flask, g, redirect, abort, render_template, url_for, request, session, send_from_directory
from data import Contest, ScoreboardTeamProblem
from models import *


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


def is_logged_in():
    return 'team' in session and session['team'] in contest.teams

def get_team():
    if not is_logged_in(): return None
    return contest.teams.get(session['team'])

def only_localhost(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if request.remote_addr != '127.0.0.1':
            abort(403)
        return f(*args, **kwargs)
    return decorated

def login_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for('login', next=request.path))
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

        if (phase.frozen is not None and sub.submitted > 60.0 * phase.frozen and (not is_logged_in() or get_team().name != sub.team)) or sub.verdict == 'QU':
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
    team_name = ''
    password = ''
    bad_login = False
    if is_logged_in():
        return redirect(goto)
    if request.method == 'POST':
        team_name = request.form['team']
        password = request.form['password']
        if team_name in contest.teams and contest.teams[team_name].password == password:
            session['team'] = team_name
            return redirect(goto)
        else:
            session.pop('team', '')
            bad_login = True
    return render_template('login.html', team_name=team_name, bad_login=bad_login)

@app.route('/logout/')
def logout():
    session.pop('team', '')
    return redirect(url_for('index'))

# TODO: make sure only works on localhost, IT DOESNT SEEM TO WORK (probably because of nginx layer)
@app.route('/_reload/')
@only_localhost
def _reload():
    global contest
    contest = Contest.load(opts.contest)
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html')

def main(argv):
    global opts, contest, conn
    parser = argparse.ArgumentParser(description='A minimalistic programming contest environment.')
    parser.add_argument('contest', help='the contest directory')
    parser.add_argument('-p', '--port', default=31415, type=int, help='the port to listen on')
    parser.add_argument('-H', '--host', default='', help='the host to listen on')
    parser.add_argument('-d', '--debug', default=False, action='store_true', help='run in debug mode')
    opts = parser.parse_args(argv)
    contest = Contest.load(opts.contest)
    app.config['SQLALCHEMY_DATABASE_URI'] = contest.db

    for table in db.metadata.tables.values():
        table.name = '%s_%s' % (contest.id, table.name)

    db.init_app(app)
    # db.drop_all(app=app)
    db.create_all(app=app)
    app.run(host=opts.host, port=opts.port, debug=opts.debug)

if __name__ == '__main__':
    main(sys.argv[1:])

