from __future__ import annotations
from typing import NamedTuple

import envparse


class BotConfig(NamedTuple):
    TOKEN: str

    @classmethod
    def from_env(cls) -> BotConfig:
        env = envparse.Env()
        return cls(TOKEN=env.str('ARTEM_BOT_TOKEN'))
