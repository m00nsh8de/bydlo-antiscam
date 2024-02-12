class Config:
    # Токен бота Telegram. Получите его от @BotFather в Telegram.
    BOT_TOKEN = "TOKEN"

    # Ключи API для OCR.space. Можно использовать несколько ключей для избежания ограничений по лимитам.
    OCR_API_KEYS = ["key1", "key2", "key3"]

    # Другие константы и настройки
    MAX_FRAME_SAMPLE_INTERVAL = 250  # Пример константы для обработки видеофайлов
    # Дополнительные константы и настройки можно добавлять по мере необходимости
    
    #URL Telegram Api для того чтобы бот кушал файлы больше 20 Мб
    #API_URL = 'https://localhost:8081'
    #API_URL = 'https://149.154.167.40:443'

# Это может быть полезно, если вы хотите иметь разные настройки для разработки и продакшена
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# Вы можете переключаться между DevelopmentConfig и ProductionConfig в зависимости от среды
current_config = DevelopmentConfig
