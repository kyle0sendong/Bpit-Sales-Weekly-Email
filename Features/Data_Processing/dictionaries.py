from datetime import datetime, timedelta

from Utils.dates import convert_date_string, get_date_today, get_last_week_date, convert_datetime_string
from Utils.dates import get_7_day_list


def create_mailer_dictionary(sales) -> dict:
    mailer_data_dict = {
        "sales_firstname": f"{sales.FirstName}",
        "sales_lastname": f"{sales.LastName}",
        "sales_email": f"{sales.Email}",
        "start_date": f"{convert_date_string(get_last_week_date())}",
        "end_date": f"{convert_date_string(get_date_today() - timedelta(days=1))}",
        "weekly_days": get_7_day_list(),
        "report": []
    }
    return mailer_data_dict


def create_arm_dictionary(arm_credential) -> dict:
    arm_dict = {
        "arm_name": arm_credential.DatabaseName,
        "region_name": arm_credential.RegionName,
        "online": "",
        "stations": []
    }
    return arm_dict


def create_current_status_dictionary(station_status_reporter) -> dict:
    current_status_dictionary = station_status_reporter.get_current_status()
    current_status_dictionary["customer_name"] = f"{station_status_reporter.customer_name}"
    current_status_dictionary["date_checked"] = convert_datetime_string(datetime.now())
    # Get all hours online
    hours_online_dict = station_status_reporter.get_daily_weekly_hours_online()
    current_status_dictionary["weekly_hours"] = hours_online_dict["weekly_hours"]
    current_status_dictionary["daily_hours"] = hours_online_dict["daily_hours"]

    return current_status_dictionary

    # days_online = station_status_reporter.get_days_online()
    # current_status_dictionary["days_online"] = f"{days_online}/7 days"
