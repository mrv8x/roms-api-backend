from api.helpers.commits.github import GithubSearcher
from fastapi import APIRouter, Form

from api import (
    devices,
    telegraph,
    short_name,
    rom_pic_url,
    telegram,
    channel_name,
    support_group,
    firebase,
)
from api.models.common import APIResponse

router = APIRouter(prefix="/changelog")


@router.get("/device")
async def device_changelog(codename: str = Form(...)):
    codename = codename.lower()

    device = devices.get(codename)
    if not device:
        return APIResponse(status=404, message="DEVICE_NOT_FOUND")

    instance = GithubSearcher(codename)
    changelog = instance.get_changelog()
    response = telegraph.create_post(
        rom_name=short_name, device=codename, changelog=changelog, rom_pic=rom_pic_url
    )
    url = firebase.get_build_link(codename=codename, version="eleven")

    await telegram.send_message(
        chat_id=channel_name,
        device=codename,
        changelog_link=response,
        rom_name=short_name,
        group_name=support_group,
        download_link=url,
    )
    return changelog
