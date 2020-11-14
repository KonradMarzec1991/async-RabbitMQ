"""
Main module with server routing and server-run method
"""
import os
import logging

from aiohttp import web
import db
from setup.urls import add_urls


# Initialize logger
if not os.path.isdir('logs'):
    os.mkdir('logs')

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/log.log"),
        logging.StreamHandler()
    ]
)

# Initialize web application
app = web.Application()
logging.debug('App initialized')

# Add routes for GET/POST requests
add_urls(app)
logging.debug('Urls added to app')

# Create/connect database
db.init_db()
logging.debug('Database initialized successfully')

# Run application
web.run_app(app)
