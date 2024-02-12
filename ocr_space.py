import requests
from config import Config


def ocr_space_file(filename, api_key, language='rus', ocr_engine=3):
    """
    OCR.space API запрос с локальным файлом.

    :param filename: Путь к файлу для OCR.
    :param api_key: Ключ API OCR.space.
    :param language: Язык текста на изображении.
    :param ocr_engine: Версия OCR движка.
    :return: Распознанный текст.
    """
    payload = {
        'isOverlayRequired': True,
        'apikey': api_key,
        'language': language,
        'OCREngine': ocr_engine
    }
    with open(filename, 'rb') as f:
        response = requests.post('https://api.ocr.space/parse/image',
                                 files={filename: f},
                                 data=payload)
    return response.content.decode()
