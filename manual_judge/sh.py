"""The main xonsh script."""
import sys
import os
import argparse
import builtins
import shell
import tempfile
import shlex
from functools import wraps

BASE_DIR = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(BASE_DIR, "xonsh"))
from xonsh.shell import Shell
from xonsh.parser import Parser
from xonsh.tools import TERM_COLORS

ROOT = None


def chdir(d):
    os.chdir(d)
    if hasattr(builtins, "__xonsh_env__"):
        builtins.__xonsh_env__['PWD'] = os.getcwd()


# Decorator functions
# for making sure the current directory is a submission directory
def current(*arg, **kwarg):
    error = True
    if arg and not callable(arg[0]):
        error = False
    elif kwarg:
        error = kwarg["error"]

    def decorator(func):
        @wraps(func)
        def validate(*args, **kwargs):
            if not os.path.isfile(os.path.join(os.getcwd(), "submission.yaml")):
                if error:
                    print("Not in submission directory, exiting...")
                return False
            return func(*args, **kwargs)
        return validate
    if arg and callable(arg[0]):
        return decorator(arg[0])
    return decorator


# A cool helper function to make a tuple of arguments
def ar(*args, **kwargs):
    return args, kwargs


# Runs argparse on the arguments passed before running the function
def arguments(*gargs, **gkwargs):
    def decorator(func):
        if "prog" not in gargs[0][1]:
            gargs[0][1]["prog"] = func.__name__
        parser = argparse.ArgumentParser(*gargs[0][0], **gargs[0][1])
        for i in range(1, len(gargs)):
            parser.add_argument(*gargs[i][0], **gargs[i][1])

        @wraps(func)
        def args(*args, **kwargs):
            try:
                opts = parser.parse_args(args[0])
                args = args + (opts, parser)
                return func(*args, **kwargs)
            except SystemExit:
                return None
        args.__doc__ = parser.format_help()
        return args
    return decorator


@arguments(
    ar(description='List submissions'),
    ar('type', nargs="?", default="queue", help='which submissions to list'),
    ar('-t', '--team', help='filter by team'),
    ar('-p', '--problem', help='filter by problem')
)
def submissions(arg, opts, parser, stdin=None):
    return shell.submissions(opts.type, opts.team, opts.problem)


@arguments(
    ar(description='Checkout submission'),
    ar('id', nargs="?", default="next", help='which submissions to checkout')
)
def checkout(arg, opts, parser, stdin=None):
    return chdir(shell.checkout(opts.id, cwd=ROOT))


@current
@arguments(
    ar(description='Compile current submission')
)
def compile_sub(arg, opts, parser, stdin=None):
    shell.compile()


@current
@arguments(
    ar(description='Execute current submission'),
    ar('-d', '--detail', action="store_true", help="Print detailed output of the submission")
)
def execute(arg, opts, parser, stdin=None):
    val = shell.execute(os.getcwd())
    if opts.detail:
        print("Return code %d." % val[0])
        if val[1].strip():
            print("stdout:\n%s" % val[1].strip())
        if val[2].strip():
            print("stderr:\n%s" % val[2].strip())
    else:
        if val[1].strip():
            sys.stdout.write(val[1])
        if val[2].strip():
            sys.stderr.write(val[2])


def run_test(test, detail=False, diff=True, diff_cmd="sdiff --ignore-all-space"):
    path = os.path.join(os.getcwd(), "tests", test)
    if not os.path.isfile(path):
        sys.stderr.write("Test %s does not exist, exiting.\n" % test)
        return

    data = None
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()

    val = shell.execute(os.getcwd(), test=True, data=data)
    if diff and diff_cmd is not None:
        print("Exit status: %d" % val[0])
        if val[2].strip():
            print("stderr:\n%s" % val[2].strip())
        out = path[:-3] + ".out"
        valdiff = shell.run(shlex.split(diff_cmd) + [out, "-"], stdin=val[1])

        if valdiff[0] == 1:
            print("diff: Output mismatch")
            print(valdiff[1].strip())
            return False
        elif valdiff[0] == 0:
            print("diff: Output matches")
            return True
        else:
            print("diff returned non-zero exit status! %d" % valdiff[0])
            if valdiff[1].strip():
                print("stdout:\n%s" % valdiff[1].strip())
            if valdiff[2].strip():
                print("stderr:\n%s" % valdiff[2].strip())
            return None
    else:
        if detail:
            print("Exit status %d." % val[0])
            if val[1].strip():
                print("stdout:\n%s" % val[1].strip())
            if val[2].strip():
                print("stderr:\n%s" % val[2].strip())
        else:
            if val[1].strip():
                sys.stdout.write(val[1])
            if val[2].strip():
                sys.stderr.write(val[2])
    return None


