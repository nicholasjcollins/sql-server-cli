import pyodbc


def query_to_dicts(query, connection_str):
    with pyodbc.connect(connection_str) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]
