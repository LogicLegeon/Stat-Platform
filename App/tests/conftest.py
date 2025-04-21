# App/tests/conftest.py
import pytest
from App.main import create_app            # import your app‑factory
from App.database import db, create_db

@pytest.fixture(scope="session")
def app():
    """A Flask application object configured for tests."""
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    # Everything after this 'with' runs inside the app‑context
    with app.app_context():
        create_db()                        # create tables once
        yield app                          # give the app to tests
        db.session.remove()                # clean up
        db.drop_all()

@pytest.fixture(scope="session")
def client(app):
    """Flask test client; handy for route tests."""
    return app.test_client()
