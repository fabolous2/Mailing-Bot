from dataclasses import dataclass, field


@dataclass
class Email():
    id: int
    user_id: int
    email: str
    folder_id: int
    sendments: int = field(default=0)
    