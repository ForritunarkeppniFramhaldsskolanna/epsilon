#!/usr/bin/env python3

import os
import sys
import shutil
import fnmatch
import subprocess
import argparse

DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(DIR, 'config'))
sys.path.append(os.path.join(DIR, 'lib'))
from config import CONFIG as KEYS, load_executables
from yamllib import insert_conf

parser = argparse.ArgumentParser(description='An install script for epsilon.')
parser.add_argument('--prefix', default='/opt/epsilon', help='the prefix that epsilon should be installed under')
parser.add_argument('--noserver', default=False, action='store_true', help='don\'t install server')
parser.add_argument('--nojudge', default=False, action='store_true', help='don\'t install judge')
parser.add_argument('--nojail', default=False, action='store_true', help='don\'t build judge jail')
parser.add_argument('--nomanualjudge', default=False, action='store_true', help='don\'t install the manual judge')
parser.add_argument('action', help='"install" or "uninstall"')
opts = parser.parse_args()

opts.prefix = os.path.abspath(opts.prefix).rstrip('/')

BIN_PATH = '/usr/local/bin'

PERMS = [
    ('*', (644, 755, 'root')),
    ('./judge/execute-submission.sh', (755, 755, 'root')),
    ('./judge/jail-setup.sh', (744, 744, 'root')),
    ('./judge/jail-destroy.sh', (744, 744, 'root')),
    ('./judge/submissions', (777, 777, 'root')),
    ('./judge/scripts/*.sh', (755, 755, 'root')),
    ('./server/db/setup_db.sh', (755, 755, 'root')),
    ('./bin/epsilon-judge', (755, 755, 'root')),
    ('./bin/epsilon-server', (755, 755, 'root')),
    ('./bin/epsilon-manual-judge', (755, 755, 'root')),
]


PROG_LANGS = {
    ('js', 'JS'),
    ('python2', 'PYTHON2'),
    ('python3', 'PYTHON3'),
    ('ruby', 'RUBY'),
    ('perl', 'PERL'),
    ('java', 'JAVA'),
    ('mono', 'MONO'),
    ('octave', 'OCTAVE'),
}


KEY_EXPAND = [
    './config/config.ini',
    './bin/epsilon-*',
]


def log(txt):
    sys.stdout.write("%s\n" % txt)


def fatal(error):
    sys.stderr.write('error: %s\n' % error)
    sys.exit(1)


def sh(cmd, cwd=None, die=True):
    log(' '.join(cmd))

    global opts
    if cwd is None:
        cwd = opts.prefix
    sub = subprocess.Popen(cmd, cwd=cwd)
    if sub.wait() != 0 and die:
        fatal('command failed: %s' % ' '.join(cmd))


def sh_com(cmd, stdin, cwd=None, die=True):
    log(' '.join(cmd))

    global opts
    if cwd is None:
        cwd = opts.prefix
    sub = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd=cwd)
    stdout, stderr = sub.communicate(stdin)
    if sub.returncode != 0 and die:
        fatal('command failed: %s' % ' '.join(cmd))
    return stdout.decode('utf-8')


def updateperms(path):
    global opts

    for glob, (f, d, u) in reversed(PERMS):
        if fnmatch.fnmatch(path, glob):
            if os.path.isfile(path):
                sh(['chmod', str(f), path])
            else:
                sh(['chmod', str(d), path])

            sh(['chown', u, path])
            break


def copy(path):
    global opts
    src = os.path.abspath(os.path.join(DIR, path))
    dest = os.path.abspath(os.path.join(opts.prefix, path))

    log('copying %s' % path)

    found = False
    for glob in KEY_EXPAND:
        if fnmatch.fnmatch(path, glob):
            found = True
            break

    if found:
        with open(src, 'r', encoding='utf-8') as f:
            txt = f.read()

        res = insert_conf(txt, config=KEYS)

        with open(dest, 'w', encoding='utf-8') as f:
            f.write(res)
    else:
        shutil.copyfile(src, dest)


def update(path):
    global opts
    src = os.path.abspath(os.path.join(DIR, path))
    dest = os.path.abspath(os.path.join(opts.prefix, path))
    log('updating %s' % dest)

    if os.path.isfile(dest):
        os.unlink(dest)

    if not os.path.exists(dest):
        os.mkdir(dest)

    updateperms(path)

    for f in os.listdir(src):

        if os.path.isdir(os.path.join(src, f)):

            update(os.path.join(path, f))

        else:

            if os.path.isdir(os.path.join(dest, f)):
                shutil.rmtree(os.path.join(dest, f))

            if os.path.isfile(os.path.join(dest, f)):
                os.unlink(os.path.join(dest, f))

            copy(os.path.join(path, f))

            updateperms(os.path.join(path, f))


