import time, datetime, yaml, argparse
import sys, os, shutil, difflib, signal
from subprocess import Popen, PIPE, TimeoutExpired

DIR = os.path.join(os.path.dirname(__file__), "..")
MAX_DIFF = 400

sys.path.append(DIR)
from config import CONFIG
import lib.judgelib as j
from lib.judgelib import *

def read_file(path):
    try:
        with open(path, 'r', encoding='utf8') as f:
            return f.read()
    except UnicodeDecodeError as e:
        with open(path, 'r', encoding='latin1') as f:
            return f.read()

def execute_submission(sub_id, sub_real_id, cpu, mem, nprocs, cmd):
    global USER_NO

    proc = Popen([ 'sudo', os.path.join(DIR, 'execute-submission.sh'),
            str(USER_NO),
            '%d:%d' % (os.getuid(), os.getgid()),
            str(sub_real_id),
            str(cpu // 1000),
            str(mem),
            str(nprocs),
            ' '.join(cmd) ],
        cwd=DIR)

    retcode = proc.wait()

    try:
        stdout = read_file(os.path.join(DIR, 'submissions', sub_id, 'out'))
        stderr = read_file(os.path.join(DIR, 'submissions', sub_id, 'err'))
        usage = read_file(os.path.join(DIR, 'submissions', sub_id, 'usage'))

        os.unlink(os.path.join(DIR, 'submissions', sub_id, 'out'))
        os.unlink(os.path.join(DIR, 'submissions', sub_id, 'err'))
        os.unlink(os.path.join(DIR, 'submissions', sub_id, 'usage'))
    except Exception as e:
        logger.exception(e)

        if stderr:
            logger.error('safeexec failed:')
            logger.error(stderr)
        else:
            logger.error('safeexec failed')

        # safeexec failed for whatever reason :(
        return 'SE', retcode, None, None, stdout, stderr

    logger.debug('usage:')
    logger.debug('\n' + usage)

    usage = usage.split('\n')

    retcode = 0
    if usage[0].startswith('Command exited with non-zero status'):
        retcode = int(usage[0].split('(')[1].split(')')[0])
        ver = 'RE'
    elif usage[0].startswith('Command terminated by signal'):
        retcode = int(usage[0].split('(')[1].split(':')[0])
        ver = 'RE'
    elif usage[0] == 'Memory Limit Exceeded':
        ver = 'ML'
    elif usage[0] == 'Time Limit Exceeded':
        ver = 'TL'
    elif usage[0] == 'Output Limit Exceeded':
        ver = 'OL'
    elif usage[0] == 'Invalid Function':
        ver = 'RF'
    elif usage[0] == 'Internal Error':
        ver = 'SE'
    elif usage[0] == 'OK':
        ver = 'OK'
    else:

        # Nooo, some verdict I don't know about
        ver = 'DNO'

        logger.error('safeexec returned an unknown status:')
        logger.error(usage)

    try:
        cpu = int(float(usage[3].split(': ')[1].split(' ')[0]) * 1000)
        mem = int(usage[2].split(': ')[1].split(' ')[0])
    except:
        cpu = None
        mem = None

    return ver, retcode, cpu, mem, stdout, stderr


def process_submission(sub, check, time_limit, memory_limit, language, tests):

    sub_id = USER + '_' + str(sub.id)
    sub_dir = os.path.join(DIR, 'submissions', sub_id)
    verdicts = []
    judge_response = ""

    if os.path.exists(sub_dir):
        shutil.rmtree(sub_dir)

    os.makedirs(sub_dir)

    with open(os.path.join(sub_dir, language['filename']), 'w') as f:
        f.write(sub.file)

    compiled = True
    if 'compile' in language:

        # TODO: timeout compilation
        proc = Popen(language['compile'],
                    stdin=PIPE,
                    stdout=PIPE,
                    stderr=PIPE,
                    cwd=sub_dir)

        res = proc.communicate()
        stdout = res[0].decode('utf-8')
        stderr = res[1].decode('utf-8')

        if proc.returncode == 0:
            logger.debug('compile successful')
        else:
            sub.judge_response = """<h4>Compile error</h4><p><pre><code>%s</code></pre></p>""" % ((stdout + '\n' + stderr).strip())
            logger.debug('compile error:\n' + stderr)
            compiled = False
            verdicts.append('CE')

    mxcpu = None
    mxmem = None
    if compiled:
        first_wa = True
        for test_no, test in enumerate(tests):
            logger.debug('running test %d' % test_no)

            with open(os.path.join(sub_dir, 'in'), 'w') as f:
                f.write(test.input)

            ver, retcode, cpu, mem, stdout, stderr = execute_submission(
                    sub_id=sub_id,
                    sub_real_id=sub.id,
                    cpu=time_limit,
                    mem=max(memory_limit, language.get('min_mem', 0)),
                    nprocs=language.get('nprocs', 0),
                    cmd=language['execute'])

            if ver == 'TL':
                logger.debug('time limit exceeded')
                judge_response += """<h4>Time limit exceeded on test %d</h4>""" % (test_no+1)
                verdicts.append('TL')
            elif ver == 'RE':
                verdicts.append('RE')
                judge_response += """<h4>Runtime error on test %d</h4><p><pre><code>%s</code></pre></p>""" % (test_no+1, stderr)
                logger.debug('runtime error:\n' + stderr)
            elif ver == 'ML':
                logger.debug('memory limit exceeded')
                judge_response += """<h4>Memory limit exceeded on test %d</h4>""" % (test_no+1)
                verdicts.append('ML')
            elif ver == 'OL':
                logger.debug('output limit exceeded')
                judge_response += """<h4>Output limit exceeded on test %d</h4>""" % (test_no+1)
                verdicts.append('OL')
            elif ver == 'RF':
                logger.debug('restricted function')
                judge_response += """<h4>Restricted function on test %d</h4>""" % (test_no+1)
                verdicts.append('RF')
            elif ver == 'SE':
                logger.debug('submission error')
                judge_response += """<h4>Submission error on test %d</h4>""" % (test_no+1)
                verdicts.append('SE')
            elif ver == 'OK':

                try:
                    ok = check(expected=test.output, obtained=stdout)
                except Exception as e:
                    ok = False
                    logger.warning('exception occured in checker, treating as WA')
                    logger.exception(e)

                if ok:
                    verdicts.append('AC')
                    judge_response += """<h4>Accepted on test %d</h4>""" % (test_no+1)
                    logger.debug('accepted')
                else:
                    verdicts.append('WA')
                    logger.debug('wrong answer')

                    judge_response += """<h4>Wrong answer on test %d</h4>""" % (test_no+1)

                    if first_wa:
                        first_wa = False

                        if DISPLAY_INPUT:
                            judge_response += """<h5>Input</h5><pre>%s</pre>""" % test.input.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

                        if DISPLAY_DIFF:
                            judge_response += """<h5>Output</h5>"""

                            linesa = stdout.split('\n')
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

            if ver in {'TL','RE','ML','OL','OK'}:
                if cpu is not None and (mxcpu is None or cpu > mxcpu): mxcpu = cpu
                if mem is not None and (mxmem is None or mem > mxmem): mxmem = mem

            # TODO: make this optional (stop after first non-AC test case)
            if verdicts[-1] != 'AC':
                break

        if judge_response:
            sub.judge_response = judge_response

    shutil.rmtree(sub_dir)
    return (verdicts, mxcpu, mxmem)


def main(argv):

    parser = argparse.ArgumentParser(description='An automatic programming contest judge.')

    parser.add_argument('config', help='the contest judge config file')
    parser.add_argument('user', default=1, type=int, help='the number of the judge user to use')

    opts = parser.parse_args(argv)

    with open(opts.config, 'r') as f:
        config = yaml.load(f)

    global DISPLAY_DIFF, DISPLAY_INPUT, USER, USER_NO
    j.BALLOONS = config.get('balloons', False)
    j.TESTS_DIR = os.path.abspath(config['tests_dir'])
    j.DB_CONN_STRING = config['db_conn_string']
    DISPLAY_DIFF = config.get('display_diff', False)
    DISPLAY_INPUT = config.get('display_input', False)
    USER = CONFIG['JUDGE_USER_PREFIX'] + '-' + str(opts.user)
    USER_NO = str(opts.user)

    j.set_contest_id(config['contest_id'])
    j.start(process_submission)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

