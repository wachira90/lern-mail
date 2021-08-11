# postqueue command

Using Postfix postqueue command.
postqueue – This is a Postfix queue control tool. The postqueue command implements the Postfix user interface for queue management. It implements operations that are traditionally available via the sendmail command. postqueue command options:

parameter
```
-f  
```
Flush the queue: attempt to deliver all queued mail.
```
-i queue_id 
```
Schedule immediate delivery of deferred mail with the specified queue ID.
```
-j
```
Produce a queue listing in JSON format, based on the output from the showq daemon
```
-p
```
Produce a traditional sendmail-style queue listing. This option implements
the traditional mailq command, by contacting the Postfix showq daemon.The queue ID string is followed by an optional status character:
```
* –> The message is in the active queue, i.e. the message is selected for delivery.

!  –> The message is in the hold queue, i.e. no further delivery attempt will be made until the
```

Flushing queue with postqueue:
```
postqueue -f
```
Print  postfix queue in sendmail-style:
```
postqueue -p
```

Postfix print queue in JSON format
```
postqueue -j
```
Have fun using Postfix Commands Administration Cheat Sheet, drop comments for any commands you often use when working with Postfix Relay servers. I’ll be happy to update this list with any new item.


