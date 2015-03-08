#!/usr/bin/env python3

import sys
import os
import argparse
import readline
import shlex
import logging
import cmd
import tempfile
import re

from functools import wraps
from subprocess import call, Popen, PIPE

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, BASE_DIR)
import judge

SUBMISSION_WAIT = 1000  # ms
EDITOR = os.environ.get('EDITOR', 'vim')  # that easy!
contest = None
ROOT = tempfile.mkdtemp(prefix="epsilon")
judge.CWD = ROOT

PROMPT = "ɛ %s > "


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
            if not os.path.isfile(os.path.join(args[0].cwd(), "submission.yaml")):
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
            gargs[0][1]["prog"] = func.__name__[3:]
        parser = argparse.ArgumentParser(*gargs[0][0], **gargs[0][1])
        for i in range(1, len(gargs)):
            parser.add_argument(*gargs[i][0], **gargs[i][1])

        @wraps(func)
        def args(*args, **kwargs):
            opts = parser.parse_args(args[1])
            args = args + (opts, parser)
            return func(*args, **kwargs)
        args.__doc__ = parser.format_help()
        return args
    return decorator


# Execute helper functions
def execute(cwd, test=False, data=None):
    subdetails = judge.load(os.path.join(cwd, 'submission.yaml'))
    sid = int(subdetails['id'])

    db = judge.models.get_db(judge.j.DB_CONN_STRING)
    try:
        sess = db()
        sub = sess.query(judge.Submission).filter_by(id=sid).first()
        if not sub:
            sys.stderr.write('error: submission with id %d not found\n' % sid)
            exit(1)

        lang = judge.load(judge.j.LANGUAGES_FILE)[sub.language]
        if test:
            return _exec(lang['execute'], cwd, stdin=data)
        else:
            return _exec(lang['execute'], cwd, stdin=False)
    finally:
        sess.close()


def _exec(cmd, cwd, stdin=None):
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


class Cmd2(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)

    def onecmd(self, line):
        """Mostly ripped from Python's cmd.py"""
        cmd, arg, line = self.parseline(line)
        if arg:
            arg = shlex.split(arg)
        else:
            arg = []

        if not line:
            return self.emptyline()
        if cmd is None:
            return self.default(line)
        self.lastcmd = line
        if cmd == '':
            return self.default(line)
        else:
            try:
                func = getattr(self, 'do_' + cmd)
            except AttributeError:
                return self.default(line)
            try:
                return func(arg)
            except (SystemExit, KeyboardInterrupt):
                return False
            except Exception:
                logging.exception("%s failed" % (cmd))

    def cmdloop(self, intro=None):
        """Repeatedly issue a prompt, accept input, parse an initial prefix
        off the received input, and dispatch to action methods, passing them
        the remainder of the line as argument.

        """

        self.preloop()
        if self.use_rawinput and self.completekey:
            try:
                import readline
                self.old_completer = readline.get_completer()
                readline.set_completer(self.complete)
                readline.parse_and_bind(self.completekey + ": complete")
            except ImportError:
                pass
        try:
            if intro is not None:
                self.intro = intro
            if self.intro:
                self.stdout.write(str(self.intro) + "\n")
            stop = None
            while not stop:
                try:
                    if self.cmdqueue:
                        line = self.cmdqueue.pop(0)
                    else:
                        if self.use_rawinput:
                            try:
                                line = input(self.prompt)
                            except EOFError:
                                line = 'EOF'
                        else:
                            self.stdout.write(self.prompt)
                            self.stdout.flush()
                            line = self.stdin.readline()
                            if not len(line):
                                line = 'EOF'
                            else:
                                line = line.rstrip('\r\n')
                    line = self.precmd(line)
                    stop = self.onecmd(line)
                    stop = self.postcmd(stop, line)
                except KeyboardInterrupt:
                    print("\nUse `exit` or EOF (C-D) to exit")
            self.postloop()
        finally:
            if self.use_rawinput and self.completekey:
                try:
                    import readline
                    readline.set_completer(self.old_completer)
                except ImportError:
                    pass


