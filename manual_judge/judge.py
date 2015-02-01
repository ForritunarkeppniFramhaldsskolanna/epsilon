import sys
import os
import errno
import argparse
import datetime
import shutil
import time
import random
from subprocess import Popen, PIPE
from sqlalchemy import or_

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, BASE_DIR)
import lib.judgelib as j
from lib.judgelib import Submission, SubmissionQueue, SUBMISSION_JUDGE_TIMEOUT
from lib.yamllib import load, dump

SUBMISSION_WAIT = 1000  # ms


def format_time(time):
    return '%02d:%02d' % (int(time // 60), int(time) % 60)


def do_list(opts, parser):
    if opts.type not in {'all', 'queue'}:
        parser.print_help()
        exit(0)

    db = j.get_db()
    try:
        sess = db()

        if opts.type == 'all':
            subs = sess.query(Submission)
        elif opts.type == 'queue':
            subs = sess.query(Submission, SubmissionQueue).join(SubmissionQueue, Submission.id == SubmissionQueue.submission_id)

        if opts.team:
            subs = subs.filter(Submission.team == opts.team)
        if opts.problem:
            subs = subs.filter(Submission.problem == opts.problem)

        for item in subs.order_by(Submission.submitted).all():
            sub = item
            subq = None
            if opts.type == 'queue':
                sub = item[0]
                subq = item[1]

            sys.stdout.write('%d\t%s\t%s\t%s\t%s\t%s\n' % (sub.id, format_time(sub.submitted), sub.team, sub.problem, sub.verdict, '' if subq is None else subq.last_announce))

    finally:
        sess.close()


def do_checkout(opts, parser):

    db = j.get_db()
    try:
        sess = db()

        if opts.id == 'next':
            fst = True
            while True:

                get_before = datetime.datetime.now() - datetime.timedelta(0, SUBMISSION_JUDGE_TIMEOUT / 1000.0)
                # TODO: do something smarter for concurrency
                qsub = sess.query(SubmissionQueue).filter(or_(SubmissionQueue.last_announce == None, SubmissionQueue.last_announce < get_before)).first()

                if qsub:
                    opts.id = qsub.submission_id
                    sys.stdout.write('checking out submission %d\n' % opts.id)
                    break

                if fst:
                    sys.stdout.write('waiting for next submission...\n')
                    fst = False

                time.sleep(SUBMISSION_WAIT / 1000.0 + random.random())

        opts.id = int(opts.id)

        sub = sess.query(Submission).filter_by(id=opts.id).first()
        if not sub:
            sys.stderr.write('error: submission with id %d not found\n' % opts.id)
            exit(1)

        qsub = sess.query(SubmissionQueue).filter_by(submission_id=opts.id).first()
        if qsub:
            qsub.last_announce = datetime.datetime.now()
            sess.commit()

        lang = load(j.LANGUAGES_FILE)[sub.language]

        if os.path.isdir(str(opts.id)):
            shutil.rmtree(str(opts.id))

        os.mkdir(str(opts.id))
        with open(os.path.join(str(opts.id), 'submission.yaml'), 'w') as f:
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

        with open(os.path.join(str(opts.id), lang['filename']), 'w') as f:
            f.write(sub.file)

        shutil.copytree(os.path.join(j.TESTS_DIR, sub.problem), os.path.join(str(opts.id), 'tests'))

    finally:
        sess.close()


def do_current_submit(opts, parser):
    subdetails = load('submission.yaml')
    sid = int(subdetails['id'])

    db = j.get_db()
    try:
        sess = db()
        sub = sess.query(Submission).filter_by(id=sid).first()
        if not sub:
            sys.stderr.write('error: submission with id %d not found\n' % opts.id)
            exit(1)

        qsub = sess.query(SubmissionQueue).filter_by(submission_id=sid).first()
        if opts.verdict == 'QU':
            if qsub:
                qsub.last_announce = None
            else:
                sess.add(SubmissionQueue(sid))
        else:
            if qsub:
                sess.delete(qsub)
                sess.commit()

        sub.verdict = opts.verdict
        if opts.message:
            sub.judge_response = opts.message

        if sub.verdict == 'AC':
            j.deliver_balloon(sess, sub)

        sess.commit()

    finally:
        sess.close()


def do_current_compile(opts, parser):
    subdetails = load('submission.yaml')
    sid = int(subdetails['id'])

    db = j.get_db()
    try:
        sess = db()
        sub = sess.query(Submission).filter_by(id=sid).first()
        if not sub:
            sys.stderr.write('error: submission with id %d not found\n' % opts.id)
            exit(1)

        lang = load(j.LANGUAGES_FILE)[sub.language]

        if 'compile' in lang:
            proc = Popen(lang['compile'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
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


def do_current_execute(opts, parser):
    subdetails = load('submission.yaml')
    sid = int(subdetails['id'])

    db = j.get_db()
    try:
        sess = db()
        sub = sess.query(Submission).filter_by(id=sid).first()
        if not sub:
            sys.stderr.write('error: submission with id %d not found\n' % opts.id)
            exit(1)

        lang = load(j.LANGUAGES_FILE)[sub.language]
        proc = Popen(lang['execute'])
        proc.wait()

    finally:
        sess.close()


def do_current(opts, parser):
    if opts.current_cmd_subparser_name is None:
        parser.print_help()
        exit(0)

    actions = {'submit': do_current_submit, 'compile': do_current_compile, 'execute': do_current_execute}
    actions[opts.current_cmd_subparser_name](opts, parser)


verdict_explanation = {
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


def do_help(opts, parser):
    if opts.item == "verdicts":
        print("\n".join("%s: %s" % (k, v) for k, v in verdict_explanation.items()))


def main(argv):

    parser = argparse.ArgumentParser(description='A command line judge interface.')
    parser.add_argument('-c', '--config', default='config.yml', help='config file')

    subparsers = parser.add_subparsers(dest='subparser_name')

    list_cmd = subparsers.add_parser('list', help='list submissions')
    list_cmd.add_argument('type', help='which submissions to list')
    list_cmd.add_argument('-t', '--team', help='filter by team')
    list_cmd.add_argument('-p', '--problem', help='filter by problem')

    checkout_cmd = subparsers.add_parser('checkout', help='checkout submission')
    checkout_cmd.add_argument('id', help='which submissions to checkout')
    # checkout_cmd.add_argument('-t', '--time', default=j.SUBMISSION_JUDGE_TIMEOUT, help='how long the submission should be checked out for')

    current_cmd = subparsers.add_parser('current', help='various operations for the current submission')

    current_cmd_subparsers = current_cmd.add_subparsers(dest='current_cmd_subparser_name')
    current_cmd_submit = current_cmd_subparsers.add_parser('submit', help='submit the current submission (see help verdicts for explanations)')
    current_cmd_submit.add_argument('verdict', help='the verdict', choices=verdict_explanation.keys())
    current_cmd_submit.add_argument('-m', '--message', help='a message with the verdict')

    current_cmd_compile = current_cmd_subparsers.add_parser('compile', help='compile the current submission')
    current_cmd_execute = current_cmd_subparsers.add_parser('execute', help='execute the current submission')

    help_cmd = subparsers.add_parser('help', help="additional information for submissions")
    help_cmd.add_argument("item", help="what item to help with")

    opts = parser.parse_args(argv)

    config = j.load(opts.config)

    j.set_contest_id(config['contest_id'])

    j.DB_CONN_STRING = config['db_conn_string']
    j.TESTS_DIR = os.path.abspath(os.path.join(os.path.dirname(opts.config), config['tests_dir']))

    if opts.subparser_name is None:
        parser.print_help()
        exit(0)

    actions = {'list': do_list, 'checkout': do_checkout, 'current': do_current, 'help': do_help}
    try:
        actions[opts.subparser_name](opts, parser)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main(sys.argv[1:])
