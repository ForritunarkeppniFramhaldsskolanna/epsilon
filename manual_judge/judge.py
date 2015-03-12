import sys
import os
import argparse
import builtins

import shell
import sh
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, BASE_DIR)

SUBMISSION_WAIT = 1000  # ms
contest = None
CWD = os.getcwd()


def do_help(opts, parser):
    if opts.item == "verdicts":
        print("\n".join("%s: %s" % (k, v) for k, v in shell.verdict_explanation.items()))


def main(argv):
    parser = argparse.ArgumentParser(description='A command line judge interface.')
    parser.add_argument('contest', help='contest')
    parser.add_argument("command", nargs=argparse.REMAINDER)

    opts = parser.parse_args(argv)

    sh.shell.load_contest(opts.contest)

    builtins.aliases = {}
    sh.setup_aliases()
    builtins.aliases["list"] = builtins.aliases["subs"]
    if opts.command:
        try:
            builtins.aliases[opts.command[0]](opts.command[1:])
        except KeyboardInterrupt:
            pass
        except KeyError:
            print("Invalid command! The available commands are (%s)" % (", ".join(builtins.aliases.keys())))
        except IndexError:
            print("Missing arguments")


if __name__ == '__main__':
    main(sys.argv[1:])
