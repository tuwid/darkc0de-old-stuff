from fusil.project_agent import ProjectAgent
from fusil.tools import minmax
from datetime import datetime

CREATE_GRAPH_DAT = False

class AggressivityAgent(ProjectAgent):
    def __init__(self, project):
        ProjectAgent.__init__(self, project, "aggressivity")

        # Options for state machine
        self.aggressivity_min = 0.01
        self.aggressivity_max = 1.00
        self.add_after = 5       # steps
        self.faster_after = 10   # steps
        self.slower_after = 5    # steps
        self.state_increment = {
            "+":   0.01,
            "++":  0.04,
            "-":  -0.01,
            "--": -0.04,
        }

        # Variables of state machine
        self.state = "init"
        self.state_age = 1
        self.min_score = None
        self.max_score = None

        # Attributes for graph.dat file
        self.graph_data = None
        self.last_session_index = None

        # Set default value of aggressivity
        self.setValue(self.aggressivity_min)

    def setValue(self, value):
        value = round(value, 2)
        value = minmax(self.aggressivity_min, value, self.aggressivity_max)
        self.aggressivity = value

    def on_session_start(self):
        self.send('aggressivity_value', self.aggressivity)

        text = []
        if self.min_score is not None and self.max_score is not None:
            text.append("%.1f%%<=score<=%.1f%%" % (self.min_score*100, self.max_score*100))
        text.append("aggressivity:%s" % self)
        text.append("state:%s (age:%s)" % (self.state, self.state_age))
        self.warning("  ".join(text))

    def destroy(self):
        if not self.graph_data:
            return
        self.writeGraphData(self.last_session_index+1, 0.0)
        self.writeGraphData(self.last_session_index+1, 0.0)

    def writeGraphData(self, session_index, score):
        self.last_session_index = session_index
        if CREATE_GRAPH_DAT and not self.graph_data:
            directory = self.project().directory
            filename = directory.uniqueFilename('graph.dat')
            self.graph_data = open(filename, 'w')
            print >>self.graph_data, "# Aggressivity data"
            print >>self.graph_data, "# Started at %s" % datetime.now()
            print >>self.graph_data, "#"
            print >>self.graph_data, "# session_index score aggressivity"
        if self.project().success_score <= score:
            score = 1.0
        else:
            score = minmax(-1.0, score, 1.0)
        if self.graph_data:
            print >>self.graph_data, "%u\t%.3f\t%.3f" % (
                self.last_session_index, score, self.aggressivity)
            self.graph_data.flush()

    def on_session_done(self, score):
        self.writeGraphData(self.project().session_index, score)
        self.update(score)

    def update(self, score):
        # Update previous/min/max score variables
        if self.min_score is None:
            self.min_score = score
        if self.max_score is None:
            self.max_score = score

        # Choose state using score
        self.state_age += 1
        state = self.updateState(score)
        if state:
            self.state = state
            self.state_age = 1

        # Update aggressivity depending on the state
        try:
            self.setValue(self.aggressivity + self.state_increment[self.state])
        except KeyError:
            # State has no increment
            pass

    def updateState(self, score):
        if self.project().success_score <= score:
            return "success"

        if self.max_score < score:
            # Best new score: continue to augment aggressivity to reach success
            self.max_score = score
            return "0"
        if score < self.min_score:
            self.min_score = score
            return "-"

        if self.state == "init":
            # First aggressivity evolution: start to grow
            return "+"

        if self.state == "success":
            # If we reach a success, try to keep aggressivity constant
            # to get more success
            return "0"

        if self.aggressivity < self.aggressivity_max:
            if self.state == "0" and self.add_after < self.state_age:
                # Nothing interesting since many cycles,
                # augment to make the system react
                return "+"
            if self.state == "+" and self.faster_after < self.state_age:
                # Grow acceleration
                return "++"
        if self.aggressivity_min < self.aggressivity:
            if score < 0:
                # Target error: reduce aggressivity
                if self.state not in ("-", "--"):
                    return "-"
            if self.state == "-" and self.slower_after < self.state_age:
                # Reduction acceleration
                return "--"

        if self.state in ("-", "--") and 0 <= score:
            # During a reduction stage, target is now calm: stop reduction
            return "0"

        # Hit min/max aggressivity limits
        if self.aggressivity == self.aggressivity_min and self.state in ("-", "--"):
            return "0"
        if self.aggressivity == self.aggressivity_max and self.state in ("+", "++"):
            return "0"
        return None

    def __str__(self):
        return "%.1f%%" % (self.aggressivity*100)

