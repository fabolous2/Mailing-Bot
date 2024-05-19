from typing import Optional
from datetime import datetime

from dataclasses import dataclass, field


@dataclass
class Settings():
    id: int
    user_id: int
    audio_amount: Optional[int] = field(default=None)
    schedule: Optional[datetime] = field(default=None)
    subject: Optional[str] = field(default=None)
    text: Optional[str] = field(default=None)
    turned_on: Optional[bool] = field(default=False)
