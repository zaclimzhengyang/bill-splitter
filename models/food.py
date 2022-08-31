from pydantic import BaseModel
from typing import List

class Food(BaseModel):
    name: str
    price: float
    list_of_people: List[str]
