#!/usr/bin/env python3

import sys
import os
import argparse
import datetime
import shutil
import readline
import shlex
import logging
import cmd
import tempfile
from subprocess import Popen, PIPE, call

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, BASE_DIR)
import judge

SUBMISSION_WAIT = 1000  # ms
EDITOR = os.environ.get('EDITOR', 'vim')  #that easy!
contest = None
ROOT = tempfile.mkdtemp(prefix="epsilon")
judge.CWD = ROOT


class ManualJudge(cmd.Cmd):
    """ɛMJ Command line"""
    prompt = "ɛ > "

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.cwd = ROOT

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
            except SystemExit:
                return False
            except KeyboardInterrupt:
                pass
            except Exception:
                logging.exception("%s failed" % (cmd))

    def do_help(self, arg):
        return cmd.Cmd.do_help(self, " ".join(arg))

    def do_list(self, arg):
        """
        usage: list [-h] [-t TEAM] [-p PROBLEM] type

        List submissions

        positional arguments:
          type                  which submissions to list

        optional arguments:
          -h, --help            show this help message and exit
          -t TEAM, --team TEAM  filter by team
          -p PROBLEM, --problem PROBLEM
                                filter by problem"""
        parser = argparse.ArgumentParser(prog="list", description='List submissions')
        parser.add_argument('type', help='which submissions to list')
        parser.add_argument('-t', '--team', help='filter by team')
        parser.add_argument('-p', '--problem', help='filter by problem')
        opts = parser.parse_args(arg)
        judge.do_list(opts, parser)

    def do_checkout(self, arg):
        """
        usage: checkout [-h] id

        Checkout submission

        positional arguments:
          id          which submissions to checkout

        optional arguments:
          -h, --help  show this help message and exit
        """
        parser = argparse.ArgumentParser(prog="checkout", description='Checkout submission')
        parser.add_argument('id', help='which submissions to checkout')
        opts = parser.parse_args(arg)
        self.cwd = judge.do_checkout(opts, parser)

    def do_compile(self, arg):
        """
        usage: compile [-h]

        Compile current submission

        optional arguments:
          -h, --help  show this help message and exit
        """
        if not os.path.isfile(os.path.join(self.cwd, "submission.yaml")):
            print("Not in submission directory, exiting...")
            return False
        parser = argparse.ArgumentParser(prog="compile", description='Compile current submission')
        opts = parser.parse_args(arg)
        judge.do_current_compile(opts, parser, cwd=self.cwd)

    def do_execute(self, arg):
        """
        usage: execute [-h]

        Execute current submission

        optional arguments:
          -h, --help  show this help message and exit
        """
        if not os.path.isfile(os.path.join(self.cwd, "submission.yaml")):
            print("Not in submission directory, exiting...")
            return False
        parser = argparse.ArgumentParser(prog="execute", description='Execute current submission')
        opts = parser.parse_args(arg)
        judge.do_current_execute(opts, parser, cwd=self.cwd)

    def do_submit(self, arg):
        if not os.path.isfile(os.path.join(self.cwd, "submission.yaml")):
            print("Not in submission directory, exiting...")
            return False
        parser = argparse.ArgumentParser(prog="submit", description='submit the current submission')
        parser.add_argument('verdict', help='the verdict  (see `verdicts` for explanations)', choices=judge.verdict_explanation.keys())
        parser.add_argument('-m', '--message', help='a message with the verdict')
        opts = parser.parse_args(arg)
        judge.do_current_submit(opts, parser, cwd=self.cwd)

    def do_verdicts(self, arg):
        print("\n".join("%s: %s" % (k, v) for k, v in judge.verdict_explanation.items()))

    def do_edit(self, arg):
        """Open file in $EDITOR"""
        call([EDITOR] + arg, cwd=self.cwd)

    def do_shell(self, arg):
        call(arg, cwd=self.cwd)

    def do_cd(self, arg):
        """Change working directory"""
        cwd = os.path.abspath(os.path.join(self.cwd, arg[0]))
        if cwd.startswith(ROOT):
            self.cwd = cwd
        else:
            self.cwd = ROOT

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
