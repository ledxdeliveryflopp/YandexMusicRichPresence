from fastapi import APIRouter, Depends
from src.api.schemas import SetPlayPresenceSchemas, SetPausePresenceSchemas
from src.api.service import BaseService, init_service

handler_router = APIRouter(prefix='/handler')


@handler_router.get("/idle/")
async def in_main_page_router(service: BaseService = Depends(init_service)):
    return await service.in_main_page_presence()


@handler_router.post("/listen-music/")
async def listen_music_router(schemas: SetPlayPresenceSchemas,
                              service: BaseService = Depends(init_service)):
    return await service.listen_music_presence(schemas)


@handler_router.post("/pause-music/")
async def pause_music_router(schemas: SetPausePresenceSchemas,
                             service: BaseService = Depends(init_service)):
    return await service.pause_listen_music_presence(schemas)
