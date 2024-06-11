from datetime import date, timedelta
from Database.fetch import get_latest_data, get_date_range_data, get_custom_query
from Features.Data_Processing.utils import convert_to_dictionary
from Utils.dates import get_date_today, get_last_week_date, convert_datetime_string


def is_offline_today(data):
    today = date.today()
    converted_data = convert_to_dictionary(data)
    return converted_data['Date_Time'].date() < today


def get_current_status(cursor, station_name):

    latest_data = get_latest_data(cursor, station_name)
    station_dictionary = {
        "station_name": station_name,
        "current_status": "Online",
    }

    if latest_data:
        offline = is_offline_today(latest_data)
        station_dictionary["latest_data"] = convert_datetime_string(latest_data.Date_Time)
        if offline:
            station_dictionary["current_status"] = "Offline"
        else:
            station_dictionary["current_status"] = "Online"

    elif latest_data is None:
        station_dictionary["current_status"] = "Offline"
        station_dictionary["latest_data"] = "Not Available  "

    return station_dictionary


def get_days_online(cursor, station_name):
    customer_data = get_date_range_data(cursor, station_name, "2021-8-01", "2021-08-27 16:00:00.000")
    date_last_week_from_now = get_last_week_date()
    date_today = get_date_today()

    # For test cases only
    test1 = date(2021, 1, 1)
    test2 = test1 - timedelta(days=7)

    online_stations_counter = 0
    while test2 < test1:

        data = get_custom_query(cursor, f"SELECT * FROM {station_name} WHERE Date_Time = '{test1}'")

        if data:
            online_stations_counter = online_stations_counter + 1

        test1 = test1 - timedelta(days=1)

    return online_stations_counter
