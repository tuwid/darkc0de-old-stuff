from ptrace.error import (PTRACE_ERRORS as FUSIL_ERRORS,
    writeBacktrace, formatError, writeError)

class FusilError(Exception):
    pass

