"""
Main module with server routing and server-run method
"""
from aiohttp import web
from api import pair
from db import setup

# Initialize web application
app = web.Application()
app.router.add_view('/pair/', pair.Pair)
app.router.add_get('/pair/{key_name:[0-9A-Za-z]+}', pair.PairGet)

setup.init_db()
web.run_app(app)
