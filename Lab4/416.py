from datetime import datetime, timezone, timedelta

def parse_line(line):
    
    date_part, time_part, tz_part = line.split()

    dt = datetime.strptime(date_part + " " + time_part, "%Y-%m-%d %H:%M:%S")

    sign = 1 if "+" in tz_part else -1
    hours = int(tz_part[4:6])
    minutes = int(tz_part[7:9])

    offset = timedelta(hours=hours, minutes=minutes)
    if sign == -1:
        offset = -offset

    return dt.replace(tzinfo=timezone(offset))

start = parse_line(input())
end = parse_line(input())


seconds = int((end - start).total_seconds())
print(seconds)