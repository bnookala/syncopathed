from datetime import date
from datetime import timedelta
import time
import openpaths

import pymongo
from pymongo import MongoClient

connection = MongoClient('localhost', 20002)
db = connection.syncopathed
collection = db.locations

yesterday = date.today() - timedelta(days=1)
end_of_yesterday = yesterday + timedelta(hours=24)

start_of_yesterday_unix_time = int(time.mktime(yesterday.timetuple()))
end_of_yesterday_unix_time = int(time.mktime(end_of_yesterday.timetuple()))

num_points = 2000
locations = openpaths.get_points(
		start_time=start_of_yesterday_unix_time,
		end_time=end_of_yesterday_unix_time,
		num_points=num_points
		)

document = {}
document['date'] = yesterday.isoformat()
document['locations'] = locations

print document
collection.insert(document)
