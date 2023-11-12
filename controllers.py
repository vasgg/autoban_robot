import time
from urllib.parse import urlparse
import logging
from aiogram import types, exceptions
from aiogram.enums import MessageEntityType

from config import allowed_groups, checked_hosts, settings


def validate_url(url: str) -> bool:

    if not url.startswith('http'):
        url = 'https://' + url
    parsed_url = urlparse(url)
    # проверяются ТОЛЬКО ссылки на домены из списка checked_hosts
    # ссылки на прочие домены пропускаются
    if parsed_url.hostname in checked_hosts:
        # разрешены ссылки ТОЛЬКО на группы из списка allowed_groups (добавляем /название группы)
        # будут забанены так же все ссылки на личные страницы и страницы ботов
        if parsed_url.path in allowed_groups:
            return True
        else:
            return False
    else:
        return True


async def ban_user(message: types.Message) -> None:
    logging.info("Trying to ban...")
    current_time = int(time.time())
    # прибавляем к текущему таймштампу время бана из .env в секундах (по умолчанию 1 неделя)
    until_date = current_time + settings.BAN_TIME
    # удаляем сообщение с рекламной ссылкой

    await message.delete()
    # тут можно не передавать параметр until_date, тогда бан будет навсегда
    # revoke_messages - это удаление всех сообщений этого пользователя из чата
    try:
        await message.bot.ban_chat_member(chat_id=message.chat.id,
                                          user_id=message.from_user.id,
                                          until_date=until_date,
                                          revoke_messages=True)
    except exceptions.TelegramBadRequest as e:
        logging.warning(f'Cant remove chat owner of admin. {e}')


def should_be_banned(entities: list[types.MessageEntity], text: str) -> bool:
    for entity in entities:
        if entity.type == MessageEntityType.TEXT_LINK:
            url = entity.url
        elif entity.type == MessageEntityType.URL:
            url = entity.extract_from(text)
        else:
            continue

        logging.info(f"Detected url: {url}")

        if not validate_url(url):
            return True

    return False
