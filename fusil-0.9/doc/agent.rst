Agent
=====

An agent is an object able to send/receive messages to/from other agents.
Agents have a limited vision of the whole application: agents do not see them
each other. For pratical reasons, they have access to Application, Project and
Session objets.

Active or inactive
------------------

By default, an agent is inactive. It does not receive any event and is not
allowed to send messages. Calling activate() method does active then agent
and then call init() method. To disable an agent, use deactive() which
calls deinit() method.

Sum up of attributes and methods:

 - is_active: boolean
 - activate(): enable the agent, call init()
 - deactivate(): disable the agent, call deinit()
 - init(): create objects (eg. open file)
 - deinit(): destroy objects (eg. close file)

live()
------

When an agent is active, it's live() method is called at each session step.
The method have to be fastest as possible, so don't use any blocking
function (eg. select() before read()).

Events
------

Method related to message handling:
 - readMailbox(): read messages and call related agent event handler
 - send(event, \*arguments): send an event to other agents

You don't have to call readMailbox(), this job is done by
Session.executeObject().

To register to a message, just add a method to your class with the prototype::

   def on_EVENT(*arguments): ...

Example of method called on session start::

   def on_session_start():
       ...

Other attributes
-----------------

 - name (str): Agent name (should be unique in the whole application)
 - agent_id (int): Unique identifier in the whole application (basic integer counter)
 - logger: Logger object used by methods debug(), info(), ...
 - mailbox: Mailbox used to store message until readMailbox() is called

Logging
-------

To write string to logger, use methods:

 - debug(message): DEBUG level
 - info(message): INFO level
 - warning(message): WARNING level
 - error(message): ERROR level

Score
-----

ProjectAgent and SessionAgent have a method getScore() which return the agent
score. Default value is None (agent has no score). An agent has also
'score_weight' attribute (default value: 1.0) which is used to compute final
agent score:

   minmax(-1.0, agent.getScore() * agent.score_weight, 1.0)

