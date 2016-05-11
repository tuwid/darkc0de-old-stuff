"""
Fuzzer for GNU libc environment variables.

Errors (?) with libc 2.5 and 2.6.1:
    MALLOC_TOP_PAD_: (len=38) '-8819591051163692829984324870324709886'
    LD_HWCAP_MASK: (len=31) '4604331229650750074196056802320'

GNU libc variable list:
    http://www.scratchbox.org/documentation/general/tutorials/glibcenv.html

Old advisories about unsecure variables:
 * 2000-09-01: NLSPATH
   Unix locale format string vulnerability
   http://www.coresecurity.com/index.php5?module=ContentMod&action=item&id=1067
 * 2003-12-30: LANG
   Xsok "LANG" Environment Variable Privilege Escalation Vulnerability
   http://secunia.com/advisories/10513/
 * 2007-07-05: LD_HWCAP_MASK integer overflow
   http://securitytracker.com/alerts/2007/Jul/1018334.html
 * MALLOC_TOP_PAD_: exploit
   http://www.synnergy.net/downloads/exploits/traceroute-exp.txt
 * 2007-11-07: LC_TIME: setlocale() exploit for aix 5.2 (CVE-2006-4254)
   http://www.milw0rm.com/exploits/4612

Disabled variables for SUID programs:
    __libc_init_secure(): elf/enbl-secure.c (__libc_enable_secure=1)
    UNSECURE_ENVVARS: sysdeps/generic/unsecvars.h
    EXTRA_UNSECURE_ENVVARS: sysdeps/unix/sysv/linux/i386/dl-librecon.h
"""

def setupProject(project):
    # Use non trival program to make sure that libc uses many environment variables
#    COMMAND = ['/bin/bash', '-c', 'echo "Hello World!"']
    COMMAND = ['python', '-c', 'print "Hello World!"']
    MAX_COUNT = 5

    # Run program with fuzzed environment variables
    vars = list(LIBC_VARIABLES)
    if False:
        # AVOID libc bugs
        vars.remove('LD_HWCAP_MASK')
        vars.remove('MALLOC_TOP_PAD_')
    if False:
        var = EnvVarInteger(vars, max_count=MAX_COUNT)
    elif False:
        var = EnvVarLength(vars, max_count=MAX_COUNT)
    elif False:
        var = EnvVarRandom(vars, max_length=200, max_count=MAX_COUNT)
        var.characters = LETTERS | PUNCTUATION
    else:
        var = EnvVarRandom(vars, max_length=2000, max_count=MAX_COUNT)
    process = ProjectProcess(project, COMMAND)
    process.env.add(var)

    # Watch process failure with its PID
    WatchProcess(process)

    # Watch process failure with its text output
    stdout = WatchStdout(process)
    stdout.words['failed'] = 0

from fusil.bytes_generator import LETTERS, PUNCTUATION
from fusil.process.env import EnvVarRandom, EnvVarInteger, EnvVarLength
from fusil.process.create import ProjectProcess
from fusil.process.watch import WatchProcess
from fusil.process.stdout import WatchStdout

# List generated from GNU libc 2.4 using shell command:
#    find -name "*.c"|xargs grep -H 'getenv *("'\
#    | sed 's/^.*getenv *("\([A-Z_0-9]*\)".*$/\1/'\
#    | sort -u
LIBC_VARIABLES = (
    'ARGP_HELP_FMT',
    'CHARSET',
    'COREFILE',
    'CRASHSERVER',
    'DATEMSK',
    'GCONV_PATH',
    'GETCONF_DIR',
    'GMON_OUT_PREFIX',
    'HES_DOMAIN',
    'HESIOD_CONFIG',
    'HOME',
    'HOSTALIASES',
    'HZ',
    'I18NPATH',
    'IFS',
    'LANG',
    'LANGUAGE',
    'LC_ALL',
    'LC_CTYPE',
    'LD_BIND_NOT',
    'LD_BIND_NOW',
    'LD_DYNAMIC_WEAK',
    'LD_HWCAP_MASK',
    'LD_LIBRARY_PATH',
    'LD_PROFILE_OUTPUT',
    'LD_WARN',
    'LIBC_FATAL_STDERR_',
    'LOCALDOMAIN',
    'LOCPATH',
    'MALLOC_CHECK_',
    'MALLOC_MMAP_MAX_',
    'MALLOC_MMAP_THRESHOLD_',
    'MALLOC_PERTURB_',
    'MALLOC_TOP_PAD_',
    'MALLOC_TRIM_THRESHOLD_',
    'MEMUSAGE_BUFFER_SIZE',
    'MEMUSAGE_NO_TIMER',
    'MEMUSAGE_OUTPUT',
    'MEMUSAGE_PROG_NAME',
    'MEMUSAGE_TRACE_MMAP',
    'MSGVERB',
    'NIS_DEFAULTS',
    'NIS_GROUP',
    'NIS_PATH',
    'NLSPATH',
    'OUTPUT_CHARSET',
    'PATH',
    'PCPROFILE_OUTPUT',
    'POSIXLY_CORRECT',
    'PWD',
    'RES_OPTIONS',
    'SEGFAULT_OUTPUT_NAME',
    'SEGFAULT_SIGNALS',
    'SEGFAULT_USE_ALTSTACK',
    'SEV_LEVEL',
    'SOMETHING_NOBODY_USES',
    'TIMEOUTFACTOR',
    'TMPDIR',
    'TZ',
    'TZDIR',
    'X',
    'XYZZY',
)

