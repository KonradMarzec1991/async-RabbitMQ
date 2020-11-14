from api import (
    PairGet,
    PairPost
)


def add_urls(app):
    app.router.add_get('/pair/{key_name:[0-9A-Za-z]+}', PairGet)
    app.router.add_view('/pair/', PairPost)
    return app
