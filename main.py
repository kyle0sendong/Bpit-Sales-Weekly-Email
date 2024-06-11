from Database.connect import get_cursor, get_cursor_localhost_mssql
from Database.fetch import get_all_data, get_custom_query
from Features.Data_Processing.get_station_status import get_current_status, get_days_online
from Utils.dates import get_last_week_date, get_date_today, convert_datetime_string, convert_date_string
from datetime import datetime
import json
from Features.Mailer.send_email import send_mail
import time
import os
from dotenv import load_dotenv


load_dotenv()

local_server_name = os.getenv("LOCAL_MSSQL")
local_database_name = os.getenv("LOCAL_MSSQL_DATABASE")


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


def main():

    data_dictionary = []

    localhost = {
        'ServerName': local_server_name,
        'DatabaseName': local_database_name
    }

    localhost_cursor = get_cursor_localhost_mssql(localhost)
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
            cursor = get_cursor(arm_credential)

            arm_dict = {
                "arm_name": arm_credential.DatabaseName,
                "online": "",
                "stations": []
            }

            stations_online_counter = 0
            counter = 0
            for customer in sales_customers:

                if customer.ArmId == arm.ArmId:

                    current_status_dictionary = get_current_status(cursor, customer.TableName)
                    current_status_dictionary["date_checked"] = convert_datetime_string(datetime.now())

                    days_online = get_days_online(cursor, customer.TableName)
                    current_status_dictionary["days_online"] = f"{days_online}/7 days"

                    arm_dict["stations"].append(current_status_dictionary)

                    if current_status_dictionary['current_status'] == 'Online':
                        stations_online_counter = stations_online_counter + 1

                    counter = counter + 1

            cursor.close()

            arm_dict["online"] = f"{stations_online_counter}/{counter}"
            mailer_data_dict["report"].append(arm_dict)

        response = send_mail(mailer_data_dict, sales.Email)
        data_dictionary.append(mailer_data_dict)
        time.sleep(1)

    localhost_cursor.close()

    with open("data/mailer_data.json", "w") as outfile:
        json.dump(data_dictionary, outfile)


try:
    if __name__ == "__main__":
        main()
        print("Finished sending mail")

except Exception as e:
    print(f"Error: {e}")
