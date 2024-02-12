import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from config import Config
from database import DatabaseManager
from ocr_space import ocr_space_file
from video_processing import process_video_frames
from utils import ensure_directory_exists, send_notification_to_admins, is_user_admin
from admin_commands import handle_command

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher(bot)

# Ensure the directories for temporary files exist
ensure_directory_exists('tmp/photos')
ensure_directory_exists('tmp/videos')

# Database manager for banned words
db_manager = DatabaseManager()

# OCR API keys
ocr_api_keys = Config.OCR_API_KEYS

# Download file from Telegram

async def download_file(bot, file_id, media_type):
    file = await bot.get_file(file_id)
    file_path = file.file_path
    local_file_path = os.path.join('tmp', media_type, file_path.split('/')[-1])

    if not os.path.exists(os.path.dirname(local_file_path)):
        os.makedirs(os.path.dirname(local_file_path))

    await bot.download_file(file_path, destination=local_file_path)
    return local_file_path

@dp.message_handler(content_types=[types.ContentType.PHOTO, types.ContentType.VIDEO])
async def handle_media_message(message: types.Message):
#    chat_id = message.chat.id
    user_id = message.from_user.id
    chat_id = message.chat.id
#    chat_title = message.chat.title or "Неизвестный чат"
    chat_title = message.chat.title or message.chat.id
    user = message.from_user
    user_identity = user.username or f"{user.first_name} {user.last_name or ''} {user.id}"

    if await is_user_admin(bot, chat_id, user_id):
        logger.debug("Admin message, skipping.")
        return

    media_type = 'photos' if message.photo else 'videos'
    file_id = message.photo[-1].file_id if message.photo else message.video.file_id
    local_file_path = await download_file(bot, file_id, media_type)

    banned_words = db_manager.get_banned_words()

    if media_type == 'videos':
        recognized_text = process_video_frames(local_file_path, banned_words)
        if recognized_text:
            await bot.delete_message(chat_id, message.message_id)
#            await bot.kick_chat_member(chat_id, user_id)
    else:
        # Обработка фотографий
        recognized_text = ocr_space_file(local_file_path, Config.OCR_API_KEYS[0])
        # Удаление временного файла фотографии
        if os.path.exists(local_file_path):
            os.remove(local_file_path)

    # Проверка распознанного текста на наличие запрещенных слов
    if recognized_text:
        for banned_word in banned_words:
            if banned_word in recognized_text:
                # Отправляем уведомление администраторам
                notification_text = f"Обнаружено запрещенное слово '{banned_word}' в сообщении от {user_identity} в чате '{chat_title}'."
                await send_notification_to_admins(bot, chat_id, notification_text)
                # Логика удаления сообщения и бана пользователя
                await bot.delete_message(chat_id, message.message_id)
                #await bot.kick_chat_member(chat_id, user_id)
                break



# Command handlers for admin commands
@dp.message_handler(commands=['addword', 'delword', 'listwords', 'help'])
async def admin_commands(message: types.Message):
    await handle_command(message, db_manager)

# Start the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
