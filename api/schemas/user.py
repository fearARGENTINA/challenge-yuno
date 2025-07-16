from pydantic import BaseModel, StrictStr
from typing import Optional
from config.config import Role

class UserSearch(BaseModel):
    username: StrictStr

class UserCreate(UserSearch):
    role: Role = Role.GUEST.name

class UserUpdate(BaseModel):
    role: Optional[Role]