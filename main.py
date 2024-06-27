import os
import time

from dotenv import load_dotenv

from Database.DatabaseConnection import DatabaseConnection
from Database.DatabaseModel import DatabaseModel
from Error_Handler.Logger import Logger
from Features.Data_Processing.StationStatusReporter import StationStatusReporter
from Features.Data_Processing.dictionaries import create_mailer_dictionary, create_arm_dictionary, \
    create_current_status_dictionary
from Features.Mailer.send_email import send_mail

load_dotenv()

mysql_driver = os.getenv("ODBC_DRIVER_MYSQL")
localhost_server_name = os.getenv("SERVER3_MYSQL_LOCALHOST_NAME")
localhost_username = os.getenv("SERVER3_MYSQL_LOCALHOST_USERNAME")
localhost_password = os.getenv("SERVER3_MYSQL_LOCALHOST_PASSWORD")
localhost_database = os.getenv("local_mysql_database")


def create_log(logger: Logger, response: dict, data: dict):
    if response == {}:
        message = f'Mail sent to {data['sales_email']}'
        logger.write_log(level=20, message=message)
    else:
        message = f'Mail not sent to {data['sales_email']}'
        logger.write_log(level=20, message=message)


def main():
    data_dictionary = []

    localhost_connection = DatabaseConnection(driver=mysql_driver,
                                              server=localhost_server_name,
                                              database=localhost_database,
                                              username=localhost_username,
                                              password=localhost_password)
    localhost_model = DatabaseModel(localhost_connection.get_cursor())

    sales_list = localhost_model.get_all_data('Sales')
    arm_list = localhost_model.get_all_data('Arm')
    execution_logger = Logger('execution_logs',
                              './Logs/execution.log',
                              '%(asctime)s. %(levelname)s. %(message)s')

    # Process every sales personnel
    for sales in sales_list:

        mailer_data_dict = create_mailer_dictionary(sales)

        customer_id_list = localhost_model.get_data_custom_query(f'SELECT CustomerId FROM Lookup_Sales_Customer '
                                                                 f'WHERE SalesId = {sales.Id}')

        # check which region a customer belongs to
        for arm in arm_list:
            arm_driver = localhost_model.get_data('Driver', arm.DriverId)
            arm_connection = DatabaseConnection(
                driver=arm_driver.DriverName,
                server=arm.ServerName,
                database=arm.DatabaseName,
                username=arm.Username,
                password=arm.Password
            )
            arm_dict = create_arm_dictionary(arm)
            arm_cursor = arm_connection.get_cursor()

            # Process the data for each customer/station
            stations_online_counter = 0
            max_stations_counter = 0
            for customer_id in customer_id_list:

                customer = localhost_model.get_data_custom_query(f'SELECT * FROM Customer '
                                                                 f'WHERE Id = {customer_id.CustomerId}')
                customer = customer[0]

                if customer.ArmId != arm.Id:
                    continue

                station_status_reporter = StationStatusReporter(DatabaseModel(arm_cursor),
                                                                customer.TableName,
                                                                customer.CustomerName)

                # put current status dictionary inside the ARM "stations" dictionary
                current_status_dictionary = create_current_status_dictionary(station_status_reporter)
                arm_dict["stations"].append(current_status_dictionary)

                # Counters for tracking online stations
                max_stations_counter += 1
                if current_status_dictionary['current_status'] == 'Online':
                    stations_online_counter += 1

            arm_dict["online"] = f"{stations_online_counter}/{max_stations_counter}"
            mailer_data_dict["report"].append(arm_dict)

            arm_connection.close_cursor()
            arm_connection.close_connection()

        data_dictionary.append(mailer_data_dict)
        sendmail_response = send_mail(mailer_data_dict, sales.Email)
        create_log(execution_logger, sendmail_response, mailer_data_dict)

        time.sleep(1)

    localhost_connection.close_cursor()
    localhost_connection.close_connection()


if __name__ == "__main__":
    main()
