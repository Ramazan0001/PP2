from datetime import datetime, timezone, timedelta

def parse_line(line):
    date_part, tz_part = line.split()
    dt = datetime.strptime(date_part, "%Y-%m-%d")

    sign = 1 if "+" in tz_part else -1
    hours = int(tz_part[4:6])
    minutes = int(tz_part[7:9])

    offset = timedelta(hours=hours, minutes=minutes)
    if sign == -1:
        offset = -offset

    return dt.replace(tzinfo=timezone(offset))

def is_leap(year):
    return (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)

birth_dt = parse_line(input())
now_dt = parse_line(input())

b_month = birth_dt.month
b_day = birth_dt.day

def make_birthday(year, birth_tz):
    
    if b_month == 2 and b_day == 29 and not is_leap(year):
        return datetime(year, 2, 28, tzinfo=birth_tz)
    return datetime(year, b_month, b_day, tzinfo=birth_tz)

birth_tz = birth_dt.tzinfo

cand1 = make_birthday(now_dt.year, birth_tz)
cand2 = make_birthday(now_dt.year + 1, birth_tz)


now_utc = now_dt.astimezone(timezone.utc)
cand1_utc = cand1.astimezone(timezone.utc)
cand2_utc = cand2.astimezone(timezone.utc)

if cand1_utc >= now_utc:
    target = cand1_utc
else:
    target = cand2_utc

diff_seconds = (target - now_utc).total_seconds()

print(int(diff_seconds // 86400))