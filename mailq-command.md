# mail command

To check current active  mail queue, use the command:

```
$ mailq
```

Get email accounts with high Postfix queues

```
$ mailq | grep ^[A-F0-9] | cut -c 42-80 | sort | uniq -c | sort -n | tail
```
