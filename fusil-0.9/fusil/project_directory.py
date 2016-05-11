from os.path import basename
from fusil.project_agent import ProjectAgent
from fusil.directory import Directory
from os import getcwd

class ProjectDirectory(ProjectAgent, Directory):
    def __init__(self, project):
        # Create $PWD/run-0001 directory name
        Directory.__init__(self, getcwd())
        self.directory = self.uniqueFilename('run', count=1, save=False)

        # Initialize the agent and create the directory
        ProjectAgent.__init__(self, project, "directory:%s" % basename(self.directory))
        self.warning("Create directory: %s" % self.directory)
        self.mkdir()

    def destroy(self):
        if not self.directory:
            return False
        remove = self.isEmpty(True)
        if remove:
            self.info("Remove directory: %s" % self.directory)
            self.rmtree()
        else:
            self.error("Keep non-empty directory: %s" % self.directory)
        self.directory = None
        return remove

