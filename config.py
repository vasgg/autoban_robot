import logging

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    BAN_TIME: int
    ADMINS: list[int]
    CHANNEL_CHAT_ID: int

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s: "
    "%(filename)s: "
    "%(levelname)s: "
    "%(funcName)s(): "
    "%(lineno)d:\t"
    "%(message)s",
)


checked_hosts = ['t.me', ]
allowed_groups = ['/test_group_with_ban', ]
