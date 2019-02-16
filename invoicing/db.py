
from __future__ import absolute_import

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///db.sqlite")

Session = sessionmaker()
Session.configure(bind=engine)


@contextmanager
def connection():
    s = Session()

    try:
        yield s
        s.commit()
    except BaseException:
        s.rollback()
        raise
