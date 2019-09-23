# Sample Demo code for sending MIMEMutipart Email to SMTP endpoint
# This code uses smtplib library.
# Configurations to be done
# 1. HOST : IP address of HAProxy container
# 2. PORT : Port exposed by container (1587)
# 3. SENDER: Any registered email address
# 4. RECIPIENT: Any registered email address
# 5. USERNAME_SMTP: Username of SMTP server
# 6. PASSWORD_SMTP: Password of SMTP server


import datetime
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Replace sender@example.com with your "From" address.
# This address must be verified.

current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

SENDER = 'unmeshskulkarni@gmail.com'
SENDERNAME = 'Demo Admin'

# Replace recipient@example.com with a "To" address. If your account
# is still in the sandbox, this address must be verified.
RECIPIENT  = 'unmeshkulkarni@yahoo.com'

# Replace smtp_username with your Amazon SES SMTP user name.
USERNAME_SMTP = "AKIA6MQCY5C6XRQJCRPT"

# Replace smtp_password with your Amazon SES SMTP password.
PASSWORD_SMTP = "BEphH2TsztViYyE/cFIWg2LOGfKYQZ2+MrhvAyzV78HZ"

# (Optional) the name of a configuration set to use for this message.
# If you comment out this line, you also need to remove or comment out
# the "X-SES-CONFIGURATION-SET:" header below.
#CONFIGURATION_SET = "ConfigSet"

# If you're using Amazon SES in an AWS Region other than US West (Oregon),
# replace email-smtp.us-west-2.amazonaws.com with the Amazon SES SMTP
# endpoint in the appropriate region.

HOST = "10.20.60.42"
PORT = 1587
#HOST = "email-smtp.us-east-1.amazonaws.com"
#PORT = 587

# The subject line of the email.
SUBJECT = 'Orion Health Demo Email'

# The email body for recipients with non-HTML email clients.
BODY_TEXT = ("Orion SES Demo\r\n"
             "This email was sent through the Amazon SES SMTP"
             "Visit us at our website www.orionhealth.com"
            )

# The HTML body of the email.
BODY_HTML = """<html>
<head></head>
<body>
  <h1>Orion SES Demo</h1>
  <p> Current Time is {present_time}</p>
  <p>This email was sent through the Amazon SES SMTP. Please visit us at
    <a href='https://orionhealth.com/global/'>Orion Health</a>
  </p>
</body>
</html>
            """.format(present_time=current_time)

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = SUBJECT
msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
msg['To'] = RECIPIENT
# Comment or delete the next line if you are not using a configuration set
#msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)
# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(BODY_TEXT, 'plain')
part2 = MIMEText(BODY_HTML, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)

# Try to send the message.
try:
    server = smtplib.SMTP(HOST, PORT)
    server.ehlo()
    server.starttls()
    #stmplib docs recommend calling ehlo() before & after starttls()
    server.ehlo()
    server.login(USERNAME_SMTP, PASSWORD_SMTP)
    server.sendmail(SENDER, RECIPIENT, msg.as_string())
    server.close()
# Display an error message if something goes wrong.
except Exception as e:
    print ("Error: ", e)
else:
    print ("Email sent!")


