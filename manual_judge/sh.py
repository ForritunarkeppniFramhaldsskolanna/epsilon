"""The main xonsh script."""
import sys
import os
import argparse
import builtins
import shell
import tempfile
from functools import wraps

BASE_DIR = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(BASE_DIR, "xonsh"))
from xonsh.shell import Shell
from xonsh.parser import Parser

parser2 = Parser(lexer_table='lexer_table', yacc_table='parser_table',
       outputdir=os.path.join(BASE_DIR, "xonsh", "xonsh"))

ROOT = tempfile.mkdtemp(prefix="epsilon")
os.chdir(ROOT)
os.environ["USER"] = "ɛ"


def chdir(d):
    os.chdir(d)
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
    ar('type', help='which submissions to list'),
    ar('-t', '--team', help='filter by team'),
    ar('-p', '--problem', help='filter by problem')
)
def submissions(arg, opts, parser, stdin=None):
    return shell.submissions(opts.type, opts.team, opts.problem)


@arguments(
    ar(description='Checkout submission'),
    ar('id', help='which submissions to checkout')
)
def checkout(arg, opts, parser, stdin=None):
    return chdir(shell.checkout(opts.id))


@current
@arguments(
    ar(description='Compile current submission')
)
def compile(arg, opts, parser, stdin=None):
    shell.compile()


@current
@arguments(
    ar(description='Execute current submission'),
    ar('test', nargs="?", default="", help="The test case to execute"),
    ar('-d', '--detail', action="store_true", help="Print detailed output of the submission")
)
def execute(arg, opts, parser, stdin=None):
    data = None
    if opts.test:
        path = os.path.join(os.getcwd(), "tests", opts.test + ".in")
        if not os.path.isfile(path):
            sys.stderr.write("Test %s does not exist, exiting.\n" % opts.test)
        with open(path, 'r', encoding='utf-8') as f:
            data = f.read()
        val = shell.execute(os.getcwd(), test=True, data=data)
    else:
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
    return "\n".join(f for f in shell.get_tests())


def verdicts(arg, stdin=None):
    """Lists the available verdicts"""
    print("\n".join("%s: %s" % (k, v) for k, v in shell.verdict_explanation.items()))


def setup_aliases():
    builtins.aliases["execute"] = builtins.aliases["ex"] = execute
    builtins.aliases["submissions"] = builtins.aliases["subs"] = submissions
    builtins.aliases["checkout"] = builtins.aliases["ch"] = checkout
    builtins.aliases["compile"] = builtins.aliases["comp"] = compile
    builtins.aliases["submit"] = builtins.aliases["subm"] = submit
    builtins.aliases["tests"] = tests
    builtins.aliases["verdicts"] = verdicts
    builtins.aliases["l"] = ["ls"]
    builtins.aliases["c"] = ["cd"]


def main(argv):
    parser = argparse.ArgumentParser(description='An automatic programming contest judge.')
    parser.add_argument('contest', help='the contest directory')
    opts = parser.parse_args(argv)

    shell.load_contest(opts.contest)

    cmd = Shell()
    cmd.execer.parser = parser2
    setup_aliases()
    cmd.cmdloop()

# def tracefunc(frame, event, arg, indent=[0]):
#     if event == "call":
#         indent[0] += 2
#         print("-" * indent[0] + "> call function", frame.f_code.co_name)
#     elif event == "return":
#         print("<" + "-" * indent[0], "exit function", frame.f_code.co_name)
#         indent[0] -= 2
#     return tracefunc

# import sys
# sys.settrace(tracefunc)

if __name__ == '__main__':
    main(sys.argv[1:])
    # pass
