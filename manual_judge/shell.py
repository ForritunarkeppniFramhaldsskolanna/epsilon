#!/usr/bin/env python3

import sys
import os
import re
import datetime
import shutil

from subprocess import Popen, PIPE

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, BASE_DIR)

import lib.judgelib as j
from lib.models import Submission, SubmissionQueue
import lib.models as models
from lib.yamllib import load, dump
from lib.queue import Submissions

contest = None

SUBMISSION_WAIT = 1000  # ms
contest = None


verdict_explanation = {
    'QU': 'in queue',
    'AC': 'accepted',
    'PE': 'presentation error',
    'WA': 'wrong answer',
    'CE': 'compile time error',
    'RE': 'runtime error',
    'TL': 'time limit exceeded',
    'ML': 'memory limit exceeded',
    'SE': 'submission error',
    'RF': 'restricted function',
    'CJ': 'cannot judge',
}


def format_time(time):
    if isinstance(time, datetime.datetime):
        time = (time - contest["start"]).total_seconds()
    return '%02d:%02d' % (int(time // 60), int(time) % 60)


# Execute helper functions
def execute(cwd, test=False, data=None):
    subdetails = load(os.path.join(cwd, 'submission.yaml'))
    sid = int(subdetails['id'])

    db = models.get_db(j.DB_CONN_STRING)
    try:
        sess = db()
        sub = sess.query(Submission).filter_by(id=sid).first()
        if not sub:
            sys.stderr.write('error: submission with id %d not found\n' % sid)
            exit(1)

        lang = load(j.LANGUAGES_FILE)[sub.language]
        if test:
            return run(lang['execute'], cwd, stdin=data)
        else:
            return run(lang['execute'], cwd, stdin=False)
    finally:
        sess.close()


def run(cmd, cwd=None, stdin=None):
    if cwd:
        cwd = os.getcwd()
    if stdin is False:
        proc = Popen(cmd, stdin=None, stdout=PIPE, stderr=PIPE, cwd=cwd)
        stdout, stderr = proc.communicate()
    else:
        proc = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=cwd)
        stdout, stderr = proc.communicate(stdin.encode('utf-8') if stdin is not None else b'')
    return (proc.returncode, stdout.decode('utf-8'), stderr.decode('utf-8'))


def getno(name):
    ar = re.findall(r'\d+', name)
    return int(ar[-1])


def submissions(type, team=None, problem=None):
    db = models.get_db(j.DB_CONN_STRING)
    try:
        sess = db()

        if type == 'all':
            subs = sess.query(Submission)
        elif type == 'queue':
            subs = sess.query(Submission, SubmissionQueue).join(SubmissionQueue, Submission.id == SubmissionQueue.submission_id)

        if team:
            subs = subs.filter(Submission.team == team)
        if problem:
            subs = subs.filter(Submission.problem == problem)

        for item in subs.order_by(Submission.submitted).all():
            sub = item
            subq = None
            if type == 'queue':
                sub = item[0]
                subq = item[1]

            sys.stdout.write('%d\t%s\t%s\t%s\t%s\t%s\n' % (sub.id, format_time(sub.submitted), sub.team, sub.problem, sub.verdict, '' if subq is None else subq.dequeued_at))

    finally:
        sess.close()


def checkout(id, cwd=None):
    sub = None
    if id == 'next':
        sys.stdout.write('waiting for next submission...\n')

        with Submissions(j.DB_CONN_STRING, timeout=False) as subs:
            sub2 = next(subs)
            id = sub2.id
            sys.stdout.write('checking out submission %d\n' % id)
            # Duplicate so we don't get a detached error
            sub = Submission(sub2.team, sub2.problem, sub2.language, sub2.file, sub2.submitted, sub2.verdict, sub2.judge_response)
            sub.id = sub2.id
    else:
        db = models.get_db(j.DB_CONN_STRING)
        try:
            sess = db()
            id = int(id)

            sub2 = sess.query(Submission).filter_by(id=id).first()
            if not sub2:
                sys.stderr.write('error: submission with id %d not found\n' % id)
                exit(1)

            qsub = sess.query(SubmissionQueue).filter_by(submission_id=id).first()
            if qsub:
                qsub.dequeued_at = datetime.datetime.now()
                qsub.status = 1
                sess.commit()
            # Duplicate so we don't get a detached error
            sub = Submission(sub2.team, sub2.problem, sub2.language, sub2.file, sub2.submitted, sub2.verdict, sub2.judge_response)
            sub.id = sub2.id
        finally:
            sess.close()

    lang = load(j.LANGUAGES_FILE)[sub.language]
    if cwd is None:
        cwd = os.getcwd()
    path = os.path.join(cwd, str(id))
    if os.path.isdir(path):
        shutil.rmtree(path)

    os.mkdir(path)
    with open(os.path.join(path, 'submission.yaml'), 'w') as f:
        f.write(dump({
            'id': sub.id,
            'team': sub.team,
            'problem': sub.problem,
            'submitted': sub.submitted,
            'verdict': sub.verdict,
            'judge_response': sub.judge_response,
            'language': {
                'name': sub.language,
                'compile': lang.get('compile'),
                'execute': lang.get('execute')
            }
        }))

    with open(os.path.join(path, lang['filename']), 'w') as f:
        f.write(sub.file)

    test_dir = os.path.join(j.CONTEST_DIR, 'problems', sub.problem, '.epsilon', 'tests')
    test_dst = os.path.abspath(os.path.join(path, 'tests'))

    shutil.copytree(test_dir, test_dst,
                    ignore=lambda dir, files: [f for f in files if not (f.endswith(".in") or f.endswith(".out"))])

    print("Language: %s" % sub.language)
    print("Problem: %s" % sub.problem)
    print("Team: %s" % sub.team)
    return path


def compile():
    subdetails = load(os.path.join(os.getcwd(), 'submission.yaml'))
    sid = int(subdetails['id'])

    db = models.get_db(j.DB_CONN_STRING)
    try:
        sess = db()
        sub = sess.query(Submission).filter_by(id=sid).first()
        if not sub:
            sys.stderr.write('error: submission with id %d not found\n' % id)
            exit(1)

        lang = load(j.LANGUAGES_FILE)[sub.language]

        if 'compile' in lang:
            proc = Popen(lang['compile'], stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=os.getcwd())
            comp_err = proc.communicate()[1]
            comp_err = '' if comp_err is None else comp_err.decode('utf-8')
            if proc.wait() != 0:
                sys.stdout.write('compile error:\n' + comp_err + '\n')
            else:
                sys.stdout.write('compile successful\n')
        else:
            sys.stdout.write('no compiler for this language\n')

    finally:
        sess.close()


def submit(verdict, message=None):
    verdict = verdict.upper()

    subdetails = load(os.path.join(os.getcwd(), 'submission.yaml'))
    sid = int(subdetails['id'])

    db = models.get_db(j.DB_CONN_STRING)
    try:
        sess = db()
        sub = sess.query(Submission).filter_by(id=sid).first()
        if not sub:
            sys.stderr.write('error: submission with id %d not found\n' % sid)
            exit(1)

        qsub = sess.query(SubmissionQueue).filter_by(submission_id=sid).first()
        if verdict == 'QU':
            if qsub:
                qsub.dequeued_at = None
                qsub.status = 0
            else:
                sess.add(SubmissionQueue(sid))
        else:
            if qsub:
                sess.delete(qsub)
                sess.commit()

        sub.verdict = verdict
        if message:
            sub.judge_response = message

        if sub.verdict == 'AC':
            j.deliver_balloon(sess, sub)

        sess.commit()

    finally:
        sess.close()


def get_tests():
    files = [f[0:-3] for f in os.listdir(os.path.join(os.getcwd(), "tests")) if f.endswith(".in")]
    # Fix this sorting shit
    files.sort(key=lambda s: (s.split("__")[0], getno(s)))
    return files


def load_contest(name=None):
    global contest
    if name:
        contest = j.load_contest(name)
    else:
        contest = j.load_contest(os.getenv("CONTEST", name))
