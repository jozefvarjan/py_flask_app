import os

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def database_uri(db_url=None):
    """Resolve the configured database URI.

    Resolution order: explicit ``db_url`` argument, the ``DATABASE``
    environment variable, then a local sqlite database as a fallback. This
    keeps the app database-agnostic so any SQLAlchemy-supported backend
    (PostgreSQL, MySQL, ...) can be used by passing its URL.

    For sqlite URIs the path is made absolute (relative to the project root):
    flask_sqlalchemy resolves relative sqlite paths against the app's instance
    folder, not the current working directory, so a relative URI like
    ``sqlite:///./data/data.db`` would point at ``instance/data/data.db``.
    Non-sqlite URIs are returned unchanged.
    """
    uri = db_url or os.getenv("DATABASE")
    prefix = "sqlite:///"
    if uri.startswith(prefix):
        path = uri[len(prefix):]
        if not os.path.isabs(path):
            path = os.path.join(BASE_DIR, path)
        uri = prefix + os.path.abspath(path)
    return uri
