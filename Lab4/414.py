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
        
    tz = timezone(offset)
    
    return dt.replace(tzinfo=tz)

a = parse_line(input())
b = parse_line(input())

diff_seconds = abs((a - b).total_seconds())

print(int(diff_seconds // 86400))