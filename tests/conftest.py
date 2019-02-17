
import os
import tempfile

import pytest

from invoicing import create_app, init_db
from invoicing.db import Session
from invoicing.models import Base


@pytest.fixture
def client():
    app = create_app()

    app.config['TESTING'] = True
    client = app.test_client()

    db_fd, app.config["DATABASE_PATH"] = tempfile.mkstemp()
    init_db(app)
    Base.metadata.create_all(Session().get_bind())

    yield client

    os.close(db_fd)
    os.unlink(app.config["DATABASE_PATH"])
