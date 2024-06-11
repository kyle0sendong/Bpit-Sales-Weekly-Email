def get_column_names(data):
    column_name = []
    for name in data.cursor_description:
        column_name.append(name[0])
    return column_name


def convert_to_dictionary(data):
    column_names = get_column_names(data)
    return dict(zip(column_names, data))
