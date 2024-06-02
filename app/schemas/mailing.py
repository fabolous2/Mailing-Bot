import datetime
from dataclasses import dataclass, field


@dataclass
class Mailing():
    job_id: int
    folder_id: int
    user_id: int
    scheduled_time: datetime.datetime
    is_active: bool = field(default=True)
