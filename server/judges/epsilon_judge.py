import sys, os, argparse, datetime, shutil
from subprocess import Popen, PIPE
import yaml
sys.path.append('../../lib')
import judgelib as j
from judgelib import *

def format_time(time):
    return '%02d:%02d' % (int(time//60), int(time)%60)

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

        if opts.team: subs = subs.filter(Submission.team == opts.team)
        if opts.problem: subs = subs.filter(Submission.problem == opts.problem)

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
    opts.id = int(opts.id)

    db = j.get_db()
    try:
        sess = db()
        sub = sess.query(Submission).filter_by(id=opts.id).first()
        if not sub:
            sys.stderr.write('error: submission with id %d not found\n' % opts.id)
            exit(1)

        qsub = sess.query(SubmissionQueue).filter_by(submission_id=opts.id).first()
        if qsub:
            qsub.last_announce = datetime.datetime.now()
            sess.commit()

        lang = load(j.LANGUAGES_FILE)[sub.language]

        os.mkdir(str(opts.id))
        with open(os.path.join(str(opts.id), 'submission.yaml'), 'w') as f:
            f.write('id: %d\n' % sub.id)
            f.write('team: %s\n' % sub.team)
            f.write('problem: %s\n' % sub.problem)
            f.write('submitted: %s\n' % sub.submitted)
            f.write('verdict: %s\n' % sub.verdict)
            f.write('judge_response: %s\n' % sub.judge_response)
            f.write('language:\n')
            f.write('    name: %s\n' % sub.language)
            f.write('    compile: %s\n' % lang['compile'])
            f.write('    execute: %s\n' % lang['execute'])

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
            j.deliver_balloon(sess, sub.team, sub.problem)

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

    current_cmd_submit = current_cmd_subparsers.add_parser('submit', help='submit the current submission')
    current_cmd_submit.add_argument('verdict', help='the verdict')
    current_cmd_submit.add_argument('-m', '--message', help='a message with the verdict')

    current_cmd_compile = current_cmd_subparsers.add_parser('compile', help='compile the current submission')
    current_cmd_execute = current_cmd_subparsers.add_parser('execute', help='execute the current submission')

    opts = parser.parse_args(argv)

    config = j.load(opts.config)
    j.DB_CONN_STRING = config['db_conn_string']
    j.TESTS_DIR = os.path.abspath(os.path.join(os.path.dirname(opts.config), config['tests_dir']))
    j.LANGUAGES_FILE = os.path.abspath(os.path.join(os.path.dirname(opts.config), config['languages_file']))

    if opts.subparser_name is None:
        parser.print_help()
        exit(0)

    actions = {'list': do_list, 'checkout': do_checkout, 'current': do_current}
    actions[opts.subparser_name](opts, parser)


if __name__ == '__main__':
    main(sys.argv[1:])

