# from flask.ext.sqlalchemy import SQLAlchemy
# db = SQLAlchemy()
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError


Base = declarative_base()


class Submission(Base):
    __tablename__ = 'Submission'
    id = Column(Integer, primary_key=True)
    team = Column(String(200), nullable=False)
    problem = Column(String(200), nullable=False)
    language = Column(String(200), nullable=False)
    file = Column(Text(), nullable=False)
    # submitted = Column(Float(), nullable=False) 
    submitted = Column(DateTime(), nullable=False)
    verdict = Column(String(20), default='QU', nullable=False)
    judge_response = Column(Text())

    time = Column(Integer)  # ms
    memory = Column(Integer)  # bytes

    def __init__(self, team, problem, language, file, submitted=None, verdict='QU', judge_response=None):
        self.team = team
        self.problem = problem
        self.language = language
        self.file = file
        if submitted is None:
            self.submitted = datetime.datetime.now()
        else:
            self.submitted = submitted
        self.verdict = verdict
        self.judge_response = judge_response


class SubmissionQueue(Base):
    __tablename__ = 'SubmissionQueue'
    submission_id = Column(Integer, ForeignKey('Submission.id'), primary_key=True)
    status = Column(Integer, default=0, nullable=False)
    dequeued_at = Column(DateTime)

    def __init__(self, submission_id, status=0, dequeued_at=None):
        self.submission_id = submission_id
        self.satus = status
        self.dequeued_at = dequeued_at


class Balloon(Base):
    __tablename__ = 'Balloon'
    balloon_id = Column(Integer, primary_key=True)
    submission_id = Column(Integer, ForeignKey('Submission.id'), primary_key=True)
    # team = Column(String(200), nullable=False)
    # problem = Column(String(200), nullable=False)
    delivered = Column(Boolean, default=False, nullable=False)

    def __init__(self, submission_id):
        self.submission_id = submission_id


def get_db(conn_string):
    db_engine = create_engine(conn_string, convert_unicode=True)
    db = sessionmaker(bind=db_engine)
    return db


def set_contest_id(contest_id):
    for table in Base.metadata.tables.values():
        table.name = '%s_%s' % (contest_id, table.name)
    for c in Base._decl_class_registry.values():
        if hasattr(c, '__tablename__'):
            c.__tablename__ = "%s_%s" % (contest_id, c.__tablename__)


def register_base(db):
    db.Model = Base
    for c in Base._decl_class_registry.values():
        # Add the query class to each of the models.
        c.query = db.session.query_property()
