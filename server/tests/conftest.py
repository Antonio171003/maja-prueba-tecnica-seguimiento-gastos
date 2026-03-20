import pytest

from app import create_app
from app.extensions import db


@pytest.fixture
def app(monkeypatch):
    # Fuerza una DB temporal para tests sin tocar tu Config real
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")

    app = create_app()
    app.config.update(
        TESTING=True,
    )

    with app.app_context():
        # Importa modelos para que SQLAlchemy los registre antes de create_all()
        from app.models import Category, Expense  # noqa: F401

        db.create_all()
        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

