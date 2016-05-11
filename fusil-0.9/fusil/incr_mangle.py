from fusil.mangle_agent import MangleAgent
from fusil.incr_mangle_op import OPERATIONS
from random import randint, choice
from array import array

MAX_TRY = 25000

class IncrMangleError(ValueError):
    pass

class DataVersion:
    """
    Immutable data version
    """
    def __init__(self, versions, data, operations, dirty_bits):
        self.versions = versions
        self.data = data
        self.operations = operations
        self.version = versions.getVersionNumber()
        self.dirty_bits = frozenset(dirty_bits)

    def createVersion(self, agent, datalen):
        operations = list(self.operations)
        dirty_bits = set(self.dirty_bits)
        wanted_len = len(operations) + randint(1, agent.operation_per_version)
        nb_try = 0
        while len(operations) < wanted_len:
            if MAX_TRY <= nb_try:
                raise IncrMangleError("Unable to create new operation (try: %s)" % nb_try)
            nb_try += 1
            operation = self.createOperation(agent, datalen, dirty_bits)
            if not operation:
                continue
            for bit in xrange(operation.offset, operation.offset+operation.size):
                dirty_bits.add(bit)
            operations.append(operation)
            nb_try = 0
        return ModifiedVersion(self.versions, tuple(operations), dirty_bits)

    def createOperation(self, agent, datalen, dirty_bits):
        operation_cls = choice(agent.operations)
        operation = operation_cls(agent, datalen)
        for bit in xrange(operation.offset, operation.offset+operation.size):
            if bit in dirty_bits:
                return None
        return operation

    def getPrevious(self):
        return self.versions.getPrevious(self)

    def createData(self):
        raise NotImplementedError()

    def revert(self):
        """
        Revert this version and return new last version
        """
        self.versions.removeVersion(self)
        return self.versions.getLast()

    def __str__(self):
        return "<DataVersion version=%s operations=%s dirty_bits=%s>" % (
            self.version, len(self.operations), len(self.dirty_bits))

    def clearCache(self):
        pass

class OriginalVersion(DataVersion):
    def __init__(self, versions, data):
        DataVersion.__init__(self, versions, data, tuple(), set())

    def createData(self):
        return array('B', self.data)

    def revert(self):
        return self

    def __str__(self):
        return "<OriginalVersion>"

class ModifiedVersion(DataVersion):
    def __init__(self, versions, operations, dirty_bits):
        DataVersion.__init__(self, versions, None, operations, dirty_bits)

    def createData(self):
        # Cached result?
        if self.data:
            return array('B', self.data)

        # Get previous complete data
        previous = self
        while True:
            previous = previous.getPrevious()
            if previous.data:
                break

        # Apply new operations (since previous version)
        data = array('B', previous.data)
        for operation in self.operations[len(previous.operations):]:
            operation(data)

        # Cache result
        self.data = data.tostring()
        return data

    def clearCache(self):
        self.data = None

class DataVersions:
    def __init__(self):
        self.versions = []

    def getVersionNumber(self):
        return len(self.versions)+1

    def addVersion(self, version):
        self.versions.append(version)

        # Clear cache of old versions
        for version in self.versions[:-2]:
            version.clearCache()

    def removeVersion(self, version):
        self.versions.remove(version)

    def getLast(self):
        try:
            return self.versions[-1]
        except IndexError:
            return None

    def getPrevious(self, version):
        index = self.versions.index(version)
        return self.versions[index-1]

    def rollback(self, version_number):
        del self.versions[version_number:]
        return self.versions[-1]

class IncrMangle(MangleAgent):
    def __init__(self, project, source):
        MangleAgent.__init__(self, project, source, 1)
        self.versions = DataVersions()
        self.previous_score = None
        self.previous_session = "init"
        self.score_diff = None

        # User config
        self.operation_per_version = 1
        self.max_version = 25
        self.min_offset = None
        self.max_offset = None
        self.operations = OPERATIONS

    def on_session_done(self, score):
        self.score_diff = None
        if score < 0:
            self.previous_session = "error"
        elif (self.project().success_score <= score):
            self.previous_session = "success"
        else:
            self.previous_session = "normal"
            if self.previous_score is not None:
                self.score_diff = score - self.previous_score
            self.previous_score = score

    def stateText(self):
        text = self.previous_session
        if self.previous_score is not None:
            text += ", score:%.1f" % (self.previous_score*100)
            if self.score_diff is not None:
                text += ", score diff:%+.1f" % (self.score_diff*100)
        return text

    def checkPreviousVersion(self, version):
        # Success: Rollback to original version
        if self.previous_session == "success":
            original = self.versions.rollback(1)
            self.error("Rollback to %s" % original)
            return original

        # Failure: revert previous change
        if self.previous_session == "error":
            self.warning("Revert previous version (error): %s (score %s)" % (version, self.stateText()))
            return version.revert()

        # Smaller score
        if self.score_diff is not None and self.score_diff < 0:
            self.error("Revert previous version (smaller score): %s (score %s)" % (version, self.stateText()))
            return version.revert()

        # Too many version: rollback to random version
        if self.max_version < version.version:
            return self.rollbackLast()

        # Valid version: keep it
        previous = version.getPrevious()
        for operation in version.operations[len(previous.operations):]:
            self.warning("New operation: %s" % operation)
        self.error("Accepted version: %s (%s)" % (
            version, self.stateText()))
        return version

    def rollbackLast(self):
        number = randint(1, self.versions.getLast().version)
        version = self.versions.rollback(number)
        self.error("Rollback to %s" % version)
        return version

    def mangleData(self, data, file_index):
        # Get last version
        version = self.versions.getLast()
        if version:
            version = self.checkPreviousVersion(version)
        else:
            version = OriginalVersion(self.versions, data.tostring())
            self.warning("Create first version: %s" % version)
            self.versions.addVersion(version)

        # New version
        previous = version
        try:
            version = previous.createVersion(self, len(data))
            self.warning("New version %s based on %s" % (version, previous))
            self.versions.addVersion(version)
        except IncrMangleError, err:
            for index in xrange(10):
                self.error(str(err))
            version = self.rollbackLast()

        # Create data
        return version.createData()

