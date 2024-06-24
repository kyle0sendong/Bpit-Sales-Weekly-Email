from Database.DatabaseConnection import DatabaseConnection
from Database.DatabaseModel import DatabaseModel
from Features.Mailer.send_email import send_mail
import time
from Error_Handler.Logger import Logger
from Features.Data_Processing.dictionaries import create_mailer_dictionary, create_arm_dictionary, \
    create_current_status_dictionary
from dotenv import load_dotenv
import os
from Features.Data_Processing.StationStatusReporter import StationStatusReporter


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


def create_log(response, data):
    execution_logger = Logger('execution_logs',
                              './Logs/execution.log',
                              '%(asctime)s. %(levelname)s. %(message)s ')

    if response == {}:
        message = f'Mail sent to {data['sales_email']}'
        execution_logger.write_log(level=20, message=message)
    else:
        message = f'Mail not sent to {data['sales_email']}'
        execution_logger.write_log(level=20, message=message)


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

    # Process every sales personnel
    for sales in sales_list:

        mailer_data_dict = create_mailer_dictionary(sales)

        customer_arm = localhost_model.get_data_custom_query(f"SELECT DISTINCT(ArmId) FROM Customer "
                                                             f"WHERE SalesId = {sales.Id}")
        customers = localhost_model.get_data_custom_query(f'SELECT * FROM Customer '
                                                          f'WHERE SalesId = {sales.Id}')

        # Process the data ARMs or EMB that a customer belongs to
        for arm in customer_arm:

            arm_credential = get_arm_credential(arm_list, arm.ArmId)
            arm_dict = create_arm_dictionary(arm_credential)
            arm_driver = localhost_model.get_data('Driver', arm.ArmId)
            arm_connection = DatabaseConnection(
                driver=arm_driver.DriverName,
                server=arm_credential.ServerName,
                database=arm_credential.DatabaseName,
                username=arm_credential.Username,
                password=arm_credential.Password
            )
            arm_cursor = arm_connection.get_cursor()
            arm_database_model = DatabaseModel(arm_cursor)

            # Process the data for each customer/station
            stations_online_counter = 0
            max_stations_counter = 0
            for customer in customers:
                if customer.ArmId != arm.ArmId:
                    continue

                station_status_reporter = StationStatusReporter(arm_database_model,
                                                                customer.TableName,
                                                                customer.CustomerName)

                # put current status dictionary inside the ARM "stations" dictionary
                current_status_dictionary = create_current_status_dictionary(station_status_reporter)
                arm_dict["stations"].append(current_status_dictionary)

                # Counters for tracking online stations
                if current_status_dictionary['current_status'] == 'Online':
                    stations_online_counter = stations_online_counter + 1
                max_stations_counter = max_stations_counter + 1

            arm_dict["online"] = f"{stations_online_counter}/{max_stations_counter}"
            mailer_data_dict["report"].append(arm_dict)

            arm_connection.close_cursor()

        data_dictionary.append(mailer_data_dict)
        sendmail_response = send_mail(mailer_data_dict, sales.Email)
        create_log(sendmail_response, mailer_data_dict)

        time.sleep(1)

    localhost_connection.close_cursor()

    return


if __name__ == "__main__":
    main()
