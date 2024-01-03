# Spam-Email-Deleter
A python script to delete emails from ids indicated as spam unless they have some key phrases in them

# How to Use
1) Enable 2 factor-authentication on your email id
2) Generate an application password for your email id (can be done from manage your google account>security>application passwords)
3) Pip install secure-smtplib
4) Fill in your email id and application password into the python file
5) Fill in the spam email ids and phrases that will keep the mails
6) run the script

The script will also send you a mail containing details of the deleted emails. Deleted emails will be moved to trash and not permanently deleted.
