import os
import psycopg2 as pg

DATABASE_URL = os.getenv('DATABASE_URL')
DB_NAME = 'communist_bot'
USER = os.getenv('DB_USERNAME')
PSW = os.getenv('DB_PASSWORD')


def add_user(user_id: int, username: str):
    if not _get_query('users', id=user_id):
        _insert_query('users', id=user_id, username=username)


def start_watching(watcher_id: int, target_id: int):
    _insert_query('surveillance', watcher_id=watcher_id, target_id=target_id)


def _insert_query(table_name, **kwargs):
    if not kwargs:
        raise AttributeError
    with _get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                f'''INSERT INTO {table_name}({_get_string(kwargs.keys())}) VALUES ({_get_s(len(kwargs))});''',
                tuple(kwargs.values()))
            conn.commit()


def _get_all(table_name, *columns):
    return _get_query(table_name, *columns)


def _get_query(table_name, *columns, **query):
    with _get_connection() as conn:
        with conn.cursor() as cursor:
            cols = _get_string(columns) if columns else '*'
            cursor.execute(f'SELECT {cols} FROM {table_name} WHERE {_get_filter(query)}',
                           tuple(query.values()) if query else None)
            data = cursor.fetchall()
    return data


def _get_connection():
    return pg.connect(database=DB_NAME, user=USER, password=PSW)


def _get_string(arr):
    res = ''
    for k in arr.__iter__():
        res += f'{k}, '
    return res[:-2]


def _get_s(amount: int):
    res = ''
    for i in range(amount):
        res += '%s, '
    return res[:-2]


def _get_filter(query: dict):
    if not query:
        return 'true'
    res = ''
    for i in query:
        res += f'{i}=%s and '
    return res[:-5]


if __name__ == '__main__':
    print(_get_all('users'))
    add_user(2, 'vasya')
    print(_get_all('users'))
