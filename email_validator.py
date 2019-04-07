import socket
import smtplib

import re
import dns.resolver


addressToVerify ='user@domain.com'
match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)

if match == None:
        print('Bad Syntax')
        raise ValueError('Bad Syntax')

records = dns.resolver.query('domain.com', 'MX')
mxRecord = records[0].exchange
mxRecord = str(mxRecord)

# Get local server hostname
host = socket.gethostname()

# SMTP lib setup (use debug level for full output)
server = smtplib.SMTP()
server.set_debuglevel(0)

# SMTP Conversation
server.connect(mxRecord)
server.helo(host)
server.mail('user@domain.com')
code, message = server.rcpt(str(addressToVerify))
server.quit()

# Assume 250 as Success
if code == 250:
        print('This is a perfectly working email address')
else:
        print('This Email address does not work. Check again with the person who gave you these details!')
