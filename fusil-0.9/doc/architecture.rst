Fusil architecture
==================

Fusil is a multi-agent system (MAS): it uses simple objets called "agents"
exchanging messages though asynchronus "message (mail) transfer agent" (MTA).
This architecture allows the whole project to be very modular and very
customisable.

Each agent have a live() method called at each session "step", but also event
handler. An event has a name and may contains arguments. The name is used in
agent method name: eg. "on_session_start()" method is called when the session
starts.

Some agents do change the environment and some other watchs for errors and
strange behaviour of programs.


Action agents
=============

 * CreateProcess: create a process
 * StdoutFile: created by CreateProcess to store
   process output
 * MangleFile: generate an invalid file using valid file
 * AutoMangle: MangleFile with autoconfiguration based on aggressivity factor

Network:

 * NetworkClient / NetworkServer: network client / server
 * TcpClient: TCP network client
 * UnixSocketClient: UNIX socket client
 * HttpServer: HTTP server

Probes
======

 * FileWatch: watch a text file, search specific text patterns
   like "segmentation fault"
 * CpuProbe: watch CPU used by the process
   created by CreateProcess
 * ProcessTimeWatch: watch process
   execution duration
 * WatchStdout: watch process output (stdout)
 * WatchProcess: watch process created by CreateProcess
 * AttachProcess: watch running process
 * Syslog: watch /var/log/messages and /var/log/syslog files

