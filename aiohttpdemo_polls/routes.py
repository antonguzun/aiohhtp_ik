# routes.py
from views import index, state_detail_view, create_perimeter, delete_perimeter, update_perimeter, read_all_perimeters


def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_get('/ik', state_detail_view)
    app.router.add_post('/create', create_perimeter)
    app.router.add_get('/read_all', read_all_perimeters)
    app.router.add_post('/delete', delete_perimeter)
    app.router.add_post('/update', update_perimeter)
