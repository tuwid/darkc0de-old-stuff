Fusil events
============

An event can only be sent once in a session step (eg. you can not send session_stop
event twice).

Application:

 - application_done(): Fusil is done (exit)
 - application_interrupt(): Ask Fusil application to stop
 - application_error(message): Fatal Fusil error

Project:

 - project_start(): Creation of the project
 - project_stop(): Ask to stop active project
 - project_session_destroy(): Destroy session and create a new session
   if we are not done

Session:

 - session_start(): Creation of a new session
 - session_stop(): Ask session to stop
 - session_done(score): End of the active session, score is the
   final session score

Aggressivity:

 - aggressivity_value(value): New aggressivity value with -1.0 <= value <= 1.0

Process:

 - process_create(agent): New process created
 - process_stdout(agent, file_obj): Process stdout file object is available
 - process_done(agent, status): Process finished (exited or killed by as signal)
 - process_pid(agent, pid): Attached process identifier

MangleFile:

 - mangle_filenames(filenames): Generated filenames