@current
@arguments(
    ar(description='Run current submission against a test case'),
    ar('test', nargs="?", default="all", help="The test case to execute"),
    ar('-d', '--detail', action="store_true", help="Print detailed output of the submission"),
    ar("-f", '--full', action="store_false", help="Print the full submission output"),
    ar("diff", nargs=argparse.REMAINDER, default="sdiff --ignore-all-space", help="The diff command to run")
)
def test(arg, opts, parser, stdin=None):
    if opts.test == "all":
        accepted = True
        errors = []
        for test in shell.get_tests():
            print("\n%sRunning test case: %s%s%s" % (TERM_COLORS["BOLD_YELLOW"], TERM_COLORS["UNDERLINE_YELLOW"], test, TERM_COLORS["NO_COLOR"]))
            ret = run_test(test + ".in", detail=opts.detail, diff=opts.full, diff_cmd=opts.diff)
            if not ret:
                accepted = False
                errors.append(test)
                if not opts.full:
                    print("%sIncorrect output%s" % (TERM_COLORS["BACKGROUND_RED"], TERM_COLORS["NO_COLOR"]))
        if opts.full:
            if accepted:
                print("%sAccepted output%s" % (TERM_COLORS["BOLD_GREEN"], TERM_COLORS["NO_COLOR"]))
            else:
                print("%sIncorrect output%s" % (TERM_COLORS["BOLD_RED"], TERM_COLORS["NO_COLOR"]))
                print("%sFirst incorrect output at: %s%s" % (TERM_COLORS["PURPLE"], errors[0], TERM_COLORS["NO_COLOR"]))
    else:
        if not opts.test.endswith(".in"):
            opts.test += ".in"
        run_test(opts.test, detail=opts.detail, diff=opts.full, diff_cmd=opts.diff)


@current
@arguments(
    ar(description='submit the current submission'),
    ar('verdict', help='the verdict  (see `verdicts` for explanations)', choices=shell.verdict_explanation.keys()),
    ar('-m', '--message', help='a message with the verdict')
)
def submit(arg, opts, parser, stdin=None):
    shell.submit(opts.verdict, opts.message)


@current
def tests(arg, stdin=None):
    """Lists the available tests"""
    print("\n".join(f for f in shell.get_tests()))


def verdicts(arg, stdin=None):
    """Lists the available verdicts"""
    print("\n".join("%s: %s" % (k, v) for k, v in shell.verdict_explanation.items()))


def setup_aliases():
    builtins.aliases["execute"] = builtins.aliases["ex"] = execute
    builtins.aliases["test"] = test
    builtins.aliases["submissions"] = builtins.aliases["subs"] = submissions
    builtins.aliases["checkout"] = builtins.aliases["ch"] = checkout
    builtins.aliases["compile"] = builtins.aliases["comp"] = compile_sub
    builtins.aliases["submit"] = builtins.aliases["subm"] = submit
    builtins.aliases["tests"] = tests
    builtins.aliases["verdicts"] = verdicts


def setup_shortcuts():
    builtins.aliases["l"] = ["ls"]
    builtins.aliases["c"] = builtins.aliases["cd"]

prompt_template = ('{GREEN}ɛ{BLUE} {cwd} {YELLOW}${NO_COLOR} ')


def default_prompt():
    env = builtins.__xonsh_env__
    cwd = env['PWD']
    p = prompt_template.format(
        cwd=cwd.replace(env['HOME'], '~').replace(ROOT, 'judging'),
        RED=TERM_COLORS['BOLD_RED'],
        BLUE=TERM_COLORS['BOLD_BLUE'],
        GREEN=TERM_COLORS['BOLD_GREEN'],
        YELLOW=TERM_COLORS['BOLD_YELLOW'],
        NO_COLOR=TERM_COLORS['NO_COLOR'],
    )
    return p


def setup_env():
    builtins.__xonsh_env__["PROMPT"] = default_prompt


def main(argv):
    global ROOT
    parser = argparse.ArgumentParser(description='An automatic programming contest judge.')
    parser.add_argument('contest', help='the contest directory')
    parser.add_argument('-d', "--directory", default=None, help="The root directory")
    opts = parser.parse_args(argv)

    sh_parser = Parser(lexer_table='lexer_table', yacc_table='parser_table', outputdir=os.path.join(BASE_DIR, "xonsh", "xonsh"))
    if opts.directory:
        ROOT = opts.directory
    else:
        ROOT = tempfile.mkdtemp(prefix="epsilon")
    os.chdir(ROOT)
    os.environ["USER"] = "ɛ"

    shell.load_contest(opts.contest)

    cmd = Shell()
    cmd.execer.parser = sh_parser
    setup_shortcuts()
    setup_aliases()
    setup_env()
    cmd.cmdloop()

if __name__ == '__main__':
    main(sys.argv[1:])
