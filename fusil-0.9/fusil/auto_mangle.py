from fusil.mangle import MangleFile
from fusil.tools import minmax

class AutoMangle(MangleFile):
    def __init__(self, project, *args, **kw):
        MangleFile.__init__(self, project, *args, **kw)
        self.hard_max_op = 10000
        self.hard_min_op = 0
        self.aggressivity = None
        self.fixed_size_factor = 1.0

    def on_session_start(self):
        pass

    def on_aggressivity_value(self, value):
        self.aggressivity = value
        self.mangle()

    def setupConf(self, data):
        operations = ["bit"]
        size_factor = 0.30

        if 0.25 <= self.aggressivity:
            operations.extend(("replace", "special_value"))
        if 0.50 <= self.aggressivity:
            operations.extend(("insert_bytes", "delete_bytes"))
            size_factor = 0.20
        self.config.operations = operations

        # Display config
        count = len(data) * size_factor * self.fixed_size_factor
        count = minmax(self.hard_min_op, count, self.hard_max_op)
        count = int(count * self.aggressivity)
        self.config.max_op = max(count, self.hard_min_op)
        self.config.min_op = max(int(self.config.max_op * 0.80), self.hard_min_op)
        self.warning("operation#:%s..%s  operations=%s"
            % (self.config.min_op, self.config.max_op, self.config.operations))

    def mangleData(self, data, file_index):
        self.setupConf(data)
        return MangleFile.mangleData(self, data, file_index)

