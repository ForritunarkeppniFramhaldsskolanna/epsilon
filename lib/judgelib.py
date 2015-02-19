import imp
import os
from os.path import join as pjoin
import logging
from lib.yamllib import load
from lib.models import Submission, Balloon, get_db, set_contest_id
from lib.queue import Submissions
import lib.queue

BALLOONS = True
CONTEST_DIR = None
LANGUAGES_FILE = os.path.join(os.path.dirname(__file__), "..", 'config/languages.yml')
DB_CONN_STRING = ''
SUBMISSION_JUDGE_TIMEOUT = 3 * 60 * 1000  # ms
PROCESS_SUBMISSION = None
PROCESS_TEST = None
DISPLAY_DIFF = False
DISPLAY_INPUT = False

VERDICTS = [
    ('AC', 0),
    ('PE', 1),
    ('WA', 2), ('RE', 2), ('TL', 2), ('ML', 2), ('OL', 2),
    ('CE', 3),
    ('SE', 4),
    ('RF', 5),
    ('CJ', 6),
]

_verdicts_map = dict(VERDICTS)

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s, %(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

lib.queue.logger = logger


def read(path):
    try:
        with open(path, 'r', encoding='utf8') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(path, 'r', encoding='latin1') as f:
            return f.read()

# def load(p):
#     with open(p, 'r') as f:
#         return yaml.load(f)


def load_contest(path):
    config = load(os.path.join(path, 'contest.yml'))

    global BALLOONS, CONTEST_DIR, DB_CONN_STRING, DISPLAY_DIFF, DISPLAY_INPUT
    CONTEST_DIR = path
    BALLOONS = config.get('balloons', False)
    DB_CONN_STRING = config['db']
    DISPLAY_DIFF = config.get('display_diff', False)
    DISPLAY_INPUT = config.get('display_input', False)

    set_contest_id(config['id'])

def eq_check(expected, obtained):
    expected = [line.strip() for line in expected.split('\n') if line.strip()]
    obtained = [line.strip() for line in obtained.split('\n') if line.strip()]
    return expected == obtained


class Test:
    def __init__(self, input, output):
        self.input = input
        self.output = output


def compute_verdict(verdicts):
    res = []
    no = 0
    for v in verdicts:
        if _verdicts_map[v] > no:
            no = _verdicts_map[v]
            res = []
        if _verdicts_map[v] == no:
            res.append(v)
    return '+'.join(sorted(set(res)))


def get_tests(sub):
    cur_tests_dir = pjoin(CONTEST_DIR, 'problems', sub.problem, 'tests')
    if not os.path.isdir(cur_tests_dir):
        cur_tests_dir = pjoin(CONTEST_DIR, 'problems', sub.problem, '.epsilon', 'tests')

    tests = []
    for t in sorted(os.listdir(cur_tests_dir)):
        if not t.endswith('.in'):
            continue
        input = read(pjoin(cur_tests_dir, t))
        expected = pjoin(cur_tests_dir, t[:-2] + 'out')
        expected = read(expected) if os.path.exists(expected) else None
        tests.append(Test(input, expected))
    return tests


def deliver_balloon(sess, sub):
    if BALLOONS:
        # logger.debug('checking if balloon already exists')
        balloon = sess.query(Balloon, Submission).filter(Balloon.submission_id == Submission.id, Submission.team == sub.team, Submission.problem == sub.problem).first()
        if not balloon:
            # logger.debug('creating balloon')
            balloon = Balloon(sub.id)
            sess.add(balloon)
            sess.commit()
        # else:
        #     logger.debug('balloon alread exists')
    # else:
    #     logger.debug('balloon delivery turned off')


def start(process_submission):
    logger.debug('started')
    langs = load(LANGUAGES_FILE)
    with Submissions(DB_CONN_STRING) as queue:
        for sub in queue:
            logger.debug('-------------')
            logger.debug('got submission %d' % sub.id)
            logger.debug('team = %s' % sub.team)
            logger.debug('problem = %s' % sub.problem)
            logger.debug('language = %s' % sub.language)
            cur_tests_dir = pjoin(CONTEST_DIR, 'problems', sub.problem, 'tests')
            if not os.path.isdir(cur_tests_dir):
                cur_tests_dir = pjoin(CONTEST_DIR, 'problems', sub.problem, '.epsilon', 'tests')

            cur_config = load(pjoin(cur_tests_dir, 'tests.yml'))
            checker = eq_check
            if 'checker' in cur_config:
                checker = pjoin(cur_tests_dir, cur_config['checker'])

            lang = langs[sub.language]

            try:
                res, cpu, mem = process_submission(
                    sub=sub,
                    checker=checker,
                    checker_options=cur_config.get('checker_options'),
                    time_limit=int(cur_config['time_limit']),
                    memory_limit=int(cur_config['memory_limit']),
                    language=lang,
                    tests=get_tests(sub),
                )

                if isinstance(res, list):
                    res = compute_verdict(res)

                sub.verdict = res
                sub.time = cpu
                sub.memory = mem
                queue.commit()
            except Exception as e:
                logger.error('failed to judge submission %d' % sub.id)
                logger.exception(e)
                sub.verdict = 'SE'
                queue.commit()
            if sub.verdict == 'AC':
                deliver_balloon(queue.get_session(), sub)
            logger.debug('verdict = %s' % sub.verdict)
            logger.debug('-------------')


def get_all_submissions():
    db = get_db(DB_CONN_STRING)
    sess = db()
    try:
        return sess.query(Submission).all()
    finally:
        sess.close()
