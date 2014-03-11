import yaml, datetime, imp, time, os, random
from sqlalchemy import create_engine, or_, Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from os.path import join as pjoin
import logging

BALLOONS = True
TESTS_DIR = ''
LANGUAGES_FILE = os.path.join('__EPSILON_PREFIX__', 'config/languages.yml')
DB_CONN_STRING = ''
SUBMISSION_WAIT = 1000 # ms
SUBMISSION_JUDGE_TIMEOUT = 3 * 60 * 1000 # ms
PROCESS_SUBMISSION = None
PROCESS_TEST = None

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

def read(p):
    with open(p, 'r') as f:
        return f.read()

def load(p):
    with open(p, 'r') as f:
        return yaml.load(f)

def eq_check(expected, obtained):
    return expected == obtained

Base = declarative_base()
class Submission(Base):
    __tablename__ = 'Submission'
    id = Column(Integer, primary_key=True)
    team = Column(String(200), nullable=False)
    problem = Column(String(200), nullable=False)
    language = Column(String(200), nullable=False)
    file = Column(Text(), nullable=False)
    submitted = Column(DateTime(), nullable=False)
    verdict = Column(String(20), default='QU', nullable=False)
    judge_response = Column(Text())

    time = Column(Integer) # ms
    memory = Column(Integer) # bytes

    def __init__(self, team, problem, language, file, submitted=None, verdict='QU'):
        self.team = team
        self.problem = problem
        self.language = language
        self.file = file
        if submitted is None:
            self.submitted = datetime.datetime.now()
        else:
            self.submitted = submitted
        self.verdict = verdict

class SubmissionQueue(Base):
    __tablename__ = 'SubmissionQueue'
    submission_id = Column(Integer, ForeignKey('Submission.id'), primary_key=True)
    last_announce = Column(DateTime)

    def __init__(self, submission_id, last_announce=None):
        self.submission_id = submission_id
        self.last_announce = last_announce

class Balloon(Base):
    __tablename__ = 'Balloon'
    balloon_id = Column(Integer, primary_key=True)
    team = Column(String(200), nullable=False)
    problem = Column(String(200), nullable=False)
    delivered = Column(Boolean, default=False, nullable=False)

    def __init__(self, team, problem):
        self.team = team
        self.problem = problem

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
    cur_tests_dir = pjoin(TESTS_DIR, sub.problem)
    tests = []
    for t in sorted(os.listdir(cur_tests_dir)):
        if not t.endswith('.in'): continue
        input = read(pjoin(cur_tests_dir, t))
        expected = pjoin(cur_tests_dir, t[:-2] + 'out')
        expected = read(expected) if os.path.exists(expected) else None
        tests.append(Test(input, expected))
    return tests

def get_db():
    db_engine = create_engine(DB_CONN_STRING, convert_unicode=True)
    db = sessionmaker(bind=db_engine)
    return db

def deliver_balloon(sess, team, problem):
    if BALLOONS:
        balloon = sess.query(Balloon).filter_by(team=team, problem=problem).first()
        if not balloon:
            balloon = Balloon(team, problem)
            sess.add(balloon)

def start(process_submission):
    logger.debug('started')
    langs = load(LANGUAGES_FILE)

    while True:
        try:
            db = get_db()

            while True:
                sess = db()
                try:
                    time.sleep(SUBMISSION_WAIT / 1000.0 + random.random())
                    get_before = datetime.datetime.now() - datetime.timedelta(0, SUBMISSION_JUDGE_TIMEOUT / 1000.0)
                    # TODO: do something smarter for concurrency
                    qsub = sess.query(SubmissionQueue).filter(or_(SubmissionQueue.last_announce == None, SubmissionQueue.last_announce < get_before)).first()
                    if not qsub:
                        continue

                    qsub.last_announce = datetime.datetime.now()
                    sess.commit()
                    sub = sess.query(Submission).filter_by(id=qsub.submission_id).one()

                    logger.debug('-------------')
                    logger.debug('got submission %d' % sub.id)
                    logger.debug('team = %s' % sub.team)
                    logger.debug('problem = %s' % sub.problem)
                    logger.debug('language = %s' % sub.language)

                    cur_tests_dir = pjoin(TESTS_DIR, sub.problem)
                    cur_config = load(pjoin(cur_tests_dir, 'tests.yml'))
                    check = eq_check
                    if 'checker' in cur_config:
                        p = pjoin(cur_tests_dir, cur_config['checker'])
                        with open(p) as f:
                            check = imp.load_source('checker', p, f).check

                    lang = langs[sub.language]

                    try:
                        res, cpu, mem = process_submission(
                            sub=sub,
                            check=check,
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
                    except Exception as e:
                        logger.error('failed to judge submission %d' % sub.id)
                        logger.exception(e)
                        sub.verdict = 'SE'

                    if sub.verdict == 'AC':
                        deliver_balloon(sess, sub.team, sub.problem)

                    logger.debug('verdict = %s' % sub.verdict)
                    logger.debug('-------------')
                    sess.delete(qsub)
                    sess.commit()

                finally:
                    sess.close()
        except OperationalError as e:
            logger.exception(e)
            logger.debug('I probably can\'t connect to db...')
            time.sleep(60) # wait for a minute
        except Exception as e:
            logger.exception(e)
            time.sleep(SUBMISSION_WAIT / 1000.0 + random.random())

def get_all_submissions():
    db_engine = create_engine(DB_CONN_STRING, convert_unicode=True)
    db = sessionmaker(bind=db_engine)
    sess = db()
    try:
        return sess.query(Submission).all()
    finally:
        sess.close()

def set_contest_id(contest_id):
    for table in Base.metadata.tables.values():
        table.name = '%s_%s' % (contest_id, table.name)

