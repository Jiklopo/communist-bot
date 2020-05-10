from .database import _get_connection

with _get_connection() as conn:
    with conn.cursor() as cursor:
        with open('database/users.sql') as u:
            cursor.execute(u.read())
        with open('database/surveillance.sql') as s:
            cursor.execute(s.read())
    conn.commit()
