import os
import sys
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, BASE_DIR)

import argparse
import time
from flask import Flask, g, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from server.data import Contest
import lib.models as models
from server.util import context_processor

from server.routes.default import default
from server.routes.judge import judge


# REDIRECT_SUB = re.compile('^http://localhost(:[0-9]+)?')
# REDIRECT_SUB_FOR = 'http://localhost/fk_2013_beta'

# class MyFlask(Flask):
#     def process_response(self, response):
#         global opts
#         if opts.prefix is not None and opts.hostname is not None and response.status_code == 301:
#             response.headers['Location'] = re.sub(REDIRECT_SUB, 'http://' + opts.hostname + opts.prefix, response.headers['Location'])
#         return response

# app = MyFlask(__name__)
app = Flask(__name__)
app.secret_key = "V=7Km+XXkg:}>4dT0('cV>Rp1TG82QEjah+X'v;^w:)a']y)^%"
db = app.db = SQLAlchemy(app)
models.register_base(db)


opts = app.opts = None
contest = app.contest = None


app.context_processor(context_processor)


app.register_blueprint(default)
app.register_blueprint(judge, url_prefix="/judge")


@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: time.time() - g.request_start_time


@app.template_filter('format_time')
def template_format_time(time):
    # return '%02d:%02d:%02d' % (int(time//60//60), int(time//60)%60, int(time)%60)
    return '%02d:%02d' % (int(time // 60), int(time) % 60)


@app.route('/')
def index():
    return render_template('index.html')


def main(argv):
    global app
    parser = argparse.ArgumentParser(description='A minimalistic programming contest environment.')
    parser.add_argument('contest', help='the contest directory')
    parser.add_argument('-p', '--port', default=31415, type=int, help='the port to listen on')
    parser.add_argument('-H', '--host', default='', help='the host to listen on')
    parser.add_argument('-d', '--debug', default=False, action='store_true', help='run in debug mode')
    parser.add_argument('--prefix', default=None, help='run under prefix')
    # parser.add_argument('--hostname', default=None, help='run with the specified hostname')
    parser.add_argument('--droptables', default=False, action='store_true', help='drop database tables and exit')
    opts = app.opts = parser.parse_args(argv)
    contest = app.contest = Contest.load(opts.contest)
    app.config['SQLALCHEMY_DATABASE_URI'] = contest.db

    models.set_contest_id(contest.id)

    db.init_app(app)

    if opts.droptables:
        print('You are about to drop the database tables for contest %s!!!' % contest.id)
        if input('Are you sure you want to continue? (y/N) ').lower() == 'y':
            db.drop_all(app=app)

        return 0

    db.create_all(app=app)
    app.run(host=opts.host, port=opts.port, debug=opts.debug)

if __name__ == '__main__':
    main(sys.argv[1:])
