from aiogram import types
from database import DatabaseManager
from utils import is_user_admin

async def handle_command(message: types.Message, db_manager: DatabaseManager):
    """
    Обрабатывает команды администратора.

    :param message: Объект сообщения от aiogram.
    :param db_manager: Экземпляр менеджера базы данных.
    """
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Проверка, является ли пользователь администратором
    if not await is_user_admin(message.bot, chat_id, user_id):
    #if not await is_user_admin(bot, chat_id, user_id):
        await message.reply("Только администраторы могут использовать эти команды.")
        return

    command, *args = message.get_full_command()

    if command == '/addword':
        await add_banned_word(message, args, db_manager)
    elif command == '/delword':
        await remove_banned_word(message, args, db_manager)
    elif command == '/listwords':
        await list_banned_words(message, db_manager)
    elif command == '/help':
        await show_help_command(message)

async def add_banned_word(message: types.Message, args: list, db_manager: DatabaseManager):
    if args:
        word_to_add = args[0]
        db_manager.add_banned_word(word_to_add)
        await message.reply(f"Слово '{word_to_add}' добавлено в список запрещенных.")
    else:
        await message.reply("Пожалуйста, укажите слово для добавления. Пример: /addword спам")

async def remove_banned_word(message: types.Message, args: list, db_manager: DatabaseManager):
    if args:
        word_to_remove = args[0]
        db_manager.remove_banned_word(word_to_remove)
        await message.reply(f"Слово '{word_to_remove}' удалено из списка запрещенных.")
    else:
        await message.reply("Пожалуйста, укажите слово для удаления. Пример: /delword спам")

async def list_banned_words(message: types.Message, db_manager: DatabaseManager):
    banned_words = db_manager.get_banned_words()
    if banned_words:
        words_list = ', '.join(banned_words)
        await message.reply(f"Список запрещенных слов: {words_list}")
    else:
        await message.reply("В настоящее время запрещенных слов нет.")


async def show_help_command(message: types.Message):
    help_text = (
        "Вот список доступных команд:\n\n"
        "/addword <слово> - Добавить слово в список запрещенных.\n"
        "/delword <слово> - Удалить слово из списка запрещенных.\n"
        "/listwords - Показать список запрещенных слов.\n"
        "/help - Показать это справочное сообщение.\n"
    )
    await message.reply(help_text)