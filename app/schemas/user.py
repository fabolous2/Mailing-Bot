from typing import Optional
from dataclasses import dataclass, field


@dataclass
class User():
    user_id: int
    email: Optional[str] = field(default=None)
    password: Optional[str] = field(default=None)