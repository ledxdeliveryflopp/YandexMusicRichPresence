import json
import os
from dataclasses import dataclass

from loguru import logger


@dataclass
class Settings:
    """Класс настроек api"""
    api_host: str = None
    api_port: int = None

    @staticmethod
    def init_settings() -> dict:
        settings_path_exist = os.path.exists(rf"{os.getcwd()}\discord\config\settings.json")
        settings_path = rf"{os.getcwd()}\discord\config\settings.json"
        logger.info(f"settings path exist: {settings_path_exist}")
        logger.info(f"getcwd: {os.getcwd()}")
        if settings_path_exist is False:
            with open(settings_path, "w") as file:
                data = {"host": "127.0.0.1", "port": 1111}
                json_data = json.dumps(data)
                file.write(json_data)
            return data
        else:
            with open(settings_path, "rb") as file:
                data = file.read()
                json_data = json.loads(data)
            return json_data


settings = Settings()
