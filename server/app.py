"""
Main module with server routing and server run method
"""

from aiohttp import web

import db
from api import pair

app = web.Application()
app.router.add_view('/pair', pair.Pair)

db.setup(app)
web.run_app(app)
