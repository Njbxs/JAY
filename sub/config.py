#
# Copyright (C) 2023 by stereoproject
# All rights reserved.

import os

from dotenv import load_dotenv

load_dotenv(".env")

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
MONGO_URL = os.environ.get("MONGO_URL")
ADMINS = [int(x) for x in (os.environ.get("ADMINS", "").split())]
MEMBER = [int(x) for x in (os.environ.get("MEMBER", "").split())]
LOG_GRP = int(os.environ.get("LOG_GRP"))
BOT_ID = int(os.environ.get("BOT_ID"))
