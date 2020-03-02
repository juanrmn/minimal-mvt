import sys
import signal
import asyncio
from aiohttp import web
import aiohttp_cors
import asyncpg
import logging
# TODO: logging...

# Database to connect to
DATABASE = {
    'user':     'postgres',
    'password': 'XXX',
    'host':     'XXX',
    'port':     '5432',
    'database': 'postgres'
}
TILES_TABLE = 'mvt_censustract'

async def get_pool(app):
    if app.get('db_pool'):
        return app['db_pool']
    else:
        app['db_pool'] = await asyncpg.create_pool(**DATABASE, loop=app.loop)
    return app['db_pool']

async def tile(request):
    z = request.match_info['z']
    x = request.match_info['x']
    y = request.match_info['y']
    logging.info(f'- Requested tile: {z}/{x}/{y}')

    sql = f'''SELECT mvt FROM {TILES_TABLE}
        WHERE z = {z} AND x = {x} AND y = {y};'''

    db_pool = await get_pool(request.app)
    async with db_pool.acquire() as conn:
        res = await conn.fetchval(sql)
        logging.info(f'+ serving tile: {z}/{x}/{y}')
        return web.Response(
            body=res,
            content_type='application/vnd.mapbox-vector-tile'
        )

async def create_app():
    app = web.Application()
    asyncio.set_event_loop(app.loop)

    app.add_routes([web.get('/{z}/{x}/{y}.{ext}', tile)])

    cors = aiohttp_cors.setup(app, defaults={
        '*': aiohttp_cors.ResourceOptions(
            allow_methods='*',
            allow_credentials=True,
            allow_headers='*',
            expose_headers='*'
        )
    })
    for route in app.router.routes():
        cors.add(route)

    return app


def main_exit_handler(*args, **kwargs):
    sys.exit(0)

signal.signal(signal.SIGTERM, main_exit_handler)


app = asyncio.run(create_app())

# ------ TODO: Run script with:
# gunicorn minimal-mvt-aiohttp:app -b localhost:8081 -w 1 --worker-class aiohttp.GunicornUVLoopWebWorker
