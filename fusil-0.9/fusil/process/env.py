from fusil.project_agent import ProjectAgent
from random import choice, randint
from os import getenv
from fusil.bytes_generator import BytesGenerator, ASCII0, DECIMAL_DIGITS
from ptrace.os_tools import RUNNING_WINDOWS

class EnvironmentVariable:
    def __init__(self, name, max_count=1):
        self.name = name
        self.min_count = 1
        self.max_count = max_count

    def hasName(self, name):
        if isinstance(self.name, (list, tuple)):
            return name in self.name
        else:
            return self.name == name

    def createName(self):
        """
        Generate variable name
        """
        if isinstance(self.name, (list, tuple)):
            return choice(self.name)
        else:
            return self.name

    def createValue(self):
        """
        Generate variable content
        """
        raise NotImplementedError()

    def create(self):
        """
        Generate variable content
        """
        if isinstance(self.name, (list, tuple)):
            max_count = len(self.name)
        else:
            max_count = 1
        if self.max_count:
            max_count = min(max_count, self.max_count)
        count = randint(self.min_count, max_count)
        for index in xrange(count):
            name = self.createName()
            value = self.createValue()
            yield (name, value)


class EnvVarValue(EnvironmentVariable):
    def __init__(self, name, value='', max_count=1):
        EnvironmentVariable.__init__(self, name, max_count)
        self.value = value

    def createValue(self):
        return self.value


class EnvVarLength(BytesGenerator, EnvironmentVariable):
    def __init__(self, name, min_length=0, max_length=2000, characters=None, max_count=1):
        if not characters:
            characters = set('A')
        BytesGenerator.__init__(self, min_length, max_length, characters)
        EnvironmentVariable.__init__(self, name, max_count)


class EnvVarInteger(EnvVarLength):
    def __init__(self, name, max_count=1):
        # 2^32 length in decimal: 10 digits
        # 2^64 length in decimal: 10 digits
        # 2^128 length in decimal: 39 digits
        EnvVarLength.__init__(self, name, 1, 40, DECIMAL_DIGITS, max_count)

    def createValue(self):
        value = EnvVarLength.createValue(self)
        if randint(0, 1) == 1:
            return "-"+value
        else:
            return value


class EnvVarRandom(EnvVarLength):
    def __init__(self, name, min_length=0, max_length=10000, max_count=1):
        EnvVarLength.__init__(self, name, min_length, max_length,
            ASCII0, max_count)


class Environment(ProjectAgent):
    def __init__(self, process):
        ProjectAgent.__init__(self, process.project(), "%s:env" % process.name)
        self.copies = []
        self.variables = []
        if RUNNING_WINDOWS:
            self.copies.append('SYSTEMROOT')

    def add(self, variable):
        """
        Add a new EnvironmentVariable object.
        """
        self.variables.append(variable)

    def copy(self, name):
        """
        Add the name of the environment variable to copy.
        """
        if name in self.copies:
            return
        self.copies.append(name)

    def __getitem__(self, name):
        for var in self.variables:
            if var.hasName(name):
                return var
        raise KeyError('No environment variable: %r' % name)

    def create(self):
        """
        Create process environment variable dictionnary:
        name (str) => value (str).
        """
        env = {}

        # Copy some environment variables
        for name in self.copies:
            value = getenv(name)
            if value is not None:
                env[name] = value

        # Generate new variables
        for var in self.variables:
            for name, value in var.create():
                if not RUNNING_WINDOWS and name == "MALLOC_CHECK_" and value == '2':
                    log_func = self.info
                else:
                    log_func = self.warning
                log_func("Create %s (len=%s)" % (name, len(value)))
                if "\0" in value:
                    raise ValueError("Nul byte in environment variable value is forbidden!")
                env[name] = value

        # Write result to logs
        self.info("Environment=%r" % env)
        return env

