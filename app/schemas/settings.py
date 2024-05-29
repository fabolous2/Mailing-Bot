from typing import Optional
from datetime import datetime

from dataclasses import dataclass, field


@dataclass
class Settings():
    id: int
    user_id: int
    folder_id: int
    subject: Optional[str] = field(default=None)
    text: Optional[str] = field(default=None)
