from email.mime import base
from BaseClasses.BaseSender import Sender
from os.path import basename
from pathlib import Path
from ftplib import FTP

import config
import json

logger = config.logger


class FTPSender(Sender):
    def __init__(self, file: str) -> None:
        """
        Create a FTPSender Object

        Used to send scraped HTML Files to a FTP Server
        The configuration is stored in ftp.json

        Args:
            file (str): Filename of the corresponding HTML File to be send
        """

        super().__init__()

        with open("ftp.json", "r") as f:
            self.ftp_config = json.load(f)

        self.file = file

        self.FTP_SERVER = self.ftp_config["ftp_server"]
        self.FTP_USER = self.ftp_config["ftp_user"]
        self.FTP_PASS = self.ftp_config["ftp_pass"]

        self.FTP_DIR_NAME = self.ftp_config["dir_name"]

        self.ftp = FTP(self.FTP_SERVER)
        self.ftp.login(self.FTP_USER, self.FTP_PASS)

        self.ftp.cwd(self.FTP_DIR_NAME)

    def get_config(self) -> dict:
        """
        Returns the data loaded from ftp.json

        Returns:
            dict: data loaded from ftp.json
        """

        return self.ftp_config

    def send(self) -> bool:
        """
        Send the file to the FTP Server specified in ftp.json

        Returns:
            bool: True on Success, otherwise False
        """

        try:
            self.ftp.storbinary("STOR " + basename(self.file),
                                open(self.file, "rb"))

            logger.info("Sent Successfully!")

            return True

        except Exception as e:
            logger.info("Could not send to FTP!. \n ", e)

            return False
