from __future__ import annotations

from typing import NamedTuple

import envparse


class AirtableConfig(NamedTuple):
    API_URL: str
    API_SECRET: str

    @classmethod
    def from_env(cls) -> AirtableConfig:
        env = envparse.Env()
        return cls(API_URL=env.str('AIRTABLE_API_URL'), API_SECRET=env.str('AIRTABLE_API_SECRET'))

    @property
    def headers(self):
        return {'Authorization': f'Bearer {self.API_SECRET}', 'Content-Type': 'application/json'}


class BotConfig(NamedTuple):
    TOKEN: str

    @classmethod
    def from_env(cls) -> BotConfig:
        env = envparse.Env()
        return cls(TOKEN=env.str('ARTEM_BOT_TOKEN'))
