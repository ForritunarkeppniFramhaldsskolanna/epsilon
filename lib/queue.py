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


class Submissions:
    def __init__(self, conn_string):
        self._conn_string = conn_string
        self._sess = None
        self._qsub = None
        self._db = None
        self.stopped = False
        self._checked_out = False
        self._connect_db()

    def __enter__(self):
        return self

    def __exit__(self, exc_t, exc_v, traceback):
        if exc_t:  # If this was the result of an unhandled exception, consider the submission as not processed
            self.cancel()
        else:
            self._pop()
            self._cleanup()

    def __del__(self):
        self._cleanup()

    def _connect_db(self):
        while True:
            try:
                self._db, self._db_engine = models.get_db(self._conn_string, engine=True)
                break
            except OperationalError as e:
                if logger:
                    logger.exception(e)
                    logger.debug('I probably can\'t connect to db...')
                time.sleep(60)  # wait for a minute

    def get_session(self):
        return self._sess

    def commit(self):
        self._sess.commit()

    def cancel(self):
        self._requeue()
        self._cleanup()

    def stop(self):
        self._cleanup()
        self.stopped = True

    def _cleanup(self):
        if self._sess:
            self._sess.close()

        self._sess = None
        self._qsub = None

    def _requeue(self):
        if self._qsub and self._sess:
            self._qsub.status = 0
            self._qsub.dequeued_at = None
            self._sess.commit()
            self._qsub = None

    def _pop(self):
        if self._qsub and self._sess:
            self._sess.delete(self._qsub)
            self._sess.commit()

    def _dequeue(self):
        if self._sess is None:
            return None
        result = self._sess.execute("""
            SELECT submission_id, status, dequeued_at FROM \"%s\"
            WHERE (status=0 OR dequeued_at < current_timestamp - interval '%s')
                  AND pg_try_advisory_xact_lock(submission_id)
            ORDER BY submission_id asc
            LIMIT 1
            FOR UPDATE
            """ % (SubmissionQueue.__tablename__, "10 minutes"))  # For safe measure, also check out submissions checked out over 10 minutes ago

        qsub = result.first()
        if qsub is None:
            self._sess.commit()
            self._qsub = None
            return

        # Another query to attach it to the session, so its easy to work with the object
        self._qsub = self._sess.query(SubmissionQueue).filter(SubmissionQueue.submission_id == qsub.submission_id).one()
        self._qsub.status = 1
        self._qsub.dequeued_at = datetime.datetime.now()
        self._sess.commit()

    def __iter__(self):
        return self

    def __next__(self):
        if self.stopped:
            raise StopIteration
        # Clean up the previous states
        self._pop()
        self._cleanup()

        # Pop a new one
        while True:
            try:
                self._sess = self._db()
                self._dequeue()
                if self._qsub is None:
                    self._cleanup()
                    time.sleep(SUBMISSION_WAIT / 1000.0 + random.random())
                    continue

                self._sub = self._sess.query(Submission).filter_by(id=self._qsub.submission_id).one()

                return self._sub
            except OperationalError:
                self._cleanup()
                self._connect_db()
            except Exception as e:
                if logger:
                    logger.exception(e)
                if self._qsub:
                    self._requeue()
                self._cleanup()
                time.sleep(SUBMISSION_WAIT / 1000.0 + random.random())
