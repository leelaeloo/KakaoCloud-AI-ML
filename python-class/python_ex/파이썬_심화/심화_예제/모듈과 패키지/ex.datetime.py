

from datetime import datetime, date, time, timedelta

now = datetime.now()
print(f"\n현재 : {now}")

specific_date = datetime(2025, 12, 31, 23, 59, 59)
print(f"특정 일시 : {specific_date}")

date_str = now.strftime("%Y-%m-%d %H:%M:%S")
print(f"형식화 된 날짜 : {date_str}")

parsed_date = datetime.strptime("2025-08-29", "%Y-%m-%d")
print(f"파싱된 날짜 : {parsed_date}\n")

