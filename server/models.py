from flask.ext.sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()

class Submission(db.Model):
    __tablename__ = 'Submission'
    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(200), nullable=False)
    problem = db.Column(db.String(200), nullable=False)
    language = db.Column(db.String(200), nullable=False)
    file = db.Column(db.Text(), nullable=False)
    submitted = db.Column(db.Float(), nullable=False)
    verdict = db.Column(db.String(20), default='QU', nullable=False)
    judge_response = db.Column(db.Text())

    time = db.Column(db.Integer) # ms
    memory = db.Column(db.Integer) # bytes

    def __init__(self, team, problem, language, file, submitted, verdict='QU', judge_response=None):
        self.team = team
        self.problem = problem
        self.language = language
        self.file = file
        self.submitted = submitted
        self.verdict = verdict
        self.judge_response = judge_response

class SubmissionQueue(db.Model):
    __tablename__ = 'SubmissionQueue'
    submission_id = db.Column(db.Integer, db.ForeignKey('Submission.id'), primary_key=True)
    last_announce = db.Column(db.DateTime)

    def __init__(self, submission_id, last_announce=None):
        self.submission_id = submission_id
        self.last_announce = last_announce

class Balloon(db.Model):
    __tablename__ = 'Balloon'
    balloon_id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(200), nullable=False)
    problem = db.Column(db.String(200), nullable=False)
    delivered = db.Column(db.Boolean, default=False, nullable=False)

