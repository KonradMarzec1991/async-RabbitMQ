"""
Main module with server routing and server-run method
"""
from aiohttp import web
import db
from setup.urls import add_urls


# Initialize web application
app = web.Application()

# Add routes for GET/POST requests
add_urls(app)

# Create/connect database
db.init_db()

# Run application
web.run_app(app)
