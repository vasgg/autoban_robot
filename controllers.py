import time
from urllib.parse import urlparse

from aiogram import types

from config import allowed_groups, checked_hosts, settings


def validate_url(url: str) -> bool:
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
    current_time = int(time.time())
    # прибавляем к текущему таймштампу время бана из .env в секундах (по умолчанию 1 неделя)
    until_date = current_time + settings.BAN_TIME
    # удаляем сообщение с рекламной ссылкой
    await message.delete()
    await message.answer('Ссылки на другие телеграм каналы запрещены!\n'
                         f'Пользователь <b>{message.from_user.full_name}</b> забанен!')
    # тут можно не передавать параметр until_date, тогда бан будет навсегда
    # revoke_messages - это удаление всех сообщений этого пользователя из чата
    await message.bot.ban_chat_member(chat_id=message.chat.id,
                                      user_id=message.from_user.id,
                                      until_date=until_date,
                                      revoke_messages=True)


async def parse_entities(message: types.Message) -> None:
    entities = message.entities
    if entities:
        for entity in entities:
            hidden_url = entity.url
            url = message.text[entity.offset:entity.offset + entity.length]
            if not validate_url(hidden_url) or not validate_url(url):
                await ban_user(message)