def setup_virtualenv(path):
    global opts
    path = os.path.abspath(os.path.join(opts.prefix, path))
    if not os.path.exists(os.path.join(path, 'venv')):
        log('setting up virtualenv at %s' % path)
        sh(['virtualenv', '--no-site-packages', '-p', 'python3', 'venv'], cwd=path)

    log('updating virtualenv requirements at %s' % path)
    sh(['bash', '-c', '''
        source ./venv/bin/activate
        pip install -r requirements.txt
    '''], cwd=path)


def install():
    global opts

    KEYS['PREFIX'] = opts.prefix

    # TODO: make this optional if not installing judge
    log('installing safeexec')
    sh(['make'], cwd=os.path.join(DIR, 'judge/SafeExec'))
    sh(['make', 'install'], cwd=os.path.join(DIR, 'judge/SafeExec'))
    sh(['make', 'clean'], cwd=os.path.join(DIR, 'judge/SafeExec'))

    if not os.path.isdir(opts.prefix):
        os.makedirs(opts.prefix)

    load_executables()

    log('installing necessary files')
    updateperms('.')

    log('config files')
    update('./config')

    log('files for the library')
    update('./lib')

    log('files for the virtualenv')
    copy('./requirements.txt')
    updateperms('./requirements.txt')
    setup_virtualenv('.')

    log('executables')
    update('./bin')

    if not opts.noserver:
        log('files for the server')
        update('./server')
        sh(['ln', '-sf', os.path.join(opts.prefix, 'bin/epsilon-server'), os.path.join(BIN_PATH, 'epsilon-server')])

    if not opts.nojudge:
        log('files for the judge')
        update('./judge')
        sh(['ln', '-sf', os.path.join(opts.prefix, 'bin/epsilon-judge'), os.path.join(BIN_PATH, 'epsilon-judge')])

        if not opts.nojail:
            log('destroying the jail, if it exists')
            print(os.path.join(opts.prefix, 'judge'))
            sh(['./jail-destroy.sh'], cwd=os.path.join(opts.prefix, 'judge'))
            log('creating the jail')
            sh(['./jail-setup.sh'], cwd=os.path.join(opts.prefix, 'judge'))

            log('creating symlinks for programming languages')
            sh(['mkdir', os.path.join(opts.prefix, 'judge/jail/bin/lang/')])
            for lang, key_name in PROG_LANGS:
                sh(['ln', '-sf', KEYS['EXE_' + key_name], os.path.join(opts.prefix, 'judge/jail/bin/lang/' + lang)])

    if not opts.nomanualjudge:
        log('files for the manual judge')
        update('./manual_judge')
        sh(['ln', '-sf', os.path.join(opts.prefix, 'bin/epsilon-manual-judge'), os.path.join(BIN_PATH, 'epsilon-manual-judge')])

    log('')
    log('')
    log('Installation succeeded.')

    if not opts.nojudge:
        log('Please do the following:')
        log('')
        log('   - append the following to /etc/sudoers (where your_username is the user who will be running epsilon judge):')
        log('        your_username ALL=(root) NOPASSWD: %s/judge/execute-submission.sh' % opts.prefix)

    log('')
    log('')


def uninstall():
    global opts

    if os.path.exists(os.path.join(opts.prefix, 'judge/jail-destroy.sh')):
        log('destroying the jail')
        sh(['./jail-destroy.sh'], cwd=os.path.join(opts.prefix, 'judge'))

    log('removing binaries')
    sh(['rm', '-f', os.path.join(BIN_PATH, 'epsilon-server')], cwd='/')
    sh(['rm', '-f', os.path.join(BIN_PATH, 'epsilon-judge')], cwd='/')
    sh(['rm', '-f', os.path.join(BIN_PATH, 'epsilon-manual-judge')], cwd='/')

    log('erasing the whole prefix directory')
    sh(['rm', '-rf', opts.prefix], cwd='/')

    log('uninstalling safeexec')
    sh(['make', 'uninstall'], cwd=os.path.join(DIR, 'judge/SafeExec'))

if opts.action == 'install':
    install()
elif opts.action == 'uninstall':
    uninstall()
else:
    sys.stderr.write('error: action must be either "install" or "uninstall"\n')
    parser.print_help()
    sys.exit(1)
