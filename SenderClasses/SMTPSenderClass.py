from BaseClasses.BaseSender import Sender
from os.path import basename
from pathlib import Path

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

import smtplib
import config
import json

logger = config.logger


class SMTPSender(Sender):
    def __init__(self, file: str) -> None:
        """
        Create a SMTPSender Object

        Used to send scraped HTML Files to a gmail account
        The configuration is stored in email.json

        Args:
            file (str): Filename of the corresponding HTML File to be send
        """

        super().__init__()

        with open("email.json", "r") as f:
            self.email_config = json.load(f)

        self.gmail_user = self.email_config["gmail_user"]
        self.gmail_password = self.email_config["gmail_pass"]

        self.message = MIMEMultipart()

        # Email Meta Data
        self.message["from"] = self.gmail_user
        self.message["to"] = self.gmail_user
        self.message["subject"] = "Scraped HTML Files"

        # Body
        self.message.attach(MIMEText("Upload of the scraped HTML files"))

        with open(file, "rb") as f:
            part = MIMEApplication(
                f.read(),
                Name=basename(file)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(
            file)
        self.message.attach(part)

        # logger.debug(f"Build HTMLParser with file '{file}'")

    def get_config(self) -> dict:
        """
        Returns the data loaded from email.json

        Returns:
            dict: data loaded from email.json
        """

        return self.email_config

    def send(self) -> bool:
        """
        Send the file to the gmail account specified in email.json

        Returns:
            bool: True on Success, otherwise False
        """

        try:
            with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
                smtp.ehlo()  # Start connection
                smtp.starttls()
                smtp.login(self.gmail_user, self.gmail_password)
                smtp.send_message(self.message)

            logger.info("Sent Successfully!")

            return True

        except Exception as e:
            logger.info("Could not send email!. \n ", e)

            return False
