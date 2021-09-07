import os
import time

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from loguru import logger


class GoogleDriveTools:
    def __init__(self):
        self.__GDRIVE_DOWNLOAD_URL = "https://drive.google.com/uc?id={}&export=download"
        self.__GDRIVE_SCOPE = ["https://www.googleapis.com/auth/drive"]
        self.__authorize = self.authorize()

    def authorize(self):
        creds = None

        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file(
                "token.json", self.__GDRIVE_SCOPE
            )

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.__GDRIVE_SCOPE
                )
                creds = flow.run_console(port=0)
                logger.info("Succesfully saved token")
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return build("drive", "v3", cache_discovery=False, credentials=creds)

    def upload_file(self, cached_file, file_name, mime_type, drive_id, device) -> str:
        response = self.check_folders(device=device, drive_id=drive_id)

        if not response:
            logger.info(
                f"Folder for device {device} does not exist, creating it now..."
            )
            if self.create_folder(device=device, drive_id=drive_id):
                time.sleep(5)
                return self.upload_file(
                    cached_file=cached_file,
                    file_name=file_name,
                    mime_type=mime_type,
                    drive_id=drive_id,
                    device=device,
                )

        file_metadata = {
            "name": file_name,
            "description": "Derpfest ROM",
            "mimeType": mime_type,
            "parents": [response],
        }

        media_body = MediaFileUpload(cached_file, mimetype=mime_type, resumable=False)

        response = (
            self.__authorize.files()
            .create(supportsTeamDrives=True, body=file_metadata, media_body=media_body)
            .execute()
        )

        drive_file = (
            self.__authorize.files()
            .get(supportsTeamDrives=True, fileId=response["id"])
            .execute()
        )
        logger.info(
            f"Uploaded file {file_name} successfully! Removing it now from host."
        )
        os.remove(cached_file)

        return drive_file.get("id")

    def create_folder(self, device, drive_id):
        file_metadata = {
            "name": device,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [drive_id],
        }

        response = (
            self.__authorize.files()
            .create(body=file_metadata, fields="id", supportsTeamDrives=True)
            .execute()
        )

        return response.get("id", False)

    # https://stackoverflow.com/a/56532379
    def check_folders(self, device, drive_id):
        response = (
            self.__authorize.files()
            .list(
                q=f'name="{device}" and mimeType="application/vnd.google-apps.folder"',
                driveId=drive_id,
                spaces="drive",
                corpora="drive",
                includeItemsFromAllDrives=True,
                supportsAllDrives=True,
            )
            .execute()
        )
        return response.get("files", False)
