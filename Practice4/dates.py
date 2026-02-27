#1
import datetime
x = datetime.datetime.now()
print(x)
#2
import datetime
x = datetime.datetime.now()
print(x.year)
print(x.strftime("%A"))
#3
import datetime

x = datetime.datetime(2018, 6, 1)

print(x.strftime("%B"))

#Task1
today = datetime.date.today()
new_date = today - datetime.timedelta(days=5)

print(new_date)

#Task2
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
tomorrow = today + datetime.timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)

#Task3
now = datetime.datetime.now()
without_microseconds = now.replace(microsecond=0)

print(without_microseconds)

#Task4
import datetime

date1 = datetime.datetime(2026, 2, 20, 10, 0, 0)
date2 = datetime.datetime(2026, 2, 27, 12, 30, 0)

difference = date2 - date1
print(difference.total_seconds())