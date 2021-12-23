# Restrict Postfix SMTP Relay (smtpd_relay_restrictions)

- Access restrictions for mail relay control that the Postfix SMTP server applies in the context of the `RCPT TO` command, before `smtpd_recipient_restrictions`
- With Postfix versions before 2.10, the rules for relay permission and spam blocking were combined under `smtpd_recipient_restrictions`, resulting in error-prone configuration
- As of Postfix 2.10, relay permission rules are preferably implemented with `smtpd_relay_restrictions`, so that a permissive spam blocking policy under `smtpd_recipient_restrictions` will no longer result in a permissive mail relay policy.

## By default, the Postfix SMTP server accepts:

- Mail from clients whose IP address matches `$mynetworks`, or:
- Mail to remote destinations that match `$relay_domains`, except for addresses that contain sender-specified routing `(user@elsewhere@domain)`, or:
- Mail to local destinations that match `$inet_interfaces` or `$proxy_interfaces`, `$mydestination`,`$virtual_alias_domains`, or `$virtual_mailbox_domains`.
