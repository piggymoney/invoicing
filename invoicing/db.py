
from __future__ import absolute_import

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()


def init(path):
    """Initialise the DB.

    Takes one argument:
    - path: The file path for the SQLite DB.

    """

    engine = create_engine("sqlite:///{0}".format(path))
    Session.configure(bind=engine)


@contextmanager
def connection():
    """A context manager for managing the scope of a database transaction.

    Usage:

    >>> with db.connection() as DB:
    >>>     DB.add(<model object>)
    >>>     result = DB.query(...)
    ...
    >>> for r in result:
    >>>    <do things>

    """

    s = Session()

    try:
        yield s
        s.commit()
    except BaseException:
        s.rollback()
        raise
