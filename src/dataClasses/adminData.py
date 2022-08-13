from dataclasses import dataclass


@dataclass
class adminData:
    id: int
    adminOf: list(int)
    messagePerms: bool
    editPerms: bool
    startVotePerms: bool
