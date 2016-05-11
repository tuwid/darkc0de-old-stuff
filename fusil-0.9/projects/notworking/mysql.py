"""
Generate random SQL requets to MySQL daemon
using "mysql" command line program.
"""

def setupProject(project):
    # Some options
    DEBUG = False
    USE_STDOUT = DEBUG
    sql = GenerateSQL(project, "sql")
    if DEBUG:
        sql.max_nb_instr = 1

    # Watch mysqld process
    mysqld = AttachProcess(project, 'mysqld')
    mysqld.max_memory = 300*1024*1024
    if USE_STDOUT:
        stdout = 'file'
    else:
        stdout = 'null'

    # MySQL client used to send fuzzy SQL
    process = MysqlProcess(project, ['/usr/bin/mysql'], stdout)
    WatchProcess(process, exitcode_score=0.15, timeout_score=0.15)
    if USE_STDOUT:
        stdout = WatchStdout(process)
        stdout.ignoreRegex('You have an error in your SQL syntax; check the manual')
        if not DEBUG:
            stdout.words['error'] = 0.10
        else:
            stdout.words['error'] = 1.0

    # Watch logs
    syslog = Syslog(project)
    mysql_log = FileWatch(project, open('/var/log/mysql/mysql.log'),
        'mysql.log', start="end")
    # FileWatch(project, open('/var/log/mysql/mysql.err'), 'mysql.err', start="end"),
    logs = [
        syslog.syslog, syslog.messages,
        mysql_log,
    ]
    for log in logs:
        log.words['mysqld'] = 1.0

from fusil.process.create import CreateProcess
from fusil.file_watch import FileWatch
from fusil.process.watch import WatchProcess
from fusil.process.attach import AttachProcess
from fusil.process.stdout import WatchStdout
from fusil.linux.syslog import Syslog
from fusil.project_agent import ProjectAgent
from fusil.bytes_generator import (BytesGenerator, IntegerGenerator, LengthGenerator,
    LETTERS, DECIMAL_DIGITS, PUNCTUATION)
from fusil.c_tools import quoteString
from random import choice, randint

