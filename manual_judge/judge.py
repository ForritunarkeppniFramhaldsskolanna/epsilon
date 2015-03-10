import sys
import os
import argparse
from subprocess import Popen, PIPE

import shell
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, BASE_DIR)
import lib.judgelib as j
from lib.models import Submission
import lib.models as models
from lib.yamllib import load

SUBMISSION_WAIT = 1000  # ms
contest = None
CWD = os.getcwd()


def do_list(opts, parser):
    if opts.type not in {'all', 'queue'}:
        parser.print_help()
        exit(0)

    shell.submissions(opts.type, team=opts.team, problem=opts.problem)


def do_checkout(opts, parser):
    shell.checkout(opts.id)


def do_current_submit(opts, parser, cwd=None):
    shell.submit(opts.verdict, opts.message)


def do_current_compile(opts, parser, cwd=None):
    shell.compile()


def do_current_execute(opts, parser, cwd=None, data=None):
    if cwd is None:
        cwd = CWD
    subdetails = load(os.path.join(cwd, 'submission.yaml'))
    sid = int(subdetails['id'])

    db = models.get_db(j.DB_CONN_STRING)
    try:
        sess = db()
        sub = sess.query(Submission).filter_by(id=sid).first()
        if not sub:
            sys.stderr.write('error: submission with id %d not found\n' % opts.id)
            exit(1)

        lang = load(j.LANGUAGES_FILE)[sub.language]
        proc = None
        if data:
            proc = Popen(lang['execute'], stdin=PIPE, cwd=cwd)
            proc.communicate(input=data.encode())
        else:
            proc = Popen(lang['execute'], cwd=cwd)
        proc.wait()

    finally:
        sess.close()


def do_current(opts, parser):
    if opts.current_cmd_subparser_name is None:
        parser.print_help()
        exit(0)

    actions = {'submit': do_current_submit, 'compile': do_current_compile, 'execute': do_current_execute}
    actions[opts.current_cmd_subparser_name](opts, parser)


def do_help(opts, parser):
    if opts.item == "verdicts":
        print("\n".join("%s: %s" % (k, v) for k, v in shell.verdict_explanation.items()))


def main(argv):
    parser = argparse.ArgumentParser(description='A command line judge interface.')
    parser.add_argument('-c', '--contest', help='contest')

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
    current_cmd_submit.add_argument('verdict', help='the verdict', choices=shell.verdict_explanation.keys())
    current_cmd_submit.add_argument('-m', '--message', help='a message with the verdict')

    current_cmd_compile = current_cmd_subparsers.add_parser('compile', help='compile the current submission')
    current_cmd_execute = current_cmd_subparsers.add_parser('execute', help='execute the current submission')

    help_cmd = subparsers.add_parser('help', help="additional information for submissions")
    help_cmd.add_argument("item", help="what item to help with")

    opts = parser.parse_args(argv)
    shell.load_contest(opts.contest)

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
