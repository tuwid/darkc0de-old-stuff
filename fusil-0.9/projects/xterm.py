"""
Demontration of xterm bug: off-by-one error in memory allocation used
to parse PATH environement variable.
"""

def setupProject(project):
    process = ProjectProcess(project, ['xterm', 'ls'], timeout=1.0)
    setupX11Process(process)
    process.env.add(EnvVarLength('PATH', max_length=1000))

    WatchProcess(process, timeout_score=0)
    WatchStdout(process)

from fusil.process.env import EnvVarLength
from fusil.process.create import ProjectProcess
from fusil.process.watch import WatchProcess
from fusil.process.stdout import WatchStdout
from fusil.x11 import setupX11Process

