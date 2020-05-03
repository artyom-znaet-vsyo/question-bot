from __future__ import annotations
from typing import Dict, NamedTuple, Optional, Union

from telegram.message import Message as TelegramMessage


class Question(NamedTuple):
    tg_user: str
    text: str
    group_id: int
    group_title: str

    def as_amplitude_fields(self) -> Dict[str, Union[str, int]]:
        return {
            "Question text": self.text,
            "tg user": self.tg_user,
            "tg group id": self.group_id,
            "tg group title": self.group_title,
        }

    @classmethod
    def from_updater_message(cls, message: TelegramMessage) -> Optional[Question]:
        if message.reply_to_message is None:
            return None
        return cls(
            tg_user=f'{message.from_user.full_name} (@{message.from_user.username})',
            text=message.reply_to_message.text,
            group_id=message.chat.id,
            group_title=message.chat.title,
        )
