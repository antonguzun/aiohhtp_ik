# routes.py
from views import index, new_user, state_detail_view


def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_post('/user', new_user)
    app.router.add_post('/ik', state_detail_view)
