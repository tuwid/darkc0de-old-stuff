Time managment
==============

Session timeout
---------------

You can set maximum session duration using Project.session_timeout option
(value in second). If session reachs the timeout, it's stopped.

Logging
-------

Messages are written with a timestamp.

TimeWatch
---------

To compute session score, you can use TimeWatch probe. It has two parameters:

 * too_fast: mininum duration of a valid session, faster session would have
   'too_fast_score' score (default: -100%)
 * too_long: maximum duration of a valid session, slower session would have
   'too_long_score' score (default: 100%)

Process
-------

A process have a default timeout set to 10 seconds. If the timeout is reached,
the process is directly killed using SIGKILL signal and WatchProcess will use
its 'timeout_score' attribute as score (default: 100%).