class ManualJudge(Cmd2):
    """ɛMJ Command line"""

    def __init__(self):
        Cmd2.__init__(self)
        self.path = ""
        self.prompt = PROMPT % self.path

    def cwd(self):
        return os.path.join(ROOT, self.path)

    def update_prompt(self):
        self.prompt = PROMPT % self.path

    def do_help(self, arg):
        return cmd.Cmd.do_help(self, " ".join(arg))

    @arguments(
        ar(description='List submissions'),
        ar('type', help='which submissions to list'),
        ar('-t', '--team', help='filter by team'),
        ar('-p', '--problem', help='filter by problem')
    )
    def do_list(self, arg, opts, parser):
        judge.do_list(opts, parser)

    @arguments(
        ar(description='Checkout submission'),
        ar('id', help='which submissions to checkout')
    )
    def do_checkout(self, arg, opts, parser):
        submission_id = judge.do_checkout(opts, parser)
        self.path = submission_id
        self.update_prompt()

    @current
    @arguments(
        ar(description='Compile current submission')
    )
    def do_compile(self, arg, opts, parser):
        judge.do_current_compile(opts, parser, cwd=self.cwd())

    @current
    @arguments(
        ar(description='Execute current submission'),
        ar('test', nargs="?", default="", help="The test case to execute"),
        ar('-d', "--diff", const=True, nargs="?", help="diff")
    )
    def do_execute(self, arg, opts, parser):
        data = None
        if opts.test:
            path = os.path.join(self.cwd(), "tests", opts.test + ".in")
            if not os.path.isfile(path):
                print("Test %s does not exist, exiting." % opts.test)
                return False
            with open(path, 'r', encoding='utf-8') as f:
                data = f.read()
            val = execute(self.cwd(), test=True, data=data)
        else:
            val = execute(self.cwd())

        print("Return code %d." % val[0])
        if val[1].strip():
            print("stdout:\n%s" % val[1].strip())
        if val[2].strip():
            print("stderr:\n%s" % val[2].strip())

    def complete_execute(self, *arg):
        return [a for a in self.get_tests() if a.startswith(arg[0])]

    @current
    @arguments(
        ar(description='submit the current submission'),
        ar('verdict', help='the verdict  (see `verdicts` for explanations)', choices=judge.verdict_explanation.keys()),
        ar('-m', '--message', help='a message with the verdict')
    )
    def do_submit(self, arg, opts, parser):
        judge.do_current_submit(opts, parser, cwd=self.cwd())

    @current(error=False)
    def get_tests(self):
        files = [f[0:-3] for f in os.listdir(os.path.join(self.cwd(), "tests")) if f.endswith(".in")]
        # Fix this sorting shit
        files.sort(key=lambda s: (s.split("__")[0], getno(s)))
        return files

    @current
    def do_tests(self, arg):
        """Lists the available tests"""
        for f in self.get_tests():
            print(f)

    def do_verdicts(self, arg):
        """Lists the available verdicts"""
        print("\n".join("%s: %s" % (k, v) for k, v in judge.verdict_explanation.items()))

    def do_edit(self, arg):
        """Open file in $EDITOR"""
        call([EDITOR] + arg, cwd=self.cwd())

    def do_shell(self, arg):
        call(arg, cwd=self.cwd())

    def do_ls(self, arg):
        return self.do_shell(['ls'] + arg)

    def do_cat(self, arg):
        return self.do_shell(['cat'] + arg)

    def do_cd(self, arg):
        """Change working directory"""
        path = os.path.normpath(os.path.join(self.path, arg[0]))
        if path == ".":
            path = ""
        if not os.path.isdir(os.path.join(ROOT, path)):
            print("cd: no such file or directory: %s" % arg[0])
            return
        self.path = path
        self.update_prompt()

    def do_exit(self, arg):
        return True

    do_EOF = do_exit


def main(argv):
    parser = argparse.ArgumentParser(description='An automatic programming contest judge.')
    parser.add_argument('contest', help='the contest directory')
    opts = parser.parse_args(argv)

    judge.load_contest(opts.contest)
    try:
        ManualJudge().cmdloop()
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    main(sys.argv[1:])
