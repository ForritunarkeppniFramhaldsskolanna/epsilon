import argparse
import sys
import os
import shutil
import difflib
import tempfile
from subprocess import Popen, PIPE, TimeoutExpired
from cgi import escape

DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.abspath(os.path.join(DIR, '..'))
MAX_DIFF = 400

sys.path.insert(0, BASE_DIR)

from config.config import CONFIG
import lib.judgelib as j
from lib.judgelib import logger
from jail import Jail

USER_NO = None
USER = None
DISPLAY_DIFF = None
DISPLAY_INPUT = None


def process_submission(sub, checker, checker_options, time_limit, memory_limit, language, tests):
    assert USER_NO is not None

    jail = Jail(USER_NO)
    try:
        jail.init()
        sub_dir = jail.box_dir

        verdicts = []
        judge_response = ""

        with open(os.path.join(sub_dir, language['filename']), 'w') as f:
            f.write(sub.file)

        compiled = True
        if 'compile' in language:

            res = jail.run(language['compile'], timelim=60, processes=100)

            if res['status'] == 'OK':
                logger.debug('compile successful')
            else:
                sub.judge_response = """<h4>Compile error</h4><p><pre><code>%s</code></pre></p>""" % ((escape(res.get('stdout', '')) + '\n' + escape(res.get('stderr', ''))).strip())
                logger.debug('compile error:\n' + res.get('stderr', ''))
                if 'message' in res:
                    logger.debug('message: %s\n' % res['message'])
                compiled = False
                verdicts.append('CE')

        mxcpu = None
        mxmem = None
        if compiled:
            first_wa = True
            for test_no, test in enumerate(tests):
                logger.debug('running test %d' % test_no)

                # with open(os.path.join(sub_dir, 'in'), 'w') as f:
                #     f.write(test.input)

                res = jail.run(language['execute'],
                               timelim=time_limit / 1000.0,
                               memlim=max(memory_limit, language.get('min_mem', 0)),
                               processes=language.get('nprocs', 1),
                               stdin=test.input)

                if res['status'] == 'TO':
                    logger.debug('time limit exceeded')
                    judge_response += """<h4>Time limit exceeded on test %d</h4>""" % (test_no + 1)
                    verdicts.append('TL')
                elif res['status'] in {'RE', 'SG'}:
                    verdicts.append('RE')
                    judge_response += """<h4>Runtime error on test %d</h4><p><pre><code>%s</code></pre></p>""" % (test_no + 1, escape(res.get('stderr', '')))
                    logger.debug('runtime error:\n' + res.get('stderr', ''))
                    if 'message' in res:
                        logger.debug('message: %s\n' % res['message'])
                elif res['status'] == 'ML':
                    logger.debug('memory limit exceeded')
                    judge_response += """<h4>Memory limit exceeded on test %d</h4>""" % (test_no + 1)
                    verdicts.append('ML')
                # elif ver == 'OL':
                #     logger.debug('output limit exceeded')
                #     judge_response += """<h4>Output limit exceeded on test %d</h4>""" % (test_no + 1)
                #     verdicts.append('OL')
                # elif ver == 'RF':
                #     logger.debug('restricted function')
                #     judge_response += """<h4>Restricted function on test %d</h4>""" % (test_no + 1)
                #     verdicts.append('RF')
                # elif ver == 'SE':
                #     logger.debug('submission error')
                #     judge_response += """<h4>Submission error on test %d</h4>""" % (test_no + 1)
                #     verdicts.append('SE')
                elif res['status'] == 'OK':

                    try:
                        if type(checker) is str:

                            tmp_dir = tempfile.mkdtemp(prefix='epsilon')
                            judge_in = os.path.join(tmp_dir, 'judge_in')
                            judge_ans = os.path.join(tmp_dir, 'judge_ans')
                            with open(judge_in, 'w') as f: f.write(test.input)
                            with open(judge_ans, 'w') as f: f.write(test.output)

                            # TODO: maybe run checker inside jail?
                            proc = Popen([checker, judge_in, judge_ans, tmp_dir] + (checker_options if checker_options else []), stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=os.path.dirname(checker))
                            proc.communicate(res['stdout'].encode('utf-8'))
                            ok = proc.returncode == 42
                            shutil.rmtree(tmp_dir)
                        else:
                            ok = check(expected=test.output, obtained=res['stdout'])
                    except Exception as e:
                        ok = False
                        logger.warning('exception occured in checker, treating as WA')
                        logger.exception(e)

                    if ok:
                        verdicts.append('AC')
                        judge_response += """<h4>Accepted on test %d</h4>""" % (test_no + 1)
                        logger.debug('accepted')
                    else:
                        verdicts.append('WA')
                        logger.debug('wrong answer')

                        judge_response += """<h4>Wrong answer on test %d</h4>""" % (test_no + 1)

                        if first_wa:
                            first_wa = False

                            if DISPLAY_INPUT:
                                judge_response += """<h5>Input</h5><pre>%s</pre>""" % escape(test.input)

                            if DISPLAY_DIFF:
                                judge_response += """<h5>Output</h5>"""

                                linesa = res['stdout'].split('\n')
                                linesb = test.output.split('\n')
                                trunc = False
                                if len(linesa) > MAX_DIFF or len(linesb) > MAX_DIFF:
                                    trunc = True
                                    linesa = linesa[:MAX_DIFF]
                                    linesb = linesb[:MAX_DIFF]

                                judge_response += difflib.HtmlDiff(tabsize=4).make_table(
                                    linesa,
                                    linesb,
                                    'Obtained',
                                    'Expected')

                                if trunc:
                                    judge_response += "<p>Note that the output was truncated.</p>"

                else:
                    # Nooo, some verdict I don't know about
                    logger.debug('unknown verdict')
                    verdicts.append('SE')
                    if 'message' in res:
                        logger.debug('message: %s\n' % res['message'])

                if verdicts[-1] == 'TL':
                    res['time'] = str(time_limit / 1000.0)
                if verdicts[-1] == 'ML':
                    res['mem'] = str(memory_limit)

                if 'time' in res and (mxcpu is None or float(res['time']) > mxcpu):
                    mxcpu = float(res['time'])
                if 'cg-mem' in res and (mxmem is None or float(res['cg-mem']) > mxmem):
                    mxmem = float(res['cg-mem'])

                # TODO: make this optional (stop after first non-AC test case)
                if verdicts[-1] != 'AC':
                    break

            if judge_response:
                sub.judge_response = judge_response

        if mxcpu is not None:
            mxcpu *= 1000.0

        return (verdicts, mxcpu, mxmem)
    finally:
        jail.cleanup()


def main(argv):

    parser = argparse.ArgumentParser(description='An automatic programming contest judge.')

    parser.add_argument('contest', help='the contest directory')
    parser.add_argument('user', default=1, type=int, help='the number of the judge user to use')

    opts = parser.parse_args(argv)

    global USER, USER_NO
    USER = CONFIG['JUDGE_USER_PREFIX'] + '-' + str(opts.user)
    USER_NO = str(opts.user)

    j.load_contest(opts.contest)

    try:
        j.start(process_submission)
    except KeyboardInterrupt:
        print("Shutting down...")
        pass
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
