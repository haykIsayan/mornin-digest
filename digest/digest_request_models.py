from pydantic import BaseModel
from typing import List


class MorninRequest(BaseModel):
    topics: List[str]
