
from __future__ import absolute_import

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()


def init(path):
    engine = create_engine("sqlite:///{0}".format(path))
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
