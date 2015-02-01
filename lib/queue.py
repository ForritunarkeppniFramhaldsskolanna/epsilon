import sys
import os
import time
import random
import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.models import OperationalError, Submission, SubmissionQueue
import lib.models as models
SUBMISSION_WAIT = 1000  # ms

logger = None


def dequeue(sess):
    result = sess.execute("""
        SELECT submission_id, status, dequeued_at FROM \"%s\"
        WHERE status=0
              AND pg_try_advisory_xact_lock(submission_id)
        ORDER BY submission_id asc
        LIMIT 1
        FOR UPDATE
        """ % (SubmissionQueue.__tablename__))

    sub = result.first()
    if sub is None:
        sess.commit()
        return None

    sub = SubmissionQueue(sub.submission_id, sub.status, sub.dequeued_at)
    sess.merge(sub)
    sub.status = 1
    sub.dequeued_at = datetime.datetime.now()
    # sess.query(SubmissionQueue).filter(SubmissionQueue.submission_id == sub.submission_id).update({"status": 1, "dequeued_at": datetime.datetime.now()})
    sess.commit()
    return sub


def submissions(conn_string, limit=0):
    processed_submissions = 0
    while True:
        try:
            db = models.get_db(conn_string)
            while True:
                sess = db()
                try:
                    qsub = dequeue(sess)
                    if qsub is None:
                        continue
                    sub = sess.query(Submission).filter_by(id=qsub.submission_id).one()
                    yield sub, sess
                    sess.query(SubmissionQueue).filter(SubmissionQueue.submission_id == qsub.submission_id).delete()
                    sess.commit()
                    processed_submissions += 1
                    if limit != 0 and processed_submissions >= limit:
                        return
                    time.sleep(SUBMISSION_WAIT / 1000.0 + random.random())
                finally:
                    sess.close()

        except OperationalError as e:
            if logger:
                logger.exception(e)
                logger.debug('I probably can\'t connect to db...')
            time.sleep(60)  # wait for a minute
        except Exception as e:
            if logger:
                logger.exception(e)
            time.sleep(SUBMISSION_WAIT / 1000.0 + random.random())
