"""MySQL database connection helper."""
import mysql.connector
import os

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'MyNewP@ssword20250317'),
    'database': os.environ.get('DB_NAME', 'java_learning_platform'),
    'charset': 'utf8mb4',
    'autocommit': True,
}


def get_connection():
    """Get a new database connection."""
    return mysql.connector.connect(**DB_CONFIG)


def query(sql, params=None, fetch=True):
    """Execute a query and return results. Use fetch=False for INSERT/UPDATE/DELETE."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, params or ())
        if fetch:
            result = cursor.fetchall()
            return result
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()
