import logging
import typing
from aiohttp import web
from model import BirdSample

LOG = logging.getLogger(__name__)


BIRD_SAMPLES: typing.List[BirdSample] = []


class BirdSamples(web.View):
    async def get(self) -> web.Response:
        LOG.debug('Getting a existing sample')
        raise web.HTTPNotImplemented()

    async def put(self) -> web.Response:
        LOG.debug('Uploading a new sample')
        raise web.HTTPNotImplemented()

    async def delete(self) -> web.Response:
        LOG.debug('Deleting a existing sample')
        raise web.HTTPNotImplemented()


async def list_all(request: web.Request) -> web.Response:
    LOG.debug('Getting a list of samples')
    raise web.HTTPNotImplemented()


app = web.Application()
app.router.add_view('/api/samples/{sample_name}', BirdSamples)
app.add_routes([web.get('/api/samples', list_all)])


web.run_app(app)
