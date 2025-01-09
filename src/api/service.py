import time
from dataclasses import dataclass

from fastapi import HTTPException
from loguru import logger

from src.rpc.service import rpc_service


@dataclass
class BaseService:
    start_time: float = time.time()

    async def in_main_page_presence(self) -> dict:
        try:
            await rpc_service.update(state="На главной странице", start=self.start_time, large_image="main")
            logger.info(f"success set idle presence")
            return {"detail": "success"}
        except Exception as exc:
            logger.info(f"idle error: {exc}")
            raise HTTPException(detail="error while set idle presence", status_code=400)

    async def listen_music_presence(self) -> dict:
        try:
            await rpc_service.update(state="Слушает музыку", start=self.start_time, large_image="main")
            logger.info(f"success set listen music presence")
            return {"detail": "success"}
        except Exception as exc:
            logger.info(f"listen music error: {exc}")
            raise HTTPException(detail="error while set music listen presence", status_code=400)


async def init_service():
    return BaseService()
