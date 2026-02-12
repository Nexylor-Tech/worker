from psycopg_pool import ConnectionPool
from config import Config
from contextlib import contextmanager

if Config.DATABASE_URL is None:
    raise ValueError("Database url not provided")

_pool = None


def get_pool():
    global _pool
    if _pool is None:
        _pool = ConnectionPool(
            conninfo=Config.DATABASE_URL,
            min_size=1,
            max_size=10,
            kwargs={"autocommit": True},
        )
    return _pool


@contextmanager
def get_db_cursor():
    with get_pool().connection() as conn:
        with conn.cursor() as cur:
            yield conn, cur


def close_pool():
    global _pool
    if _pool is not None:
        _pool.close()
        _pool = None
