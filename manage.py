import os
import unittest

from flask_migrate import Migrate

from app.main import create_app, db
from app.main.model import user, expense, blacklist
from app import blueprint

app = create_app(os.getenv('EXPENSE_TRACKER_ENV') or 'dev')

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = '*'
    header['Access-Control-Allow-Methods'] = '*'
    return response

app.url_map.strict_slashes = False

app.register_blueprint(blueprint)

migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

app.app_context().push()

def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    env = os.getenv('EXPENSE_TRACKER_ENV', 'dev')
    if env == 'prod':     
        from waitress import serve
        serve(app, host="0.0.0.0", port=8080)
    else:
        app.run()