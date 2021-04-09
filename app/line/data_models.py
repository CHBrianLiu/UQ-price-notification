from typing import Dict, List, Union

from pydantic import BaseModel


class LineRequest(BaseModel):
    destination: str
    events: List[Dict[str, Union[str, dict]]]
