from datetime import date, timedelta
from Features.Data_Processing.utils import convert_to_dictionary
from Utils.dates import get_date_today, get_last_week_date, convert_datetime_string


def is_offline_today(data):
    today = date.today()
    converted_data = convert_to_dictionary(data)
    return converted_data['date_time'].date() < today


def get_current_status(database_model, station_name):

    latest_data = database_model.get_latest_data(station_name)
    station_dictionary = {
        "station_name": station_name,
        "current_status": "Online",
    }

    if latest_data:
        offline = is_offline_today(latest_data)
        station_dictionary["latest_data"] = convert_datetime_string(latest_data.date_time)
        if offline:
            station_dictionary["current_status"] = "Offline"
        else:
            station_dictionary["current_status"] = "Online"

    elif latest_data is None:
        station_dictionary["current_status"] = "Offline"
        station_dictionary["latest_data"] = "Not Available  "

    return station_dictionary


def get_days_online(database_model, station_name):

    date_last_week_from_now = get_last_week_date()
    date_today = get_date_today()

    online_stations_counter = 0
    while date_last_week_from_now < date_today:
        data = database_model.get_data_custom_query(
            f"SELECT * FROM {station_name} WHERE Date_Time = '{date_today}'"
        )
        if data:
            online_stations_counter = online_stations_counter + 1
        date_today = date_today - timedelta(days=1)

    return online_stations_counter


def get_hours_online(database_model) -> dict:
    hours_online = {
        "days": [],
        "hours_daily": [],
        "hours_weekly": 0
    }

    date_now = date.today()
    weekly_total_hours_online = 0

    for i in range(7):

        query = (f"SELECT Date_Time FROM data_table WHERE Date_Time <= '{date_now}'"
                 f"AND Date_Time > '{date_now - timedelta(days=1)}' ")
        data_list = database_model.get_data_custom_query(query)

        # Append to list
        hours_list = []
        for data in data_list:
            hour = data.Date_Time.strftime('%H')
            hours_list.append(hour)

        # Using set only takes unique elements
        daily_hours_online = len(set(hours_list))

        month_day = date_now.strftime('%b %d')
        hours_online["days"].append(month_day)

        daily_data = {month_day: daily_hours_online}
        hours_online["hours_daily"].append(daily_data)

        weekly_total_hours_online = weekly_total_hours_online + daily_hours_online
        date_now = date_now - timedelta(days=1)

    hours_online["hours_weekly"] = weekly_total_hours_online

    return hours_online
