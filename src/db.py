

"""Oracle database connection helpers for the SRPMS CLI prototype."""

import oracledb

from config import DB_DSN, DB_PASSWORD, DB_USER


def get_connection():
    """Create and return a new Oracle database connection."""
    return oracledb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        dsn=DB_DSN,
    )


def test_connection():
    """Test whether the CLI can connect to Oracle."""
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 'Connected to Oracle' FROM dual")
                row = cursor.fetchone()
                print(row[0])
                return True
    except oracledb.DatabaseError as error:
        print("Database connection failed.")
        print(error)
        return False