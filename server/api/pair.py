import typing as t
from aiohttp import web
import pydantic as pd

from model import pair
from .utils import if_duplicated, compress_to_dict


PAIR_VALUES: t.List[pair.Pair] = []


class Pair(web.View):
    async def get(self) -> web.Response:
        global PAIR_VALUES
        return web.json_response(status=200, data=compress_to_dict(PAIR_VALUES))

    async def post(self) -> web.Response:
        global PAIR_VALUES

        try:
            new_pair = pair.Pair.parse_obj(await self.request.json())
            if if_duplicated(new_pair, PAIR_VALUES):
                raise web.HTTPConflict(text=f'Pair {new_pair} already exists!')
        except pd.ValidationError:
            raise web.HTTPBadRequest(text='Invalid key-value pair')

        PAIR_VALUES.append(new_pair)
        return web.json_response(status=201, data=new_pair.dict())

    async def put(self) -> web.Response:
        print('Jestem w put')
        raise web.HTTPNotImplemented()

    async def delete(self) -> web.Response:
        print('Jestem w delete')
        raise web.HTTPNotImplemented()