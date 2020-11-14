"""
Main module with server routing and server-run method
"""
from aiohttp import web
import setup
from api import (
    Pair,
    PairGet
)

# Initialize web application
app = web.Application()

# Add routes for GET/POST requests
app.router.add_view('/pair/', Pair)
app.router.add_get('/pair/{key_name:[0-9A-Za-z]+}', PairGet)

# Create/connect database
setup.init_db()

# Run application
web.run_app(app)
