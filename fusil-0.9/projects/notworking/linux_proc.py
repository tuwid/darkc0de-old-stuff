"""
Write random data in /proc/PID/* files
"""

from fusil.process.create import ProjectProcess
from fusil.process.watch import WatchProcess
from fusil.process.stdout import WatchStdout
from fusil.project_agent import ProjectAgent
from fusil.bytes_generator import BytesGenerator
from fusil.linux.syslog import Syslog
from os.path import join as path_join
from random import choice
from errno import ENOENT, EACCES, EINVAL, EPERM

class AttackProc(ProjectAgent):
    def __init__(self, project):
        ProjectAgent.__init__(self, project, "proc")
        self.generator = BytesGenerator(1, 256)

    def init(self):
        self.proc_keys = [
            'attr/current',
            'attr/exec',
            'attr/fscreate',
            'attr/keycreate',
            'attr/sockcreate',
            'clear_refs',
            'seccomp',

            # Strange keys
            #'mem',
            #'oom_adj',
        ]
        self.proc_path = None

    def on_process_create(self, agent):
        self.proc_path = "/proc/%s/" % agent.process.pid

    def live(self):
        if not self.proc_path:
            return
        self.info("Proc path: %s" % self.proc_path)

        key = choice(self.proc_keys)
        filename = path_join(self.proc_path, key)
        data = self.generator.createValue()
        self.info("Write data in %s: (len=%s) %r"
            % (filename, len(data), data))
        try:
            output = open(filename, 'w')
            output.write(data)
            output.close()
        except IOError, err:
            if err.errno in (EINVAL, EPERM):
                pass
            elif err.errno in (ENOENT, EACCES):
                self.error("Unable to write %s: %s" % (filename, err))
                self.removeKey(key)
            else:
                raise

    def removeKey(self, key):
        self.proc_keys.remove(key)
        if not self.proc_keys:
            self.error("All /proc entries are invalid!")
            self.send('project_done')
            self.proc_path = None

def setupProject(project):
#    project.session_timeout = 1.0
    process = ProjectProcess(project,
        ['/bin/bash'], timeout=5.0)
    AttackProc(project)
    WatchProcess(process, timeout_score=0)
    WatchStdout(process)
    syslog = Syslog(project)
    for watch in syslog:
        watch.ignoreRegex('info="invalid command"')
        watch.show_not_matching = True

