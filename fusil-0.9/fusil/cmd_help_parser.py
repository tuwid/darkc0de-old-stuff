import re

class Option:
    def __init__(self, format, nb_argument):
        self.format = format
        self.nb_argument = nb_argument

    def __str__(self):
        text = self.format
        arguments = tuple( ("ARG%s" % index) for index in xrange(1, self.nb_argument+1) )
        return text % arguments

class CommandHelpParser:
    def __init__(self):
        self.options = []

        # "-a", "-9" or "-C"
        SHORT_OPT_REGEX = r'-[a-zA-Z0-9]'

        # "-long", "-long-option" or "-Wunsued"
        LONG_OPT_REGEX = r'-[a-zA-Z][a-z-]+'

        # "--print" or "--very-long-option
        LONGLONG_OPT_REGEX = r'--[a-z][a-z-]+'

        # "value", "VALUE", "define:option" or "LONG_VALUE"
        VALUE_REGEX = '[a-zA-Z_:]+'

        # @ value@, @=value@, @,<value>@, @ "value"@, @[=value]@, ...
        VALUE_REGEX = r'[ =]%s|[ ,=]<%s>|[ =]"%s"|\[=%s\]' % (
            VALUE_REGEX, VALUE_REGEX, VALUE_REGEX, VALUE_REGEX)

        # -o
        # -o, --option
        # -o, --long-option=VALUE
        self.gnu_regex = re.compile(r'^\s+(%s), (%s)?(%s)?' %
            (SHORT_OPT_REGEX, LONGLONG_OPT_REGEX, VALUE_REGEX))

        # -option
        # -Long-option VALUE
        self.long_opt_regex = re.compile(r'^\s+(%s)(%s)?(%s)?' %
            (LONG_OPT_REGEX, VALUE_REGEX, VALUE_REGEX))

        # -C
        # -o VALUE
        # --option
        # --long-option=VALUE
        self.opt_regex = re.compile(r'^\s+(%s|%s)(%s)?' %
            (SHORT_OPT_REGEX, LONGLONG_OPT_REGEX, VALUE_REGEX))


    def addOption(self, name, *values):
        nb_arg = 0
        format = []
        for value in values:
            if not value:
                continue
            separator = value[0]
            if '"' in value:
                format.append( separator + '"%s"' )
            else:
                if separator == '[':
                    separator = value[1]
                format.append( separator + "%s" )
        nb_arg = len(format)
        format = name + ''.join(format)

        option = Option(format, nb_arg)
        self.options.append(option)

    def parseFile(self, stdout):
        for line in stdout:
            line = line.rstrip()

            match = self.gnu_regex.match(line)
            if match:
                name = match.group(1)
                value = match.group(3)
                self.addOption(name, value)

                name = match.group(2)
                if name:
                    self.addOption(name, value)
                continue

            match = self.long_opt_regex.match(line)
            if match:
                name = match.group(1)
                value = match.group(2)
                value2 = match.group(3)
                if value2:
                    self.addOption(name, value, value2)
                else:
                    self.addOption(name, value)
                continue

            match = self.opt_regex.match(line)
            if match:
                name = match.group(1)
                value = match.group(2)
                self.addOption(name, value)
                continue

