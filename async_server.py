import time
import asyncio

from aiohttp import web
from aiojobs.aiohttp import spawn, setup

from settings.settings import DJANGO_SERVER_URL
from apps.telegram.controllers import AsyncTelegramController

routes = web.RouteTableDef()
controller = AsyncTelegramController(str(DJANGO_SERVER_URL))


async def logger(request):
    print(f"[{time.ctime()}]: {request}")


async def get_event_loop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        return asyncio.get_running_loop()


@routes.get('/')
async def main(request):
    await spawn(request, logger(request))
    await controller.create_client_session()
    await controller.start_session()
    return web.json_response({"status": 200})


if __name__ == '__main__':
    application = web.Application()
    application.add_routes(routes)
    setup(application)
    web.run_app(application, port=8888)
