# Feature will be unused for now

from Features.Data_Processing.utils import convert_to_dictionary, get_column_names
from datetime import datetime
from Database.fetch import get_latest_data, get_date_range_data


def is_invalid_data(data):
    is_not_none = data is not None
    is_invalid = data == -9999.000000
    return is_not_none and is_invalid


# Removes columns with valid data
def get_invalid_data_column_names(data):
    invalid_data_column_name = []
    if data is not None:
        column_names = get_column_names(data)
        data = convert_to_dictionary(data)

        for column_name in column_names:
            is_value = column_name[0] == 'V'
            is_invalid = is_invalid_data(data[column_name])

            if is_value and is_invalid:
                invalid_data_column_name.append(column_name)

    return invalid_data_column_name


def get_invalid_parameters(cursor, station_name):

    # Change to current date
    customer_data = get_date_range_data(cursor, station_name, "2021-8-01", "2021-08-27 16:00:00.000")

    latest_data = get_latest_data(cursor, station_name)
    invalid_data_column_names = get_invalid_data_column_names(latest_data)

    invalid_parameters = []
    last_invalid_parameter = {}

    for column_name in invalid_data_column_names:

        counter = 0
        max_counter = len(customer_data)

        for row_data in reversed(customer_data):
            row_data = convert_to_dictionary(row_data)
            invalid = is_invalid_data(row_data[column_name])
            current_parameter_data = {'parameter_name': column_name, 'value': row_data[column_name],
                                      'date_occurred': row_data['Date_Time'], 'date_checked': str(datetime.now())}

            if invalid:
                counter = counter + 1
                last_invalid_parameter = current_parameter_data
            if counter == max_counter:
                invalid_parameters.append(current_parameter_data)

            # Valid data detected on current parameter
            if not invalid:
                if last_invalid_parameter != {}:
                    invalid_parameters.append(last_invalid_parameter)
                break

    return invalid_parameters
