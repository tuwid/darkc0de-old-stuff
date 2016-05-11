from fusil.project_agent import ProjectAgent
from fusil.file_watch import FileWatch

class Syslog(ProjectAgent):
    def __init__(self, project):
        ProjectAgent.__init__(self, project, "syslog")
        self.syslog = FileWatch(project, open('/var/log/syslog'), 'syslog:syslog', start='end')
        self.messages = FileWatch(project, open('/var/log/messages'), 'syslog:messages', start='end')

    def __iter__(self):
        if self.syslog:
            yield self.syslog
        if self.messages:
            yield self.messages

