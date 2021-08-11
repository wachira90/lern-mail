# postsuper command

Using Postfix postsuper command

postsuper is Postfix superintendent. This is command does maintenance jobs on the Postfix queue. Use of the postsuper command is restricted to the superuser of the Mail server. By default, postsuper performs the operations requested with the -s, and -p command-line options on all Postfix queue directories – this includes the incoming, active and deferred directories with mail files and the bounce, defer, trace and flush directories with log files.


## Command options:

### -d queue_id

Delete one message with the named queue ID from the named mail queue(s)
(default: hold, incoming, active and deferred).

### -h queue_id

Put mail “on hold” so that no attempt is made to deliver it. Move one message
with the named queue ID from the named mail queue(s) – (default: incoming, active and deferred) to the hold queue.

### -H queue_id

Release mail that was put “on hold”. Move one message with the named queue ID
from the named mail queue(s) – (default: hold) to the deferred queue.

### -r queue_id

Requeue the message with the named queue ID from the named mail queue(s)- (default: hold, incoming, active and deferred).


## Examples:

### Postfix hold all deferred messages
```
postsuper -h ALL deferred
```

### Postfix remove all messages on hold
```
postsuper -d ALL hold
```
This releases all mail that was put “on hold”


### Postfix release all messages on HOLD.
```
postsuper -H ALL
```
### Postfix dump all mails back to queue (Requeue)
```
postsuper -r ALL
```
(default: hold, incoming, active and deferred)

### Postfix purge old temporary files
```
postsuper -p
```

