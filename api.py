import json

from aiohttp import web
from rabbitFrame import PairSender, RPCSender


class Pair(web.View):
    async def post(self) -> web.Response:
        data = await self.request.json()
        sender = PairSender(data)
        sender.publish()
        return web.json_response(
            text='Data body sent successfully',
            status=201
        )

    async def put(self) -> web.Response:
        print('Jestem w put')
        raise web.HTTPNotImplemented()

    async def delete(self) -> web.Response:
        print('Jestem w delete')
        raise web.HTTPNotImplemented()


class PairGet(web.View):
    async def get(self) -> web.Response:
        key = self.request.match_info['key_name']
        print(key)
        sender = RPCSender()
        response = sender.call(key)
        print(response)

        return web.json_response(
            text=json.dumps(response.decode('utf-8')),
            status=200
        )
