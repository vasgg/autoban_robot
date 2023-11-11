import logging

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart

from config import settings
from controllers import parse_entities

router = Router()


@router.message(CommandStart())
async def start_message(message: types.Message) -> None:
    await message.answer(
        text='Привет. Я — бот, который выписывает бан за публикацию ссылок на другие каналы в телеграм.')


@router.message()
async def process_messages(message: types.Message):
    logging.info('is topic message: ', message.is_topic_message)
    logging.info('message_thread_id: ', message.message_thread_id)
    logging.info('forward_from_chat:', message.forward_from_chat)
    logging.info('forward_from:', message.forward_from)
    logging.info('chat', message.chat)
    logging.info('chat_shared: ', message.chat_shared)
    if message.from_user.id not in settings.ADMINS:
        await parse_entities(message)
    else:
        print('IS ADMIN MESSAGE')


def main():
    bot = Bot(token=settings.BOT_TOKEN.get_secret_value(), parse_mode='HTML')
    dispatcher = Dispatcher()
    dispatcher.include_routers(router)
    dispatcher.run_polling(bot)


if __name__ == '__main__':
    main()
