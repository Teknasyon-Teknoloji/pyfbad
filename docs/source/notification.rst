Notification
=============

pyfbad.notification.notifications.Email
----------------------------------------

  >>> send_gmail(self, mygmailusername, mygmailpassword, to_gmail_address, subject=None, content=None)
Send an email from gmail account to gmail account.

**mygmailusername (str):** The account to which the mail will sent from

**mygmailpassword (str):** The password to which the mail will sent from

**to_gmail_address (str):** The account to which the mail will sent to

**subject (str):** The mail subject, optional

**content (str):** The mail content, optional

pyfbad.notification.notifications.Slack
----------------------------------------
  >>> slack_notification(url, content='')
Send a slack notification to channel.

**url (str):** The account access url

**content (str):** The notification content, optional
