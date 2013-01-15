from datetime import date
from datetime import timedelta
import time
import openpaths

import pymongo
from pymongo import MongoClient

connection = MongoClient('localhost', 20002)
db = connection.syncopathed
collection = db.locations

start_date = date(2012, 12, 1)
today = date.today()

difference = today - start_date
day_difference = difference.days

for past_day in range(day_difference):
    that_day = start_date + timedelta(days=past_day)
    end_of_that_day = that_day + timedelta(hours=24)

    start_unix_time = int(time.mktime(that_day.timetuple()))
    end_unix_time = int(time.mktime(end_of_that_day.timetuple()))
    num_points = 2000

    locations = openpaths.get_points(start_time=start_unix_time, end_time=end_unix_time, num_points=num_points)
    document = {}
    date = that_day.isoformat()

    document['date'] = date
    document['locations'] = locations

    collection.insert(document)
