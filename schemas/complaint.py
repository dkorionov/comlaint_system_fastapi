from datetime import datetime

from pydantic import BaseModel
from models.complaint import State


class BaseComplaint(BaseModel):
    title: str
    description: str
    amount: float


class ComplaintIN(BaseComplaint):
    encoded_image: str
    extension: str


class ComplaintOUT(BaseComplaint):
    id: int
    photo_url: str
    created_at: datetime
    updated_at: datetime
    state: State
    complainer_id: int
