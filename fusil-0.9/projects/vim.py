"""
Demonstration of vim bug: vim 7.0 doesn't validate VIM and VIMRUNTIME
environment variables length.
"""
from fusil.process.env import EnvVarLength
from fusil.process.create import ProjectProcess
from fusil.process.watch import WatchProcess
from fusil.process.stdout import WatchStdout

def setupProject(project):
    VIM = EnvVarLength(['VIM', 'VIMRUNTIME'], max_length=10000)

    process = ProjectProcess(project, ['vim', '--version'])
    process.env.add(VIM)
    WatchProcess(process)
    WatchStdout(process)

