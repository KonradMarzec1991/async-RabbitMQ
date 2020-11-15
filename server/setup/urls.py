"""
Module delivers functions for loading urls
"""
from api.api import (
    PairGet,
    PairPost
)


def add_urls(app):
    """
    Loads to app url list
    :param app: app instance
    :return: modified app instance
    """
    app.router.add_get('/pair/{key_name:[0-9A-Za-z]+}', PairGet)
    app.router.add_view('/pair/', PairPost)
    return app
