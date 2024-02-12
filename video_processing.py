import cv2
import os
import logging
from ocr_space import ocr_space_file
from config import Config

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def process_video_frames(file_path, banned_words):
    logger.debug(f"Начало обработки видео: {file_path}")

    frames_dir = '/tmp/videos/frames'
    os.makedirs(frames_dir, exist_ok=True)

    cap = cv2.VideoCapture(file_path)
    frame_count = 0
    recognized_text = ""

    while True:
        ret, frame = cap.read()
        if not ret:
            logger.debug("Все кадры видео обработаны или видео закончилось.")
            break

        if frame_count % Config.MAX_FRAME_SAMPLE_INTERVAL == 0:
            frame_path = os.path.join(frames_dir, f'temp_frame_{frame_count}.jpg')
            cv2.imwrite(frame_path, frame)
            logger.debug(f"Обработан кадр №{frame_count}, файл сохранен как: {frame_path}")

            text = ocr_space_file(frame_path, Config.OCR_API_KEYS[0])
            os.remove(frame_path)
            logger.debug(f"Текст, распознанный на кадре №{frame_count}: {text}")

            if any(banned_word in text for banned_word in banned_words):
                recognized_text = text
                logger.debug(f"Найдено запрещенное слово в кадре №{frame_count}.")
                break

        frame_count += 1

    cap.release()
    logger.debug("Завершение обработки видео.")
    return recognized_text
