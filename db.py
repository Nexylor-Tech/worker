from psycopg_pool import ConnectionPool
from config import Config
from contextlib import contextmanager

if Config.DATABASE_URL is None:
    raise ValueError("Database url not provided")
pool = ConnectionPool(
    conninfo=Config.DATABASE_URL, min_size=1, max_size=10, kwargs={"autocommit": True}
)


@contextmanager
def get_db_cursor():
    with pool.connection() as conn:
        with conn.cursor() as cur:
            yield conn, cur


def close_pool():
    pool.close()
