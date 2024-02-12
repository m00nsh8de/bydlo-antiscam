import os
import logging
from aiogram import Bot

logger = logging.getLogger(__name__)

async def is_user_admin(bot: Bot, chat_id: int, user_id: int) -> bool:
    """
    Проверяет, является ли пользователь администратором чата.

    :param bot: Экземпляр бота.
    :param chat_id: ID чата.
    :param user_id: ID пользователя.
    :return: True, если пользователь является администратором, иначе False.
    """
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.is_chat_admin()
    except Exception as e:
        logger.error(f"Ошибка при проверке статуса администратора: {e}")
        return False

#async def send_notification_to_admins(bot: Bot, chat_id: int, notification_text: str):
async def send_notification_to_admins(bot, chat_id, notification_text):
    """
    Отправляет уведомление всем администраторам чата.

    :param bot: Экземпляр бота.
    :param chat_id: ID чата.
    :param notification_text: Текст уведомления.
    """
    try:
        admins = await bot.get_chat_administrators(chat_id)
        for admin in admins:
            try:
                await bot.send_message(admin.user.id, notification_text)
            except Exception as e:
                logger.error(f"Ошибка при отправке уведомления администратору {admin.user.id}: {e}")
    except Exception as e:
        logger.error(f"Ошибка при получении списка администраторов: {e}")

def ensure_directory_exists(path: str):
    """
    Создает директорию, если она не существует.

    :param path: Путь к директории.
    """
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f"Создана директория: {path}")
