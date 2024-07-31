import re


class Data:
    def __init__(self, query_result):
        self.dataset = {}
        for row in query_result:
            if row['DB'] not in self.dataset:
                self.dataset[row['DB']] = {}
            db_dict = self.dataset[row['DB']]
            if row['Schema'] not in db_dict:
                db_dict[row['Schema']] = {}
            sc_dict = db_dict[row['Schema']]
            if row['Table'] not in sc_dict:
                sc_dict[row['Table']] = {}
            tb_dict = sc_dict[row['Table']]
            tb_dict[row['Object']] = self.build_definition(row)

    def build_definition(self, query_row):
        if query_row['Definition'] != None:
            return query_row['Definition']
        dt = query_row['DataType'].upper()
        ln = query_row['Length']
        sc = query_row['Scale']
        pr = query_row['Precision']
        match dt:
            case 'VARBINARY' | 'BINARY' | 'NCHAR' | 'NVARCHAR' | 'VARCHAR' | 'CHAR':
                return dt + f"({ln})"
            case 'NUMERIC' | 'DECIMAL':
                return dt + f"({pr},{sc})"
            case _:
                return dt

    def search(self, root_dict, search_string):
        print(self.search_dict_keys_r(root_dict, search_string))

    def search_dict_keys_r(self, parent_dict, search_string, pre=''):
        matched = []
        new_list = self.search_dict_keys(parent_dict, search_string, pre)
        if len(new_list) > 0:
            matched.append(new_list)
        for key in parent_dict:
            if isinstance(parent_dict[key], dict):
                r = self.search_dict_keys_r(
                    parent_dict[key], search_string, self.get_prefix(pre, key))
                if len(r) > 0:
                    matched.extend(r)
            else:
                value_list = self.search_long_text(
                    parent_dict[key], search_string)
                if len(value_list) > 0:
                    matched.append({self.get_prefix(pre, key): value_list})
        return matched

    def get_prefix(self, current_prefix, key):
        exclude = ["View", "Function", "StoredProcedure"]
        if key in exclude:
            return current_prefix
        return f"{current_prefix}{key}."

    def search_dict_keys(self, search_dict, search_string, pre=''):
        found = filter(lambda x: search_string.lower()
                       in x.lower(), search_dict)
        return list(map(lambda x: pre + x, found))

    def search_long_text(self, search_in, search_for):
        pattern = re.compile(re.escape(search_for), re.IGNORECASE)
        matches = pattern.finditer(search_in)
        start_indicies = [match.start() for match in matches]
        return list(map(lambda x: search_in[max(0, x - 50):min(len(search_in), x + 50)], start_indicies))


def main():
    test_result = [
        {
            'DB': 'TestDB',
            'Schema': 'dbo',
            'Table': 'StoredProcedure',
            'Object': 'sp_test',
            'DataType': None,
            'Length': None,
            'Precision': None,
            'Scale': None,
            'Definition': 'select * from test'
        },
        {
            'DB': 'TestDB',
            'Schema': 'dbo',
            'Table': 'TestTableDBO',
            'Object': 'Name',
            'DataType': 'varchar',
            'Length': 50,
            'Precision': None,
            'Scale': None,
            'Definition': None
        }
    ]
    long_text = "test this is a pretty long string that we're using to TEST this parser. It needs to include test cases at the beginning and at the end. Maybe we go awhile without using the word. You know the word. I think it's a testament to our fortitude we've lasted this long test"
    data = Data(test_result)
    data.search(data.dataset, 'test')
    # print(data.search_long_text(long_text, "test"))


if __name__ == '__main__':
    main()
