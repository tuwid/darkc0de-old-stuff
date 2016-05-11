Create your process
===================

Today, Fusil only supports UNIX process.

system()
--------

system() function from fusil.process.system is just a wrapper to os.system():
it does raise a RuntimeError() if the command failed (exit code is not nul).

CreateProcess and ProjectProcess
--------------------------------

This action class does prepare the environment for a process and then use
subprocess.Popen() to create the process object.

ProjectProcess creates the process with 'session_start()' event whereas
CreateProcess have to be inherited to add your own session handler calling
self.createProcess() method.

Attributes:
 * env: Environment() object used to create environment variables
 * stdout: Stdout type:
   - 'file' (default): stdout is written in a file
   - 'null': redirect output to /dev/null
 * cmdline: CommandLine() object used to create the command line
 * timeout: maximum execution duration of the process in second (default: 10
   second). If the timeout is reached, the process is directly killed with
   SIGKILL signal. Use None value to disable timeout.
 * max_memory: Limit of memory grow in bytes (default: 100 MB). Use None value
   to disable memory limitation.
 * popen_args: Dictionary of supplementary options to Popen() constructor
   (default: see source code).

By default, stderr output is written to stdout: stdout and stderr are the same
file. Example:

   >>> from fusil.mockup import Project
   >>> project = Project()
   >>> from fusil.process.create import CreateProcess
   >>> null_stdout = CreateProcess(project, ['/bin/ls', '-lR'],
   ...     stdout='null', timeout=None)
   ...


Environment
-----------

This class is responsible to create new process environment variables. It
does copy some variables from Fusil environment and allow to set/generate some
others. On Linux, no variable is copied. On Windows, only SYSTSEMROOT is
copied. You may copy variables like LANGUAGE, LANG, PATH, HOME or DISPLAY
using:

   env.copy('DISPLAY')

To set/generate a variable, use on of these classes:

 * EnvVarValue: fixed value
 * EnvVarLength: generate long value to find buffer overflow. Attributes:
 * EnvVarInteger: generate signed integer value
 * EnvVarRandom: generate random bytes, use all byte values except nul byte
   (forbidden in environment variable value)

Attributes (EnvVarValue has only name attribute):

 * name: Variable name, it can be a list
 * min_length: Minimum number of bytes (default: 0)
 * max_length: Maximum number of bytes (default: 2000)
 * bytes: bytes set (default: set('A'))

Variable name is a string but it can be a tuple or list of strings. Example:

   env.add(EnvVarValue('LANGUAGE', 'fr'))
   env.add(EnvVarLength('PATH'))
   env.add(EnvVarRandom('HOME'))
   env.add(EnvVarInteger(['COLUMNS', 'SIZE']))


Command line
------------

CreateProcess object has cmdline attribute of type CommandLine. This object
has only one attribute: arguments which is a list of string.


Linux graphical application (X11)
---------------------------------

To be able to use a graphical application on Linux, you need HOME
and DISPLAY environment variables. Copy them using:

  >>> process.env.copy('DISPLAY')
  >>> process.env.copy('HOME')


Watch process activity
======================

WatchProcessPID
---------------

This class waits for process death using waitpid(). It uses waitpid() status
to compute the probe score:

 - if exit code is nul, score is 'default_score' (default: 0%)
 - if exit code is not nul, score is 'exitcode_score' (default: 50%)
 - if process has been killed by a signal, score is 'signal_score'
   (default: 100%)

WatchProcess
------------

WatchProcess inherits on WatchProcessPID but takes a CreateProces object in
constructor. If process time has been reached, probe score is: 'timeout_score'
(default: 100%).

WatchProcessStdout
------------------

WatchProcessStdout inherits on FileWatch: it looks for error message patterns
in process stdout (and stderr if process is configured to write stderr to
stdout).

CPU load probe: CpuProbe
========================

AttachProcess and WatchProcessPID have 'cpu' attribute of type CpuLoad.
If CPU load is bigger than maximum load during maximum duration, set
score to 'max_score' (default: 100%). Default values:

   >>> from fusil.mockup import Project
   >>> project = Project()
   >>> from fusil.process.cpu_probe import CpuProbe
   >>> probe = CpuProbe(project, 'cpu')
   >>> probe.max_load
   0.90
   >>> probe.max_duration
   5.0
   >>> probe.max_score
   1.0

