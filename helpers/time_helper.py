from datetime import datetime, timedelta

def strToTime(string: str):
    return datetime.strptime(string, '%Y-%m-%d %H:%M:%S.%f')

def dateAsStr(date: datetime, timezone_diff: int):
    return str((date + timedelta(hours = timezone_diff)).date())