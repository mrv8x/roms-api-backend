import shutil
import time

from fastapi import APIRouter, File, UploadFile, Form

from .. import (
    tmp_path,
    mime,
    drive_id,
    firebase,
    firebase_collection_user,
    devices,
    telegraph,
    short_name,
    rom_pic_url,
    telegram,
    channel_name,
    support_group,
)


from ..helpers.utils.utils import run_sync
from ..models.common import APIResponse
from api.helpers.commits.github import GithubSearcher

router = APIRouter(prefix="/api")


@router.post("/upload")
async def get_uploads(
    token: str = Form(...),
    codename: str = Form(...),
    version: str = Form(...),
    username: str = Form(...),
    file: UploadFile = File(...),
):
    codename = codename.lower()
    user = firebase.get_user(username=username, collection=firebase_collection_user)
    device = devices.get(codename)
    if isinstance(user.to_dict(), dict):
        if token not in user.to_dict()["token"] or not device:
            return APIResponse(status=404, message="USER_NOT_FOUND")
    else:
        return APIResponse(status=404, message="USER_NOT_FOUND")

    instance = GithubSearcher(codename)
    changelog = instance.get_changelog()
    response = telegraph.create_post(
        rom_name=short_name, device=codename, changelog=changelog, rom_pic=rom_pic_url
    )

    from ..helpers.gdrive.gdrive import GoogleDriveTools

    gdrive = GoogleDriveTools()

    cached_file = f"{tmp_path}{file.filename}"

    with open(cached_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    mime_type = mime.from_file(cached_file)

    file_id = await run_sync(
        gdrive.upload_file,
        cached_file=cached_file,
        file_name=file.filename,
        mime_type=mime_type,
        drive_id=drive_id,
        device=codename,
    )

    firebase.add_build(
        file_id=file_id,
        time=time.time(),
        username=username,
        version=version,
        codename=codename,
        changelog=response,
    )

    download_link = f"https://drive.google.com/uc?export=download&id={file_id}"

    await telegram.send_message(
        chat_id=channel_name,
        device=codename,
        changelog_link=response,
        rom_name=short_name,
        group_name=support_group,
        download_link=download_link,
    )

    return APIResponse(status=200, message="SUCCESS")
