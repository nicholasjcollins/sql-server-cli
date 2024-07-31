def create_info_query(db_dict):
    query_string = ""
    for i, key in enumerate(db_dict):
        pre = "" if i == 0 else "\nUNION ALL"
        query_string += pre + create_table_info_query(key, db_dict[key])
    return query_string


def create_db_query(db_names):
    query_string = ""
    for i, key in enumerate(db_names):
        pre = "" if i == 0 else "\nUNION ALL"
        query_string += pre + create_db_info_query(key)
    return query_string


def create_db_info_query(db_name):
    return f"""
SELECT
    '{db_name}' AS DB,
    TABLE_SCHEMA AS 'Schema',
    TABLE_NAME AS 'Table',
    COLUMN_NAME AS Object,
    DATA_TYPE AS DataType,
    CHARACTER_MAXIMUM_LENGTH AS Length,
    NUMERIC_PRECISION AS Precision,
    NUMERIC_SCALE AS Scale,
    NULL AS Definition
FROM {db_name}.INFORMATION_SCHEMA.COLUMNS
UNION ALL
SELECT
    '{db_name}' as DB,
    TABLE_SCHEMA AS 'Schema',
    'View' AS 'Table',
    TABLE_NAME AS Object,
    NULL AS DataType,
    NULL AS Length,
    NULL AS Precision,
    NULL AS Scale,
    m.Definition AS Definition
FROM {db_name}.INFORMATION_SCHEMA.VIEWS v
JOIN {db_name}.sys.sql_modules m
ON OBJECT_ID(v.TABLE_SCHEMA + '.' + v.TABLE_NAME) = m.object_id
UNION ALL
SELECT
    '{db_name}' AS DB,
    SCHEMA_NAME(o.schema_id) AS 'Schema',
    CASE WHEN o.type in ('FN', 'IF', 'TF') THEN 'Function'
    WHEN o.type = 'P' THEN 'StoredProcedure' ELSE NULL END AS 'Table',
    o.name AS Object,
    NULL AS DataType,
    NULL AS Length,
    NULL AS Precision,
    NULL AS Scale,
    m.Definition AS Definition
FROM {db_name}.sys.objects o
JOIN {db_name}.sys.sql_modules m ON o.object_id = m.object_id
    """


def create_table_info_query(db_name, schema_table_list):
    query_string = f"""
SELECT
    '{db_name}' as DB,
    TABLE_SCHEMA as 'Schema',
    TABLE_NAME as 'Table',
    COLUMN_NAME as 'Object',
    DATA_TYPE as 'DataType',
    CHARACTER_MAXIMUM_LENGTH as 'Length',
    NUMERIC_PRECISION as 'Precision',
    NUMERIC_SCALE as 'Scale'
FROM {db_name}.INFORMATION_SCHEMA.COLUMNS
"""
    for i, table_dict in enumerate(schema_table_list):
        pre = "WHERE " if i == 0 else "\nOR "
        query_string += pre + \
            f"(TABLE_NAME = '{table_dict["Table"]}' AND TABLE_SCHEMA = '{
                table_dict["Schema"]}')"
    return query_string


def parse_dbs(dbs):
    db_list = dbs.split(',')
    return list(map(lambda x: x.strip(), db_list))


def parse_tables(tables):
    # returns DatabaseName:[{Schema: SchemaName, Table: TableName}] for all provided databases (comma separated)
    table_list = tables.split(',')
    table_data = map(parse_table_string, table_list)
    db_dict = {}
    for table in table_data:
        if table[0] in db_dict:
            db_dict[table[0]].append(table[1])
        else:
            db_dict[table[0]] = [table[1]]
    return db_dict


def parse_table_string(table):
    # returns (DatabaseName: {Schema: SchemaName, Table: TableName} for provided table string in format DB.Schema.Table
    table_data = table.strip().split('.')
    if len(table_data) != 3:
        raise ValueError(f"Unexpected Table Format: {
                         table} should be provided as comma separated list as: DB.Schema.Table")
        return
    return (table_data[0], {"Schema": table_data[1], "Table": table_data[2]})


def main():
    test_str = "DW1.dbo.Employee_Info, DW1.dbo.Cost_Centers, CHDAPPS.dbo.CHDForms_FormQuestions"
    db_dict = parse_tables(test_str)
    print(create_info_query(db_dict))
    test_db = ["CHD_Polar_Bear", "CHDAPPS"]
    print(create_db_query(test_db))


if __name__ == '__main__':
    main()
