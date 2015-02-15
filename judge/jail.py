import sys, os, math
from subprocess import Popen, PIPE
from tempfile import mkstemp

DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.abspath(os.path.join(DIR, '..'))
sys.path.insert(0, BASE_DIR)
from config.config import CONFIG

class Jail:
    def __init__(self, id):
        self.box_id = id
        self.default_env = {
            'HOME': '/box',
            'PATH': '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
        }

    def _execute(self, cmd, stdin=None):
        proc = Popen([CONFIG['ISOLATE'], '-b', str(self.box_id), '--cg'] + cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = proc.communicate(stdin.encode('utf-8') if stdin is not None else b'')
        return (proc.returncode, stdout.decode('utf-8'), stderr.decode('utf-8'))

    def _get_tempfile(self, dir=None):
        return mkstemp(prefix='epsilon', dir=dir)

    def init(self):
        # TODO: add more directories, probably
        returncode, stdout, stderr = self._execute(['--init'])
        assert returncode == 0
        self.jail_dir = stdout.strip()
        self.box_dir = os.path.join(self.jail_dir, 'box')

    def run(self, command,
            timelim=None, # seconds, can be a float
            memlim=None,  # Kbytes, integer
            processes=1,
            stdin=None,
            env=None,
            dirs=None):
        args = []
        args += ['-c', '/box']

        if timelim is not None:
            args += ['--time=%d' % math.ceil(timelim)]
            args += ['--cg-timing']
            args += ['--wall-time=%d' % max(60, math.ceil(timelim) * 10)]

        if memlim is not None:
            # args += ['--mem=%d' % memlim]
            args += ['--cg-mem=%d' % memlim]

        args += ['--processes=%d' % processes]

        if not env: env = {}
        for k, v in self.default_env.items():
            if k not in env:
                env[k] = v
        for k, v in env.items():
            # XXX: escape these correctly
            args += ['--env=%s=%s' % (k, v)]

        if not dirs:
            dirs = []
        dirs.append('/epsilon/judge/scripts')
        dirs.append('/usr/lib')
        dirs.append('/usr/local/lib')
        dirs.append('/usr/include')
        dirs.append('/usr/local/include')
        dirs.append('/lib')
        dirs.append('/lib64')
        dirs.append('/etc')
        dirs.append('/sbin')
        for dir in dirs:
            args += ['--dir=%s' % dir]

        stdin_file = None
        if stdin is not None:
            handle, stdin_file = self._get_tempfile(self.box_dir)
            with os.fdopen(handle, 'w') as f: f.write(stdin)
            args += ['--stdin=%s' % os.path.join('/box', os.path.relpath(stdin_file, self.box_dir))]

        handle, stdout_file = self._get_tempfile(self.box_dir)
        os.close(handle)
        args += ['--stdout=%s' % os.path.join('/box', os.path.relpath(stdout_file, self.box_dir))]

        handle, stderr_file = self._get_tempfile(self.box_dir)
        os.close(handle)
        args += ['--stderr=%s' % os.path.join('/box', os.path.relpath(stderr_file, self.box_dir))]

        handle, meta_file = self._get_tempfile()
        os.close(handle)
        args += ['--meta=%s' % meta_file]

        returncode, stdout, stderr = self._execute(args + ['--run', '--'] + command)

        meta = {}
        try:
            with open(meta_file) as f:
                metastr = f.read()
            for line in metastr.split('\n'):
                if ':' in line:
                    k, v = line.split(':', 1)
                    meta[k] = v
        except:
            pass
        try:
            with open(stdout_file) as f:
                meta['stdout'] = f.read()
        except:
            pass
        try:
            with open(stderr_file) as f:
                meta['stderr'] = f.read()
        except:
            pass

        if meta_file: os.unlink(meta_file)

        # meta['status'] can be:
        #    - SG: interrupted
        #    - TO: time limit exceeded
        #    - RE: runtime error
        #    - OK

        if 'status' not in meta:
            meta['status'] = 'OK'

        if meta['status'] == 'OK':
            if float(meta['time']) > timelim:
                meta['status'] = 'TO'

        return meta

    def cleanup(self):
        self._execute(['--cleanup'])

# if __name__ == '__main__':
#     jail = Jail(0)
#     try:
#         jail.init()
#         # os.system('/bin/bash')
#         res = jail.run(['/bin/bash'],
#                 stdin='echo moooo',
#                 processes=10,
#                 timelim=3,
#                 memlim=100*1024,
#             )
#     finally:
#         jail.cleanup()
# 
#     for k, v in sorted(res.items()):
#         print(k, v)

