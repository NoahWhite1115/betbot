from dataclasses import dataclass


@dataclass
class playerData:
    gameId: int
    userId: int
    name: str
    active: bool
    owes: int
    lives: int
    lastCheckin: str
