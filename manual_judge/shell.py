#!/usr/bin/env python3

import sys
import os
import argparse
import readline
import shlex
import logging
import cmd
import tempfile

from functools import wraps
from subprocess import call

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, BASE_DIR)
import judge

SUBMISSION_WAIT = 1000  # ms
EDITOR = os.environ.get('EDITOR', 'vim')  # that easy!
contest = None
ROOT = tempfile.mkdtemp(prefix="epsilon")
judge.CWD = ROOT

PROMPT = "ɛ %s > "


def current(func):
    @wraps(func)
    def validate(*args, **kwargs):
        if not os.path.isfile(os.path.join(args[0].cwd(), "submission.yaml")):
            print("Not in submission directory, exiting...")
            return False
        return func(*args, **kwargs)
    return validate


def ar(*args, **kwargs):
    return args, kwargs


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


class ManualJudge(cmd.Cmd):
    """ɛMJ Command line"""

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.path = ""
        self.prompt = PROMPT % self.path

    def onecmd(self, line):
        """Mostly ripped from Python's cmd.py"""
        cmd, arg, line = self.parseline(line)
        arg = shlex.split(arg)

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
        ar('test', nargs="?", default="")
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
        judge.do_current_execute(opts, parser, cwd=self.cwd(), data=data)

    @current
    @arguments(
        ar(description='submit the current submission'),
        ar('verdict', help='the verdict  (see `verdicts` for explanations)', choices=judge.verdict_explanation.keys()),
        ar('-m', '--message', help='a message with the verdict')
    )
    def do_submit(self, arg, opts, parser):
        judge.do_current_submit(opts, parser, cwd=self.cwd())

    def do_verdicts(self, arg):
        """Lists the available verdicts"""
        print("\n".join("%s: %s" % (k, v) for k, v in judge.verdict_explanation.items()))

    @current
    def do_tests(self, arg):
        """Lists the available tests"""
        files = [f[0:-3] for f in os.listdir(os.path.join(self.cwd(), "tests")) if f.endswith(".in")]
        # Fix this sorting shit
        files.sort(key=lambda s: (s.split("__")[0], int(s.split("__")[1].split(".")[0])))
        for f in files:
            print(f)

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

    def do_EOF(self, arg):
        return True


def main(argv):
    parser = argparse.ArgumentParser(description='An automatic programming contest judge.')
    parser.add_argument('contest', help='the contest directory')
    opts = parser.parse_args(argv)

    judge.load_contest(opts.contest)
    ManualJudge().cmdloop()

if __name__ == '__main__':
    main(sys.argv[1:])
