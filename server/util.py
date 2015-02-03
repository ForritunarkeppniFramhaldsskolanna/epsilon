import datetime
import functools
from flask import redirect, url_for as real_url_for, request, session, current_app as app
from server.data import verdict_explanation
from lib.models import Submission


# TODO: make this work for internal redirects
def url_for(path, **values):
    res = real_url_for(path, **values)
    if app.opts.prefix:
        return app.opts.prefix + res
    else:
        return res


def is_logged_in():
    return 'team' in session and session['team'] in app.contest.teams


def judge_is_logged_in():
    return 'judge' in session and session['judge'] in app.contest.judges


def get_team():
    if not is_logged_in():
        return None
    return app.contest.teams.get(session['team'])


def get_judge():
    if not judge_is_logged_in():
        return None
    return app.contest.judges.get(session['judge'])


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


def context_processor():

    solved = set()
    tried = set()
    team = get_team()
    judge = get_judge()

    if team:
        cur_time = datetime.datetime.now()
        subs = Submission.query.filter(Submission.submitted <= cur_time).filter_by(team=team.name).all()
        for sub in subs:
            if sub.verdict == 'AC':
                solved.add(sub.problem)
                tried.add(sub.problem)
            elif sub.verdict not in {'SE', 'RF', 'CJ', 'QU', 'CE'}:
                tried.add(sub.problem)

    return dict(
        contest=app.contest,
        phase=app.contest.get_current_phase(),
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
