from dataclasses import dataclass


@dataclass
class Folder():
    folder_id: int
    user_id: int
    name: str