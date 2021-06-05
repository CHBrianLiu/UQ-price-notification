from typing import Set

from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    count_tracking: int
    product_tracking: Set[str]
