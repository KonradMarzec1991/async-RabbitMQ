"""
API module contains two controllers for GET/POST web methods
"""
import json

from aiohttp import web
from rabbitFrame import BaseSender
from rpc_models import RPCSender


class PairGet(web.View):
    """
    `PairGet` View class implements GET method which:
    - gets url key_name
    - creates `RPCSender` instance and call it with url key_name
    - gets server response and display it
    """
    async def get(self) -> web.Response:
        key = self.request.match_info['key_name']
        sender = RPCSender()
        response = sender.call(key)
        return web.json_response(
            text=json.dumps(response.decode('utf-8')),
            status=200
        )


class PairPost(web.View):
    """
    `PairPost` View class implements POST method which:
    - creates `PairSender` instance and run its `publish` method
    - display json response with 201 if data sent correctly
    """
    async def post(self) -> web.Response:
        data = await self.request.json()
        sender = BaseSender(data)
        sender.publish()
        return web.json_response(
            text='Data body sent successfully',
            status=201
        )
