Multi agent system (MAS)
========================

Univers agent is responsible to execute all agents. Univers is stopped using
univers_stop() event.

A session can be stopped using session_stop() event.

Main MAS events:

 * project_start(): event received at first step but only for the first
   session of a project
 * session_start(): event received at first step on a session
 * session_done(score): event received at the last step of a session

