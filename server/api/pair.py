import typing as t
from aiohttp import web

from model import pair


PAIR_VALUES: t.List[pair.Pair] = []


class Pair(web.View):
    async def get(self) -> web.Response:
        global PAIR_VALUES
        return web.json_response(status=200)

    async def post(self) -> web.Response:

        data = await self.request.json()
        sender = pair.PairSender(data)
        sender.call()

        return web.json_response(text='Udało sie')

    async def put(self) -> web.Response:
        print('Jestem w put')
        raise web.HTTPNotImplemented()

    async def delete(self) -> web.Response:
        print('Jestem w delete')
        raise web.HTTPNotImplemented()