import sqlite3

conn = sqlite3.connect('chat_db.db')
cursor = conn.cursor()


def add_data_to_db(data_to_db) -> None:
    """
    Add data to data base
    :param data_to_db:
    :return: None
    """
    data = data_to_db
    cursor.execute(f"INSERT INTO `chat_info`"
                   f"(`data`)"
                   f"VALUES (?, ?)",
                   (data))
    conn.commit()


def _init_db() -> None:
    """
    Init data base
    :return: None
    """

    with open("sql_request.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def is_db_exists() -> None:
    """
    Check is data base exists, if not exists - create data base
    :return: None

    """
    try:
        sqlite3.connect('chat_db.db', uri=True)
    except sqlite3.OperationalError:
        _init_db()


is_db_exists()
