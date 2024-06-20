from Database.connect import get_cursor, get_cursor_localhost_mysql
from Database.fetch import get_all_data, get_custom_query
import json
from Features.Mailer.send_email import send_mail
import time
import os
from dotenv import load_dotenv
from Logs.logger import logger
from Constants.dictionaries import create_mailer_dictionary, create_arm_dictionary, create_current_status_dictionary

load_dotenv()

mysql_driver = os.getenv("ODBC_DRIVER_MYSQL")
localhost_server_name = os.getenv("SERVER3_MYSQL_LOCALHOST_NAME")
localhost_username = os.getenv("SERVER3_MYSQL_LOCALHOST_USERNAME")
localhost_password = os.getenv("SERVER3_MYSQL_LOCALHOST_PASSWORD")
localhost_database = os.getenv("local_mysql_database")


def get_sales_customer_index(customers, sales_id):
    customer_indices = []
    for i in range(len(customers)):
        if customers[i].SalesId == sales_id:
            customer_indices.append(i)

    return customer_indices


def get_arm_credential(arms, arm_id):
    for arm in arms:
        if arm.Id == arm_id:
            return arm


def write_to_json(data):
    with open("data/mailer_data.json", "w") as outfile:
        json.dump(data, outfile)


def create_log(response, data):
    execution_logger = logger('execution_logs',
                              './Logs/execution.log',
                              '%(levelname)s. %(message)s %(asctime)s')

    if response == {}:
        message = f'Mail sent to {data['sales_email']}'
        execution_logger.write_log(level=20, message=message)
    else:
        message = f'Mail not sent to {data['sales_email']}'
        execution_logger.write_log(level=40, message=message)


def main():
    data_dictionary = []

    localhost = {
        'Driver': mysql_driver,
        'ServerName': localhost_server_name,
        'DatabaseName': localhost_database,
        'Username': localhost_username,
        'Password': localhost_password
    }

    localhost_cursor = get_cursor_localhost_mysql(localhost)
    sales_list = get_all_data(localhost_cursor, 'Sales')
    arms = get_all_data(localhost_cursor, 'Arm')

    # Process every sales personnel
    for sales in sales_list:

        mailer_data_dict = create_mailer_dictionary(sales)

        customer_arm = get_custom_query(localhost_cursor, f"SELECT DISTINCT(ArmId) FROM Customer "
                                                          f"WHERE SalesId = {sales.Id}")

        customers = get_custom_query(localhost_cursor,
                                     f'SELECT * FROM Customer '
                                     f'WHERE SalesId = {sales.Id}')

        # Process the data ARMs or EMB that a customer belongs to
        for arm in customer_arm:

            arm_credential = get_arm_credential(arms, arm.ArmId)
            arm_dict = create_arm_dictionary(arm_credential)
            cursor = get_cursor(arm_credential, mysql_driver)

            # Process the data for each customer/station
            stations_online_counter = 0
            max_stations_counter = 0
            for customer in customers:

                if customer.ArmId != arm.ArmId:
                    continue

                # put current status dictionary inside the "stations" in dictionary
                current_status_dictionary = create_current_status_dictionary(cursor, customer)
                arm_dict["stations"].append(current_status_dictionary)

                # Counters for tracking online stations
                if current_status_dictionary['current_status'] == 'Online':
                    stations_online_counter = stations_online_counter + 1
                max_stations_counter = max_stations_counter + 1

            arm_dict["online"] = f"{stations_online_counter}/{max_stations_counter}"
            mailer_data_dict["report"].append(arm_dict)

            cursor.close()

        data_dictionary.append(mailer_data_dict)
        sendmail_response = send_mail(mailer_data_dict, sales.Email)
        create_log(sendmail_response, mailer_data_dict)

        time.sleep(1)

    write_to_json(data_dictionary)
    localhost_cursor.close()

    return


if __name__ == "__main__":
    main()
