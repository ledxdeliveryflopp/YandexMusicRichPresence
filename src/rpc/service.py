from loguru import logger
from pypresence import AioPresence, DiscordNotFound, DiscordError


class RpcService(AioPresence):
    """Сервис Discord Rpc"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, client_id=1325723507975393372)

    async def rpc_reconnect(self) -> dict:
        logger.info("discord closed, trying reconnect")
        try:
            await self.connect()
            logger.info("reconnect successful")
            return {"detail": "success reconnect"}
        except (DiscordNotFound, DiscordError, BrokenPipeError) as exc:
            logger.error(f"reconnect to rpc error: {exc}")
            return {"detail": "failed reconnect"}


rpc_service = RpcService()
