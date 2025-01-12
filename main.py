import os
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from loguru import logger
from pypresence import DiscordNotFound

from src.api.router import handler_router
from src.rpc.service import rpc_service
from src.settings.settings import settings


@asynccontextmanager
async def lifespan(api: FastAPI):
    """Подключение к discord rpc при запуске"""
    try:
        await rpc_service.connect()
        logger.info("connected to rpc")
    except DiscordNotFound as exc:
        logger.error(f"connecting to rpc error: {exc}")
        sys.exit()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(handler_router)


def run_api(api_host: str, api_port: int) -> None:
    try:
        uvicorn.run(app, host=api_host, port=api_port)
    except Exception as exc:
        logger.error(f"Error while starting api: {exc}")


if __name__ == '__main__':
    logger.add(rf"{os.getcwd()}\discord\rich-presence.log", rotation="100 MB",
               format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}")
    api_settings = settings.init_settings()
    host = api_settings.get("host")
    port = api_settings.get("port")
    run_api(f"{host}", port)

