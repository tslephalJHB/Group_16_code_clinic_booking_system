import datetime
from datetime import timedelta

min_date = str(datetime.date.today() + 00:00) 
max_date = min_date + timedelta(7)


print(max_date)