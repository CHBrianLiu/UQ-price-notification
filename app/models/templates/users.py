from typing import List, TypedDict


class UsersTemplate(TypedDict):
    user_id: str
    count_tracking: int
    product_tracking: List[str]


template = UsersTemplate(user_id="", count_tracking=0, product_tracking=[])
