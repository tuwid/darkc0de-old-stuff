setrlimit
=========

Linux limits:
 * RLIMIT_AS: maximum size of the process’s virtual memory in bytes.
 * RLIMIT_CORE: Maximum size of core file.
 * RLIMIT_CPU: CPU  time  limit  in  seconds.
 * RLIMIT_FSIZE: Maximum  size of files that the process may create.
 * RLIMIT_LOCKS: Combined number of flock() locks and fcntl() leases
 * RLIMIT_MEMLOCK: Maximum number of bytes of memory that may be locked into RAM.
 * RLIMIT_MSGQUEUE: Limit on the number of bytes that can be allocated for POSIX message queues
 * RLIMIT_NICE: Ceiling to which the process’s nice value can be raised
 * RLIMIT_NOFILE: Value one greater than the maximum file descriptor number that can be opened by this process.
 * RLIMIT_NPROC: The  maximum  number  of  processes  that can be created
 * RLIMIT_RTPRIO: Ceiling  on  the real-time priority
 * RLIMIT_SIGPENDING:  Limit on the number of signals that may be queued
 * RLIMIT_STACK: Maximum size of the process stack in bytes

Useless limits (no supported by Linux kernel):
 * RLIMIT_DATA
 * RLIMIT_RSS