class GenerateSQL(ProjectAgent):
    def __init__(self, project, name):
        ProjectAgent.__init__(self, project, name)
        self.smart_string_generator = BytesGenerator(0, 10,
            LETTERS | DECIMAL_DIGITS | set(' '))
        self.string_generator = BytesGenerator(0, 40,
            LETTERS | DECIMAL_DIGITS | PUNCTUATION)
        self.random_string_generator = BytesGenerator(0, 200)
        self.character_generator = BytesGenerator(1, 1)
        self.digit_generator = BytesGenerator(1, 30, DECIMAL_DIGITS)
        self.integer_generator = IntegerGenerator(11)
        self.printf_set = list(LETTERS | set('%'))
        self.long_string = LengthGenerator(10000)
        self.functions = list(set((
            # Tests
            'COALESCE', 'GREATEST', 'ISNULL', 'INTERVAL', 'LEAST',
            'IF', 'IFNULL', 'NULLIF', 'STRCMP',

            # Math
            'ABS', 'ACOS', 'ASIN', 'ATAN', 'ATAN2', 'CEILING', 'CEIL',
            'COS', 'COT', 'CRC32', 'DEGREES', 'EXP', 'FLOOR',
            'LN', 'LOG', 'LOG2', 'LOG10', 'MOD', 'PI', 'POW', 'POWER',
            'RADIANS', 'RAND', 'ROUND', 'SIGN', 'SQRT', 'TAN',
            'TRUNCATE',

            # String
            'ASCII', 'BIN', 'BIT_LENGTH', 'CHAR', 'CHAR_LENGTH',
            'COMPRESS', 'CONCAT', 'CONCAT_WS', 'CONV', 'ELT',
            'EXPORT_SET', 'FIELD', 'FIND_IN_SET', 'HEX', 'INSERT',
            'INSTR', 'LCASE', 'LEFT', 'LENGTH', 'LOAD_FILE', 'LOCATE',
            'LOWER', 'LPAD', 'LTRIM', 'MAKE_SET',
            'MID', 'OCTET_LENGTH', 'ORD', 'QUOTE', 'REPEAT', 'REPLACE',
            'REVERSE', 'RIGHT', 'RPAD', 'RTRIM', 'SOUNDEX', 'SPACE',
            'SUBSTRING', 'SUBSTRING_INDEX',
            'TRIM', 'UCASE', 'UNCOMPRESS', 'UNCOMPRESSED_LENGTH',
            'UNHEX', 'UPPER',

            # Date
            'ADDDATE', 'ADDTIME', 'CURDATE', 'CURRENT_DATE',
            'CURTIME', 'CURRENT_TIME', 'CURRENT_TIMESTAMP',
            'DATE', 'DATEDIFF', 'DATE_FORMAT', 'DAY', 'DAYNAME', 'DAYOFMONTH',
            'DAYOFWEEK', 'DAYOFYEAR', 'EXTRACT', 'FROM_DAYS', 'FROM_UNIXTIME',
            'GET_FORMAT', 'HOUR', 'LAST_DAY', 'LOCALTIME', 'LOCALTIMESTAMP',
            'MAKEDATE', 'MAKETIME', 'MICROSECOND', 'MINUTE', 'MONTH', 'MONTHNAME',
            'NOW', 'PERIOD_ADD', 'PERIOD_DIFF', 'QUARTER', 'SECOND',
            'SEC_TO_TIME', 'STR_TO_DATE', 'SUBDATE', 'SUBTIME', 'SYSDATE',
            'TIME', 'TIMEDIFF', 'TIMESTAMP', 'TIMESTAMPADD', 'TIMESTAMPDIFF',
            'TIME_FORMAT', 'TIME_TO_SEC', 'TO_DAYS', 'UNIX_TIMESTAMP',
            'UTC_DATE', 'UTC_TIME', 'UTC_TIMESTAMP', 'WEEK', 'WEEKDAY',
            'WEEKOFYEAR', 'YEAR', 'YEARWEEK',

            # Encryption
            'AES_DECRYPT', 'AES_ENCRYPT',
            'DECODE', 'ENCODE',
            'DES_DECRYPT', 'DES_ENCRYPT',
            'ENCRYPT', 'MD5', 'OLD_PASSWORD', 'PASSWORD',
            'SHA', 'SHA1',

            # Information
            'BENCHMARK', 'CHARSET', 'COERCIBILITY', 'COLLATION', 'CONNECTION_ID',
            'CURRENT_USER', 'DATABASE', 'FOUND_ROWS', 'LAST_INSERT_ID',
            'SESSION_USER', 'SYSTEM_USER', 'USER', 'VERSION',

            # Autres
            'BIT_COUNT', 'FORMAT', 'GET_LOCK', 'INET_ATON', 'INET_NTOA',
            'IS_FREE_LOCK', 'IS_USED_LOCK', 'MASTER_POS_WAIT', 'RELEASE_LOCK',
            'UUID',
        )))
        self.min_nb_arg = 0
        self.max_nb_arg = 4
        self.min_nb_instr = 1
        self.max_nb_instr = 3
        self.booleans = ('true', 'false')
        self.create_value = (
            self.createCharacter,
            self.createString,
            self.createSmartString,
            self.createRandomString,
            self.createInteger,
            self.createFloat,
            self.createNull, self.createBoolean,
            self.createPrintf,
#            self.createLength,
        )

    def createPrintf(self):
        count = randint(1, 20)
        format = ('%' + choice(self.printf_set) for index in xrange(count))
        value = ''.join(format)
        return quoteString(value)

    def createString(self):
        value = self.string_generator.createValue()
        return quoteString(value)

    def createSmartString(self):
        value = self.smart_string_generator.createValue()
        return quoteString(value)

    def createRandomString(self):
        value = self.random_string_generator.createValue()
        return quoteString(value)

    def createCharacter(self):
        value = self.character_generator.createValue()
        return quoteString(value)

    def createInteger(self):
        return self.integer_generator.createValue()

    def createFloat(self):
        return self.createInteger() + '.' + self.digit_generator.createValue()

    def createBoolean(self):
        return choice(self.booleans)

    def createNull(self):
        return 'NULL'

    def createValue(self):
        func = choice(self.create_value)
        return func()

    def createLength(self):
        return quoteString(self.long_string.createValue())

    def createFunction(self):
        function = choice(self.functions)
        sql = [function, '(']
        nb_arg = randint(self.min_nb_arg, self.max_nb_arg)
        for index in xrange(1, nb_arg+1):
            if 1 < index:
                sql.append(', ')
            value = self.createValue()
            sql.append(value)
        sql.append(')')
        return ''.join(sql)

    def createInstr(self):
        return 'SELECT %s;' % self.createFunction()

    def createSQL(self):
        sql = []
        nb_instr = randint(self.min_nb_instr, self.max_nb_instr)
        for index in xrange(nb_instr):
            sql.append(self.createInstr())
        sql.append('')
        return sql

    def on_session_start(self):
        sql = '\n'.join(self.createSQL())
        self.send('mysql_sql', sql)

class MysqlProcess(CreateProcess):
    def on_mysql_sql(self, sql):
        filename = self.project().session.directory.uniqueFilename('mysql.sql')
        open(filename, 'w').write(sql)
        self.popen_args['stdin'] = open(filename)
        self.createProcess()

    def deinit(self):
        CreateProcess.deinit(self)
        if 'stdin' in self.popen_args:
            del self.popen_args['stdin']

