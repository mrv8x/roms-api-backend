from typing import List, Optional
from pydantic import BaseModel


class DeviceVersion(BaseModel):
    version_code: str
    stable: bool


class Device(BaseModel):
    name: str
    brand: str
    codename: str
    supported_versions: List[DeviceVersion]
    img: str


class DevicesResponse(BaseModel):
    status: int
    message: List[Device]


class Build(BaseModel):
    changelog: str
    timestamp: float
    uploader_username: str
    link: Optional[str]
    id: str


class DeviceBuildsResponse(BaseModel):
    status: int
    message: List[Build]
