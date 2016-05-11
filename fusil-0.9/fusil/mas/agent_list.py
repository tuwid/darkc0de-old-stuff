class AgentList:
    def __init__(self):
        self.agents = []

    def append(self, agent):
        if agent in self.agents:
            raise KeyError("Agent %r already registred")
        self.agents.append(agent)

    def _destroy(self, agent):
        agent.debug("Removed from agent list")
        agent.deactivate()
        agent.unregister(False)

    def remove(self, agent, destroy=True):
        if agent not in self.agents:
            return
        self.agents.remove(agent)
        if destroy:
            self._destroy(agent)

    def clear(self):
        while self.agents:
            agent = self.agents[-1]
            del self.agents[-1]
            self._destroy(agent)

    def __del__(self):
        self.clear()

    def __contains__(self, agent):
        return agent in self.agents

    def __iter__(self):
        return iter(self.agents)

