from typing import List
from pydantic import BaseModel


class AddUserRequest(BaseModel):
    name: str
    admin: str
    devices: List[str]
    token: str


class UserAddResponse(BaseModel):
    devices: List[str]
    token: str


class AddUserResponse(BaseModel):
    status: int
    message: UserAddResponse


class DelUserRequest(BaseModel):
    token: str
    name: str
    admin: str
