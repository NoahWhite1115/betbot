from datetime import datetime, timedelta


def strToTime(string: str):
    return datetime.strptime(string, "%Y-%m-%d %H:%M:%S.%f")


def dateAsStr(date: datetime, timezone_diff=-8):
    return str((date + timedelta(hours=timezone_diff)).date())


def dateTimeAsStr(date: datetime, timezone_diff=-8):
    return (date + timedelta(hours=timezone_diff)).strftime("%Y-%m-%d %I:%M %p")
