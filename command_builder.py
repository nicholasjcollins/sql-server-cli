from query_builder import parse_dbs, parse_tables


def interpret(command_string):
    if len(command_string) == 0:
        raise ValueError('No data provided')
    command = command_string[0]
    match command.lower():
        case 'q':
            return {"cmd": "quit"}
        case 't':
            table_list = command_string[1:]
            return {
                "cmd": "table_info",
                "data": parse_tables(table_list)
            }
        case 's':
            split_command = command_string.split('"')
            if len(split_command) != 3:
                raise ValueError(
                    'Malformed Search Command. Should be s "pattern" db1, db2')
            else:
                return {
                    "cmd": "search_dbs",
                    "search_string": split_command[1],
                    "data": parse_dbs(split_command[2])
                }
        case _:
            raise ValueError(f"Unrecognized Command: {command_string[0]}")


def main():
    test_str = "t DB1.dbo.Table, DB1.dbo.Table2, DB2.dbo.OtherTable"
    test_str2 = 's "str" DB1, DB2'
    print(interpret(test_str))
    print(interpret(test_str2))


if __name__ == '__main__':
    main()
