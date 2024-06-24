from datetime import datetime

from Features.Data_Processing.get_station_status import get_days_online, get_current_status
from Utils.dates import convert_date_string, get_date_today, get_last_week_date, convert_datetime_string


def create_mailer_dictionary(sales):
    mailer_data_dict = {
        "sales_firstname": f"{sales.FirstName}",
        "sales_lastname": f"{sales.LastName}",
        "sales_email": f"{sales.Email}",
        "start_date": f"{convert_date_string(get_last_week_date())}",
        "end_date": f"{convert_date_string(get_date_today())}",
        "report": []
    }
    return mailer_data_dict


def create_current_status_dictionary(database_model, customer):
    days_online = get_days_online(database_model, customer.TableName)
    current_status_dictionary = get_current_status(database_model, customer.TableName)
    current_status_dictionary["days_online"] = f"{days_online}/7 days"
    current_status_dictionary["customer_name"] = f"{customer.CustomerName}"
    current_status_dictionary["date_checked"] = convert_datetime_string(datetime.now())
    return current_status_dictionary


def create_arm_dictionary(arm_credential):
    arm_dict = {
        "arm_name": arm_credential.DatabaseName,
        "region_name": arm_credential.RegionName,
        "online": "",
        "stations": []
    }
    return arm_dict


