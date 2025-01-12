import time
from dataclasses import dataclass

from fastapi import HTTPException
from loguru import logger
from pypresence import ActivityType

from src.api.schemas import SetPlayPresenceSchemas, SetPausePresenceSchemas
from src.rpc.service import rpc_service


@dataclass
class BaseService:
    """Сервис установки активности"""
    test: float = None

    @staticmethod
    async def in_main_page_presence() -> dict:
        """Установка активности ожидания"""
        try:
            await rpc_service.update(activity_type=ActivityType.PLAYING,
                                     state="На главной странице", start=time.time(), large_image="main")
            logger.info(f"success set idle presence")
            return {"detail": "success"}
        except Exception as exc:
            logger.info(f"idle error: {exc}")
            raise HTTPException(detail="error while set idle presence", status_code=400)

    @staticmethod
    async def listen_music_presence(schemas: SetPlayPresenceSchemas) -> dict:
        """Установка активности проигрывания музыки"""
        try:
            if schemas.new is True:
                await rpc_service.update(activity_type=ActivityType.LISTENING, details=f"Слушает: {schemas.title}",
                                         state=f"Автор: {schemas.author}", start=time.time(),
                                         large_image=schemas.cover,
                                         small_image="main", end=time.time() + (schemas.duration / 1000))
                logger.info(f"success set new listen music presence")
                return {"detail": "success"}
            else:
                time_passed = (schemas.pause_timestamp - schemas.start_timestamp) / 1000
                await rpc_service.update(activity_type=ActivityType.LISTENING, details=f"Слушает: {schemas.title}",
                                         state=f"Автор: {schemas.author}", start=time.time(),
                                         large_image=schemas.cover,
                                         small_image="main", end=time.time() + (schemas.duration / 1000) - time_passed)
                logger.info(f"success set old listen music presence")
                return {"detail": "success"}
        except Exception as exc:
            logger.info(f"listen music error: {exc}")
            raise HTTPException(detail="error while set music listen presence", status_code=400)

    @staticmethod
    async def pause_listen_music_presence(schemas: SetPausePresenceSchemas) -> dict:
        """Установка активности постановки музыки на паузу"""
        try:
            await rpc_service.update(activity_type=ActivityType.LISTENING, details=f"На паузе: {schemas.title}",
                                     state=f"Автор: {schemas.author}", large_image=schemas.cover, start=time.time(),
                                     small_image="main")
            logger.info(f"success set pause music presence")
            return {"detail": "success"}
        except Exception as exc:
            logger.info(f"pause music error: {exc}")
            raise HTTPException(detail="error while set music pause presence", status_code=400)


async def init_service():
    return BaseService()
