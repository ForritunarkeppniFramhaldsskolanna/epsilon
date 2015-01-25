import os
import shutil
import subprocess
import sys
import shlex

prefix = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
CONFIG = {
    'PREFIX': prefix,
    'JUDGE_USER_PREFIX': 'epsilon',
    'JUDGE_USERS': '4'
}

EXECUTABLES = {
    # Programming languages
    'JS': ['js', 'js24'],
    'PYTHON2': ['python2', 'python2.7'],
    'PYTHON3': ['python3', 'python3.4', 'python3.3', 'python3.2'],
    'GPP': ['g++'],
    'GCC': ['gcc'],
    'RUBY': ['ruby'],
    'PERL': ['perl'],
    'JAVAC': ['javac'],
    'JAVA': ['java'],
    'DMCS': ['dmcs'],
    'MONO': ['mono'],
    'PASCAL': ['fpc'],
    'PASCAL_PPC': ['ppcx64', 'ppc386'],
    'OCTAVE': ['octave'],
    'OCTAVE_CLI': ['octave-cli'],

    # Other executables
    'SAFEEXEC': ['safeexec'],
    'BASH': ['bash'],
    'SH': ['sh'],
    'LOCALE': ['locale'],
    'LOCALE_GEN': ['locale-gen'],
    'LOCALEDEF': ['localedef'],
    'LDCONFIG': ['ldconfig'],
    'LDCONFIG_REAL': ['ldconfig.real'],
}

OPTIONAL_EXECUTABLES = {
    'OCTAVE_CLI',
    'PASCAL_PPC',
    'LDCONFIG_REAL',
}


def log(s):
    if __name__ == "__main__":
        return
    # print(s)


# TODO: move this check somewhere else, so that it isnt executed every time.
def _sh_com(cmd, stdin, cwd=None, die=True):
    log(' '.join(cmd))
    global opts
    if cwd is None:
        cwd = prefix
    sub = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd=cwd)
    stdout, stderr = sub.communicate(stdin)
    if sub.returncode != 0 and die:
        pass
        # fatal('command failed: %s' % ' '.join(cmd))
    return stdout.decode('utf-8')


def load_libs(found):
    libs = []
    try:
        ldd = _sh_com(['ldd', found], None, cwd='/', die=False)
        if ldd.strip() != 'not a dynamic executable':
            for line in ldd.strip().split('\n'):
                sline = line.split('(')[0].strip()
                if '=>' in sline:
                    rest = sline.split('=>')[1].strip()
                    if rest:
                        libs.append(rest)
                else:
                    libs.append(sline)
    except:
        pass
    return libs


def load_executables():
    global CONFIG

    old_path = os.environ['PATH']
    if 'VIRTUAL_ENV' in os.environ:
        venv = os.path.abspath(os.path.join(os.environ['VIRTUAL_ENV'], 'bin'))
        os.environ['PATH'] = ':'.join( p for p in os.environ['PATH'].split(':') if os.path.abspath(p) != venv )

    for key_name, exec_paths in EXECUTABLES.items():
        found = None
        for exec_path in exec_paths:
            if exec_path.startswith('/'):
                if os.path.isfile(exec_path) and os.access(exec_path, os.X_OK):
                    found = exec_path
            else:
                found = shutil.which(exec_path)
            if found is not None:
                break

        if found is None:
            if key_name in OPTIONAL_EXECUTABLES:
                CONFIG['EXE_' + key_name] = ''
                CONFIG['LIBS_' + key_name] = ''
            else:
                log('no path found for executable %s' % key_name)
        else:
            CONFIG['EXE_' + key_name] = found
            log('path for executable %s is %s' % (key_name, found))
            libs = load_libs(found)
            if libs:
                CONFIG['LIBS_' + key_name] = ', ' + ', '.join(libs)
                log('libraries for %s are %s' % (key_name, ', '.join(libs)))
            else:
                CONFIG['LIBS_' + key_name] = ''

        if key_name in OPTIONAL_EXECUTABLES:
            CONFIG['OPT_EXE_' + key_name] = ', ' + found if found else ''

    os.environ['PATH'] = old_path

load_executables()

# Output environment exports if this file was executed directly.
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    if sys.argv[1] == "export":
        for key, val in CONFIG.items():
            print("export EPSILON_%s=%s" % (key, shlex.quote(val)))
    else:
        sys.exit(1)
