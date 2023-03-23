from dataclasses import dataclass


@dataclass
class betData:
    id: int
    nextCheckin: str
    lastCheckin: str
    startTime: str
    daysPerCheckinPeriod: int
    monthsPerPayPeriod: int
    nextPayPeriod: str
    incrementOwes: int
    admins: list[int]
