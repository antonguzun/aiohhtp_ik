# routes.py
from views import index, new_user, req_state_of_dev

def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_post('/user', new_user)
    app.router.add_post('/ik', req_state_of_dev)

