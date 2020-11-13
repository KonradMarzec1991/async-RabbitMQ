from aiohttp import web
from rabbit import rabbitFrame


class Pair(web.View):
    async def get(self) -> web.Response:
        return web.json_response(status=200)

    async def post(self) -> web.Response:

        data = await self.request.json()
        sender = rabbitFrame.PairSender(data)
        sender.call()

        return web.json_response(text='Udało sie')

    async def put(self) -> web.Response:
        print('Jestem w put')
        raise web.HTTPNotImplemented()

    async def delete(self) -> web.Response:
        print('Jestem w delete')
        raise web.HTTPNotImplemented()
