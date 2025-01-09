from fastapi import APIRouter, Depends

from src.api.service import BaseService, init_service

handler_router = APIRouter(prefix='/handler')


@handler_router.get("/idle/")
async def in_main_page_router(service: BaseService = Depends(init_service)):
    return await service.in_main_page_presence()


@handler_router.get("/listen-music/")
async def listen_music_router(music_cover_url: str, service: BaseService = Depends(init_service)):
    return await service.listen_music_presence(music_cover_url)
