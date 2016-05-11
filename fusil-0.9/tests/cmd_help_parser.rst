Setup tests
===========

>>> from os.path import join as path_join
>>> def openTest(name):
...     filename = path_join('tests', 'cmd_help', name)
...     return open(filename)
...
>>> from fusil.cmd_help_parser import CommandHelpParser
>>> from StringIO import StringIO

Test identify
=============

>>> identify = openTest('identify.help')
>>> parser = CommandHelpParser()
>>> parser.parseFile(identify)
>>> for option in parser.options:
...     print option
...
-authenticate ARG1
-channel ARG1
-crop ARG1
-debug ARG1
-define ARG1
-density ARG1
-depth ARG1
-extract ARG1
-format "ARG1"
-fuzz ARG1
-help
-interlace ARG1
-limit ARG1 ARG2
-list ARG1
-log ARG1
-matte
-monitor
-ping
-quiet
-sampling-factor ARG1
-set ARG1 ARG2
-size ARG1
-strip
-units ARG1
-verbose
-version
-virtual-pixel ARG1

Test gcc
========

>>> gcc = openTest('gcc.help')
>>> parser = CommandHelpParser()
>>> parser.parseFile(gcc)
>>> for option in parser.options:
...     print option
...
-pass-exit-codes
--help
--target-help
-dumpspecs
-dumpversion
-dumpmachine
-print-search-dirs
-print-libgcc-file-name
-print-file-name=ARG1
-print-prog-name=ARG1
-print-multi-directory
-print-multi-lib
-print-multi-os-directory ARG1 ARG2
-Wa,ARG1
-Wp,ARG1
-Wl,ARG1
-Xassembler ARG1
-Xpreprocessor ARG1
-Xlinker ARG1
-combine
-save-temps
-pipe
-time
-specs=ARG1
-std=ARG1
--sysroot=ARG1
-B ARG1
-b ARG1
-V ARG1
-v
-E
-S
-c
-o ARG1
-x ARG1


Test ls
=======

>>> ls = openTest('ls.help')
>>> parser = CommandHelpParser()
>>> parser.parseFile(ls)
>>> for option in parser.options:
...     print option
...
-a
--all
-A
--almost-all
--author
-b
--escape
--block-size=ARG1
-B
--ignore-backups
-c
-C
--color=ARG1
-d
--directory
-D
--dired
-f
-F
--classify
--file-type
--format=ARG1
--full-time
-g
-G
--no-group
-h
--human-readable
--si
-H
--dereference-command-line
--dereference-command-line-symlink-to-dir
--hide=ARG1
--indicator-style=ARG1
-i
--inode
-I=ARG1
--ignore=ARG1
-k
-l
-L
--dereference
-m
-n
--numeric-uid-gid
-N
--literal
-o
-p=ARG1
--indicator-style=ARG1
-q
--hide-control-chars
--show-control-chars
-Q
--quote-name
--quoting-style=ARG1
-r
--reverse
-R
--recursive
-s
--size
-S
--sort=ARG1
--time=ARG1
--time-style=ARG1
-t
-T=ARG1
--tabsize=ARG1
-u
-U
-v
-w=ARG1
--width=ARG1
-x
-X
-1
--lcontext
-Z
--context
--scontext
--help
--version

