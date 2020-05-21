from .database import _get_connection, _insert_query, _get_query
import requests

path = 'database/table-def/'
with _get_connection() as conn:
    with conn.cursor() as cursor:
        with open(path + 'users.sql') as u:
            cursor.execute(u.read())
        with open(path + 'surveillance.sql') as s:
            cursor.execute(s.read())
        with open(path + 'countries.sql') as c:
            cursor.execute(c.read())
            if not _get_query('countries'):
                data = requests.get('https://api.covid19api.com/countries').json()
                for i in data:
                    _insert_query('countries', **i)
    conn.commit()
