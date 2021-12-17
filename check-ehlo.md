# Test the connection and send an email
Once the Telnet client has been installed, follow the steps below to test email delivery.

1. Open a command prompt.
 
2. Type the following command: telnet <mail server name or IP> 25

  - You should receive output similar to the following:
220 remote.mailserveraddress.com ESMTP
NOTE: Once the telnet session is established, the Backspace and Delete keys do not work. If a typo is made, press Enter and retry the command. In some cases, it may be necessary to close the telnet session and reconnect.

  - If you receive an error similar to Could not open connection to the host, on port 25: Connect failed, this indicates that your machine could not establish a telnet session with the destination server using port 25. If you initially attempted to connect using the destination server's name, try to connect using its IP address instead. If this is successful, you likely have a DNS issue. If you are unable to connect using the destination server's name or IP address, port 25 is being blocked somewhere between your machine and the destination server. The issue is probably due to a firewall on the destination server's end, but it can also be caused by a network misconfiguration or firewall on your end.

  - If you receive output similar to the following:
554-remote.mailserveraddress.com
554 Your connection has been blocked due to low sender reputation...
Connection to host lost.
The public IP address associated with your mail server has developed a bad reputation. If you recently acquired this IP address, its previous owner likely sent spam from it, and your best option may be to request a different address from your ISP. If this is not feasible, there are other options, but there is not always a quick or easy solution to this issue. The error message may include additional instructions for resolving the issue. If not, this blog entry has a number of suggestions. Unfortunately, it may simply be a matter of waiting for your address's reputation to improve, and this can take considerable time.

3. Type: EHLO <mail server internet name>
  
    Replace <mail server internet name> with your mail server's public fully qualified domain name - for instance, mail.dell.com.
 
4. Type: mail from: <your_name@yourdomain.com> and press Enter.
 
5. Type: rcpt to: <recipient@recipientdomain.com> and press Enter.
 
6. Type: data and press Enter.
 
7. Type: Subject: <a subject here> and press Enter.
 
8. Type: This is a test message sent from telnet. and press Enter.
 
9. Type:  .   and press Enter
    The message should be accepted for delivery.
