import json
import requests
import pandas as pd
import yagmail

class Email:
    def __init__(self) -> None:
        pass

    def send_gmail(self, mygmailusername, mygmailpassword, to_gmail_address, subject=None, content=None):
        """ Send an email from gmail account to gmail account.
        Args:
            mygmailusername (str): The account to which the mail will sent from
            mygmailpassword (str): The password to which the mail will sent from
            to_gmail_address (str): The account to which the mail will sent to
            subject (str): The mail subject, optional
            content (str): The mail content, optional
        """
        try:
            yag = yagmail.SMTP(mygmailusername, mygmailpassword)
        except:
            print("The SMTP connection couldn't be successfull. Please check your gmail account settings.")

        if content==None:
            content = "Anomaly allert!.."
        if subject==None:
            subject = "Anomaly Detected"
        try:
            yag.send(to_gmail_address, subject, content)
        except:
            print("Something went wrong when the email sending.")

class Slack:

    def slack_notification(url, content=''):
        """ Send a slack notification to channel.
        Args:
            url (str): The account access url
            content (str): The notification content, optional
        """
        if content=='':
            content = {
                "username": "AnomalyDetectionBot",
                #"icon_emoji": ":robot_face:",
                "attachments": [
                    {
                        "color": "#1eb0e2",
                        "fields": [
                            {

                                "short": "false",
                            }
                        ]
                    }
                ]
            }

        headers = {'Content-Type': "application/json"}
        response = requests.post(url, data=json.dumps(content), headers=headers)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)