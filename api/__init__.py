import yaml
import os
import magic
import shutil

from fastapi import FastAPI
from github import Github
from loguru import logger

from api.helpers.configs.devices import DevicesConfig
from api.helpers.firebase.firebase import FirebaseDatabase
from api.helpers.telegraph.telegraph import TelegraphPost
from api.helpers.telegram.telegram import Telegram
from api.helpers.gdrive.gdrive import GoogleDriveTools

gdrive = GoogleDriveTools()
app = FastAPI(redoc_url=None, docs_url=None, openapi_url=None)
config: dict = None
mime = magic.Magic(mime=True)

working_dir = os.getcwd()
tmp_path = f"{working_dir}/api/tmp/"
firebase_cert = f"{working_dir}/firebase_credentials.json"

with open("config.yaml", "r") as config_file:
    config = yaml.load(config_file.read(), Loader=yaml.FullLoader)

devices_url = config["core"]["devices_url"]

devices = DevicesConfig(devices_url=devices_url)

with open("devices.yaml", "r") as device:
    device_config = yaml.load(device.read(), Loader=yaml.FullLoader)

github_instance = Github(config["core"]["github_token"])
drive_id = config["core"]["drive_id"]
firebase_project_id = config["core"]["firebase_project_id"]
firebase_collection_user = config["core"]["firebase_collection_user"]
firebase_collection_admin = config["core"]["firebase_collection_admin"]
firebase_rldb = config["core"]["firebase_rldb"]
rldb_builds = config["core"]["firebase_rldb_builds_db"]
firebase_rldb_commits_db = config["core"]["firebase_rldb_commits_db"]
rom_pic_url = config["core"]["rom_pic_url"]
short_name = config["core"]["rom_name"]
author_name = config["core"]["author_name"]
buttons = config["core"]["buttons"]
channel_name = config["core"]["channel_name"]
support_group = config["core"]["support_group"]
telegram_token = config["core"]["telegram_token"]

firebase = FirebaseDatabase(
    firebase_cert=firebase_cert,
    project_id=firebase_project_id,
    firebase_rldb=firebase_rldb,
    rldb_builds=rldb_builds,
)

telegraph = TelegraphPost(short_name=short_name, author_name=author_name)

telegram = Telegram(
    bot_token=telegram_token,
    rom_pic_url=rom_pic_url,
    buttons=buttons,
    config=device_config,
)

logger.add("backend.log", rotation="1 week")
logger.info("Cleaning up directories")
if os.path.isdir("api/tmp"):
    shutil.rmtree("api/tmp")
os.mkdir("api/tmp")


from api.main import main  # noqa: E402

main()
