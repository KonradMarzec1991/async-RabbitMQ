import os
import typing as t
from aiohttp import web
from asyncpg import pool


def setup(app: web.Application) -> None:
    print('Initialize db connection')
    app.cleanup_ctx.append(db_setup)


async def db_setup(app: web.Application) -> t.AsyncIterator[None]:
    app['db_poll'] = db_poll = await pool.create_pool(
        user=os.getenv('DB_USER', 'pair'),
        password=os.getenv('DB_PASSWORD', 'pair123'),
        database=os.getenv('DB_NAME', 'pair'),
        host=os.getenv('DB_HOST', '127.0.0.1'),
        port=int(os.getenv('DB_PORT', '5432')),
    )
    yield

    await db_poll.close()
