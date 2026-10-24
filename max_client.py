"""
Клиент для работы с API платформы МАКС.
Содержит базовую конфигурацию HTTPX-клиента и функции для отправки сообщений.
"""
import os
import httpx
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
import urllib3

# Отключаем предупреждения о самоподписанных сертификатах (специфика среды тестирования)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Загружаем переменные окружения из .env в корне проекта
load_dotenv()

TOKEN = os.getenv("MAX_BOT_TOKEN", "default_token")
BASE_URL = os.getenv("MAX_API_BASE", "https://platform-api2.maks.app")

# Инициализация HTTP-клиента
client = httpx.Client(
    headers={"Authorization": TOKEN, "Content-Type": "application/json"},
    verify=False,
    timeout=30.0
)

def send_message(chat_id: str, text: str, keyboard: Optional[List[List[Dict[str, str]]]] = None) -> Optional[httpx.Response]:
    """
    Отправляет текстовое сообщение в чат, опционально прикрепляя inline-клавиатуру.
    
    :param chat_id: Идентификатор чата (получателя) в системе МАКС.
    :param text: Текст отправляемого сообщения.
    :param keyboard: Двумерный массив кнопок для inline-клавиатуры.
    :return: Объект ответа httpx.Response или None в случае ошибки сети/API.
    """
    payload: Dict[str, Any] = {"text": text}
    if keyboard:
        payload["attachments"] = [
            {
                "type": "inline_keyboard",
                "payload": {"buttons": keyboard}
            }
        ]
    
    try:
        resp = client.post(f"{BASE_URL}/messages", params={"chat_id": chat_id}, json=payload)
        resp.raise_for_status()
        return resp
    except Exception as e:
        print(f"[ERROR] Ошибка отправки сообщения в чат {chat_id}: {e}")
        return None
