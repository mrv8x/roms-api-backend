from firebase_admin import credentials, firestore, db
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


from loguru import logger

import os
import yaml
import firebase_admin
import uuid
import sys

config = yaml.load(open('config.yaml'), Loader=yaml.FullLoader)
working_dir = os.getcwd()
tmp_path = f"{working_dir}/api/tmp/"
firebase_cert = f"{working_dir}/firebase_credentials.json"
firebase_project_id = config["core"]["firebase_project_id"]
firebase_collection_admin = config["core"]["firebase_collection_admin"]
__GDRIVE_SCOPE = ["https://www.googleapis.com/auth/drive"]

cred = credentials.Certificate(firebase_cert)
firebase_admin.initialize_app(cred, {"projectId": firebase_project_id})
db = firestore.client()


def authorize():
    creds = None

    if os.path.exists("token.json"):
        logger.info("Token already exists!")
        creds = Credentials.from_authorized_user_file(
            "token.json", __GDRIVE_SCOPE
        )

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", __GDRIVE_SCOPE
            )
            creds = flow.run_console(port=0)
            logger.info("Succesfully saved token")
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())


def add_admin():
    device = sys.argv[1]
    username = sys.argv[2]
    token = uuid.uuid4().hex
    data = {"devices": device, "token": token}

    db.collection(firebase_collection_admin).document(username).set(data)
    logger.info(f"Successfully added user {username} with device {device}\nwith token: {token}")


if len(sys.argv) > 1:
    add_admin()
else:
    authorize()
