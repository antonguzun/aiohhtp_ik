# routes.py
from views import index, result, new_user, get_data, sand

def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_get('/res', result)
    app.router.add_post('/user', new_user)
    app.router.add_post('/ik', get_data)
    app.router.add_get('/sand', sand)

