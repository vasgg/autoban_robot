import logging

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ContentType
from aiogram.filters import CommandStart

from config import settings
from controllers import should_be_banned, ban_user

router = Router()


@router.message(CommandStart())
async def start_message(message: types.Message) -> None:
    await message.answer(
        text='Привет. Я — бот, который выписывает бан за публикацию ссылок на другие каналы в телеграм.')


@router.message()
async def process_messages(message: types.Message):
    logging.info(message.model_dump_json(exclude_none=True))
    if message.from_user.id in settings.ADMINS:
        logging.info('IS ADMIN MESSAGE')
        return

    if message.from_user.full_name == 'Telegram':
        logging.info('Message from Channel')
        return

    if message.content_type == ContentType.TEXT:
        entities = message.entities
        text = message.text
    else:
        entities = message.caption_entities
        text = message.caption

    if entities and should_be_banned(entities, text):
        await ban_user(message)


def main():
    bot = Bot(token=settings.BOT_TOKEN.get_secret_value(), parse_mode='HTML')
    dispatcher = Dispatcher()
    dispatcher.include_routers(router)
    dispatcher.run_polling(bot)


if __name__ == '__main__':
    main()
