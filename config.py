from dotenv import load_dotenv
import os

# Загружаем переменные окружения из файла .env
load_dotenv()

class Config:
    def __init__(self):
        # Чтение переменных окружения
        self.token_host = os.getenv('API_TOKEN_HOST')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        self.group_id = os.getenv("GROUP_ID")

# Пример использования
config = Config()
# print(config.token_host)  # Выводит токен из .env
