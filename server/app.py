"""
Main module with server routing and server run method
"""

from aiohttp import web
from api import pair

app = web.Application()
app.router.add_view('/pair', pair.Pair)

web.run_app(app)
