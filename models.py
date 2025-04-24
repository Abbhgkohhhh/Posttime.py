# data/models.py
from dataclasses import dataclass, field

@dataclass
class Page:
    user_id: int
    username: str
    category: str
    desc: str
    products: str
    verified: bool = False
    scores: list = field(default_factory=list)
