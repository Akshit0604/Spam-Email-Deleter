import imaplib
import email
import re
import smtplib
from email.mime.text import MIMEText

# Login to your Gmail account
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('your.email@gmail.com', 'application password')

# Select the mailbox you want to delete emails from
mail.select('inbox')

inspect_mails = ['example1@gmail.com', 'example2@gmail.com'] #email ids to be inspected
keep_unless_contains = ['important', 'urgent'] #phrases to be checked
#============mails from emails in inspect_mails will be deleted unless they contain phrases in keep_unless_contains==================== 

search_query = ' OR '.join([f'FROM {sender}' for sender in inspect_mails])
typ, data = mail.search(None, search_query)

# Loop through the emails and delete them
deleted_emails = []
for num in data[0].split():
    typ, msg_data = mail.fetch(num, '(RFC822)')
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            subject = msg['subject']
            from_email = re.search(r'<([^>]+)>', msg['from']).group(1) if re.search(r'<([^>]+)>', msg['from']) else msg['from']
            is_inspect_mail = from_email in inspect_mails

            should_delete = False

            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True).decode('utf-8')
                    if is_inspect_mail and not any(phrase.lower() in body.lower() for phrase in keep_unless_contains):
                        should_delete = True
                        break

            if should_delete:
                mail.store(num, '+X-GM-LABELS', '\\Trash')
                deleted_emails.append(f"Subject: {subject}, Sender: {msg['from']}")

# Permanently remove the deleted emails
mail.expunge()

# Close the mailbox and logout
mail.close()
mail.logout()

# Send email report
smtp_server = 'smtp.gmail.com'
smtp_port = 587
username = 'your.email@gmail.com'
password = 'application password'
sender = 'your.email@gmail.com'
recipient = 'your.email@gmail.com'

server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(username, password)

# Compose the email message
msg = MIMEText('The following emails were deleted:\n\n' + '\n'.join(deleted_emails))
msg['Subject'] = 'Deleted Emails Report'
msg['From'] = sender
msg['To'] = recipient

# Send the email
server.sendmail(sender, recipient, msg.as_string())
server.quit()
