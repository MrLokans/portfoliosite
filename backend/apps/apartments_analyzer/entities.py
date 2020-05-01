from dataclasses import dataclass
from typing import Optional


@dataclass
class TelegramUserData:
    id: int
    username: Optional[str]
    last_name: Optional[str]
    first_name: Optional[str]

    def possible_username(self):
        if self.username:
            return f"@{self.username}"
        return f"{self.first_name or 'Unknown'} {self.last_name or 'Unknown'}"
