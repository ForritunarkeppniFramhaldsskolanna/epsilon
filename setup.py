#!/usr/bin/python3

import os, sys, shutil, fnmatch, subprocess, pwd
import argparse

DIR = os.path.abspath(os.path.dirname(__file__))

parser = argparse.ArgumentParser(description='An install script for epsilon.')
parser.add_argument('--prefix', default='/opt/epsilon2', help='the prefix that epsilon should be installed under') # TODO: change to /opt/epsilon
parser.add_argument('--noserver', default=False, action='store_true', help='don\'t install server')
parser.add_argument('--nojudge', default=False, action='store_true', help='don\'t install judge')
parser.add_argument('--nojail', default=False, action='store_true', help='don\'t build judge jail')
parser.add_argument('action', help='"install" or "uninstall"')
opts = parser.parse_args()

opts.prefix = os.path.abspath(opts.prefix).rstrip('/')

PERMS = [
    ('*', (644, 755, 'root')),
    # ('./judge/automatic-judge.py', (755, 755, 'root')),
    ('./judge/execute-submission.sh', (755, 755, 'root')),
    ('./judge/jail-setup.sh', (744, 744, 'root')),
    ('./judge/jail-destroy.sh', (744, 744, 'root')),
    ('./judge/submissions', (777, 777, 'root')),
    ('./judge/scripts/*.sh', (755, 755, 'root')),
    ('./server/db/setup_db.sh', (755, 755, 'root')),
    ('./bin/epsilon-judge', (755, 755, 'root')),
    ('./bin/epsilon-server', (755, 755, 'root')),
]

KEYS = {
    'PREFIX': opts.prefix,
    'JUDGE_USER_PREFIX': 'epsilon',
    'JUDGE_USERS': '4'
}

KEY_EXPAND = [
    '*.sh',
    '*.py',
    # '*.html'
    './bin/epsilon-judge',
    './bin/epsilon-server',
]

def log(txt):
    sys.stdout.write("%s\n" % txt)

def fatal(error):
    sys.stderr.write('error: %s\n' % error)
    sys.exit(1)

def sh(cmd, cwd=None):
    global opts
    if cwd is None: cwd = opts.prefix
    sub = subprocess.Popen(cmd, cwd=cwd)
    if not sub.wait() == 0:
        fatal('command failed: %s' % ' '.join(cmd))

def updateperms(path):
    global opts
    dest = os.path.join(opts.prefix, path)

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

        tat = 0
        res = ''
        while tat < len(txt):
            if txt[tat] == '_' and txt[tat+1] == '_':
                cnt = 0
                at = tat + 2
                while at + cnt + 1 < len(txt) and (ord('A') <= ord(txt[at + cnt]) <= ord('Z') or txt[at + cnt] == '_'):
                    if txt[at + cnt] == '_' and txt[at + cnt + 1] == '_':
                        break
                    cnt += 1

                pre = 'EPSILON_'
                if (at + cnt + 1 < len(txt)
                    and txt[at + cnt] == '_'
                    and txt[at + cnt + 1] == '_'
                    and txt[at:at+len(pre)] == pre
                    and txt[at+len(pre):at+cnt] in KEYS):
                    res += KEYS[txt[at+len(pre):at+cnt]]
                    tat += cnt + 4
                else:
                    res += txt[tat]
                    tat += 1
            else:
                res += txt[tat]
                tat += 1

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
        sh(['virtualenv', '--no-site-packages', '-p', 'python3.3', 'venv'], cwd=path)

    log('updating virtualenv requirements at %s' % path)
    sh(['bash', '-c', '''
        source ./venv/bin/activate
        pip install -r requirements.txt
    '''], cwd=path)

def install():
    global opts

    if not os.path.isdir(opts.prefix):
        os.makedirs(opts.prefix)

    log('installing necessary files')
    updateperms('.')
    log('files for the library')
    update('./lib')

    log('executables')
    update('./bin')

    if not opts.noserver:
        log('files for the server')
        update('./server')
        setup_virtualenv('./server/')
    else:
        os.unlink(os.path.join(os.prefix, './bin/epsilon-server'))

    if not opts.nojudge:
        log('files for the judge')
        update('./judge')
        log('building SafeExec')
        sh(['make'], cwd=os.path.join(opts.prefix, './judge/SafeExec'))

        if not opts.nojail:
            log('destroying the jail, if it exists')
            sh(['./jail-destroy.sh'], cwd=os.path.join(opts.prefix, './judge'))
            log('creating the jail')
            sh(['./jail-setup.sh'], cwd=os.path.join(opts.prefix, './judge'))

        setup_virtualenv('./judge')
    else:
        os.unlink(os.path.join(os.prefix, './bin/epsilon-judge'))

    log('')
    log('')
    log('Installation succeeded.')
    log('Please do the following:')
    log('')

    if not opts.nojudge:
        log('   - append the following to /etc/sudoers (where your_username is the user who will be running epsilon judge):')
        log('        your_username ALL=(root) NOPASSWD: %s/judge/execute-submission.sh' % opts.prefix)

    log('   - add %s/bin to your PATH variable' % opts.prefix)

    log('')
    log('')

def uninstall():
    global opts

    if os.path.exists(os.path.join(opts.prefix, './judge')):
        log('destroying the jail')
        sh(['./jail-destroy.sh'], cwd=os.path.join(opts.prefix, './judge'))

    log('erasing the whole prefix directory')
    shutil.rmtree(opts.prefix, ignore_errors=True)

if opts.action == 'install':
    install()
elif opts.action == 'uninstall':
    uninstall()
else:
    sys.stderr.write('error: action must be either "install" or "uninstall"\n')
    parser.print_help()
    sys.exit(1)

