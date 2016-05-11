Scoring system
==============

Problematic
-----------

Guess a fuzzing session success or failure is a complex task. We can use
different parameters like process exit code, stdout, session duration, etc.
But for each project, the meaning of the values may change. For some projects,
session timeout is a success whereas you may ignore timeout for other
projects.

Fusil probes
------------

That's why Fusil use a scoring system. You can use multiple "probes" and each
probe compute its own score. Session score is the sum of all scores. A probe
score is a value between -1.0 and 1.0 where:

 * 1.0 is a success (eg. program crash)
 * 0.0 means "nothing special"
 * -1.0 means that the application just rejects your input, you may
   try next session with less noise

Each probe score is normalized in -1.0..1.0 interval. Session score is not
normalized, 130% value is allowed.

You can also set a probe "weight" ('score_weight' attribute, default value:
1.0) to change its importance in session score (see example above).

Example
-------

Let's take a project with 4 probes:
 * WatchProcess(A)
 * WatchProcess(B)
 * TimeWatch: weight=0.5 (less important)
 * FileWatch: weight=2 (more important)

At the end of the session, the scores are:
 * WatchProcess(A): score=0.25
 * WatchProcess(B): score=None (no score)
 * TimeWatch: score=-0.10
 * FileWatch: score=0.15

Session score is::

   0.25 + -0.10 * 0.5 + 0.15 * 2 = 0.50

Since minimum score for a success is 'project.success_score' (default: 50%),
we can say that the session is a success!

