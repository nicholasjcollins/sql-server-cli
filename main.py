from sql_handler import query_to_dicts
from data_dict import Data
from command_builder import interpret
from query_builder import create_db_query, create_info_query


def main():
    last_command = ""
    while last_command != "quit":
        command = input("Enter Command:")
        command_dict = interpret(command)
        if command_dict == None or 'cmd' not in command_dict:
            print("Error, command not recognized")
            continue
        last_command = command_dict['cmd']
        match last_command:
            case 'quit':
                continue
            case 'table_info':
                print(create_info_query(command_dict['data']))
            case 'search_dbs':
                print(create_db_query(command_dict['data']))


if __name__ == '__main__':
    main()
