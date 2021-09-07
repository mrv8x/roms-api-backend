from pydantic import BaseModel


class APIResponse(BaseModel):
    status: int
    message: str
