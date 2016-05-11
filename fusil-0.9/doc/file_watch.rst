FileWatch
=========

FileWatch is a probe watch plain text file. It finds patterns in each
line of the file.

Constructor
-----------

Fake objects used for the documentation:

   >>> from fusil.mockup import Project, NullLogger
   >>> logger = NullLogger()
   >>> project = Project(logger)

Constructor syntax:

   >>> from fusil.file_watch import FileWatch
   >>> stderr = FileWatch(project, open('fusil.log'), 'stderr')

If you watch server log, use start="end" to skip existing logs:

   >>> syslog = FileWatch(project, open('fusil.log'), 'fusil.log', start='end')


Ignore lines
------------

Use ignoreRegex() method to ignore lines:

   >>> from re import IGNORECASE
   >>> stderr.ignoreRegex('^error: meaningless error')
   >>> stderr.ignoreRegex('^ErrOR: another error', IGNORECASE)

You can add your own ignore handler:

   >>> def ignoreNumber42(text):
   ...    try:
   ...       return int(text) == 42
   ...    except ValueError:
   ...       return False
   ...
   >>> stderr.ignore.append(ignoreNumber42)
   >>> ignoreEmptyLine = lambda line: len(line.strip()) == 0
   >>> stderr.ignore.append(ignoreEmptyLine)


Words patterns
--------------

'words' patterns are case insensitive and only match 'word'.
Example: "abc" pattern which match line "text: abc" but not "abcd".

FileWatch includes many text patterns in 'words' attribute:

   >>> words = stderr.words.keys()
   >>> from pprint import pprint
   >>> words.sort(); pprint(words)
   ['allocate',
    'assert',
    'assertion',
    'bug',
    "can't",
    'could not',
    'critical',
    'error',
    'exception',
    'failed',
    'failure',
    'fatal',
    'glibc detected',
    'invalid',
    'memory',
    'not allowed',
    'not valid',
    'oops',
    'overflow',
    'panic',
    'permission',
    'pointer',
    'segfault',
    'segmentation fault',
    'too large',
    'unknown',
    'warning']

Get/set pattern score:

   >>> print stderr.words['overflow']
   0.4
   >>> stderr.words['overflow'] = 0.5


Text patterns
-------------

'patterns' attribute is a dictionary of case insensitive text patterns:
text => score.

   >>> stderr.patterns[r'mplayer interrupted by signal [0-9]+'] = 1.0


Regex patterns
--------------

'regexs' attribute is a list of regex, use addRegex() to add a regex:

   >>> stderr.addRegex('^Crash: ', 1.0)
   >>> stderr.addRegex('null pointer$', 1.0, flags=IGNORECASE)


Patterns compilation
--------------------

All patterns are compiled by createRegex() method on agent initialisation.
It uses 'patterns' and 'words' attributes. Example:

   >>> stderr = FileWatch(project, open('fusil.log'), 'stderr')
   >>> stderr.words = {'error': 0.5}
   >>> stderr.patterns['mplayer'] = 1.0
   >>> for pattern, score, match in stderr.compilePatterns():
   ...     print "%r, score %.1f%%, regex=%s" % (pattern, score, match)
   ...
   'mplayer', score 1.0%, regex=...
   'error', score 0.5%, regex=...


Cleanup line
------------

You can register a function to cleanup lines:

   >>> stderr.cleanup_func = lambda text: text[7:]

Test of the function:

   >>> # Prepare test
   >>> stderr.init()
   >>> stderr.show_not_matching = True; logger.show = True
   >>> # Example of line
   >>> stderr.processLine('PREFIX:Real line content')
   Not matching line: 'Real line content'
   >>> # Empty line
   >>> stderr.processLine('PREFIX:')
   >>> # Cleanup test
   >>> stderr.show_not_matching = False; logger.show = False


Line number
-----------

'nb_line' contains the number of lines (without ignored lines) and
'total_line' the total number of lines. 'max_nb_line' attribute is the maximum
number of total lines: (max, score). If 'nb_line' becomes bigger than max,
score is incremented by score. Ignored lines are not included in 'nb_line'.
Default value:

    >>> stderr.max_nb_line
    (100, 1.0)

To disable the maximum of line number, set 'max_nb_line' to None.

There is a similar option for the minimum number of line, but it's disabled
by default (no minimum). Example to add -50% to the score if there is fewer
than 10 lines of output:

    >>> stderr.min_nb_line = (10, -0.5)


Pattern matching
----------------

For each text line, FileWatch calls processLine(). First it checks if the
line matchs one ignore pattern. If not, it tries all patterns and uses
the one with the biggest absolute score.

   >>> stderr.init()
   >>> stderr.processLine('This is an error')
   >>> print stderr.score
   0.5

Attributes:
 - show_matching (default: False): use True to show matching lines
   (use ERROR log level instead of WARNING)
 - show_not_matching (default: False): use True to show not matching lines
   (--debug option enable this option)
 - log_not_matching (default: False): use True to log not matching lines.
   By default, lines are not logged because the output is already
   written to session "stdout" file.

