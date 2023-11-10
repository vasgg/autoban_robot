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
    await parse_entities(message)


def main():
    bot = Bot(token=settings.BOT_TOKEN.get_secret_value(), parse_mode='HTML')
    dispatcher = Dispatcher()
    dispatcher.include_routers(router)
    dispatcher.run_polling(bot)


if __name__ == '__main__':
    main()
