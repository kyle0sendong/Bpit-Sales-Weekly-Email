from Database.connect import get_cursor, get_cursor_localhost_mysql
from Database.fetch import get_all_data, get_custom_query
from Features.Data_Processing.get_station_status import get_current_status, get_days_online
from Utils.dates import get_last_week_date, get_date_today, convert_datetime_string, convert_date_string
from datetime import datetime
import json
from Features.Mailer.send_email import send_mail
import time
import os
from dotenv import load_dotenv
from Logs.logger import logger

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

    for sales in sales_list:

        mailer_data_dict = {
            "sales_firstname": f"{sales.FirstName}",
            "sales_lastname": f"{sales.LastName}",
            "sales_email": f"{sales.Email}",
            "start_date": f"{convert_date_string(get_last_week_date())}",
            "end_date": f"{convert_date_string(get_date_today())}",
            "report": []
        }

        sales_customers = get_custom_query(localhost_cursor,
                                           f'SELECT * FROM Customer '
                                           f'WHERE SalesId = {sales.Id}')
        sales_arm = get_custom_query(localhost_cursor, f"SELECT DISTINCT(ArmId) FROM Customer "
                                                       f"WHERE SalesId = {sales.Id}")

        for arm in sales_arm:

            arm_credential = get_arm_credential(arms, arm.ArmId)
            arm_dict = {
                "arm_name": arm_credential.DatabaseName,
                "region_name": arm_credential.RegionName,
                "online": "",
                "stations": []
            }

            cursor = get_cursor(arm_credential, mysql_driver)
            stations_online_counter = 0
            max_stations_counter = 0
            for customer in sales_customers:

                if customer.ArmId == arm.ArmId:

                    days_online = get_days_online(cursor, customer.TableName)

                    current_status_dictionary = get_current_status(cursor, customer.TableName)
                    current_status_dictionary["days_online"] = f"{days_online}/7 days"
                    current_status_dictionary["customer_name"] = f"{customer.CustomerName}"
                    current_status_dictionary["date_checked"] = convert_datetime_string(datetime.now())

                    # put current status dictionary inside the "stations" in dictionary
                    arm_dict["stations"].append(current_status_dictionary)

                    if current_status_dictionary['current_status'] == 'Online':
                        stations_online_counter = stations_online_counter + 1

                    max_stations_counter = max_stations_counter + 1

            cursor.close()

            arm_dict["online"] = f"{stations_online_counter}/{max_stations_counter}"

            mailer_data_dict["report"].append(arm_dict)

        sendmail_response = send_mail(mailer_data_dict, sales.Email)
        create_log(sendmail_response, mailer_data_dict)
        data_dictionary.append(mailer_data_dict)

        time.sleep(1)

    write_to_json(data_dictionary)
    localhost_cursor.close()

    return


if __name__ == "__main__":
    main()

