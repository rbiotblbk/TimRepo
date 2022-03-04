from pathlib import Path
from logging.config import fileConfig

import logging
import json
import os

APP_FOLDER = Path(__file__).parent
os.chdir(APP_FOLDER)

with open("config.json", "r") as f:
    _config = json.load(f)

# Load the logger confiurations from 'loggin.ini'
fileConfig(_config["logger_config"], disable_existing_loggers=False)

# Get our logger
logger = logging.getLogger()
