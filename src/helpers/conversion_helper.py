from src.exceptions.ddbExceptions import (
    playerNotFoundException,
    channelNotFoundException,
)
from src.dataClasses import playerData, betData


def responseToPlayerData(response):
    items = response["Items"]

    if len(items) != 1:
        raise (playerNotFoundException)

    playerDict = items[0]
    return playerData.playerData(
        int(playerDict["game_id"]),
        int(playerDict["user_id"]),
        playerDict["display_name"],
        playerDict["active"],
        playerDict["owes"],
        playerDict["lives"],
        playerDict["last_checkin"],
    )


def responseToAllPlayerData(response):
    items = response["Items"]

    if len(items) == 0:
        raise (playerNotFoundException)

    out = []
    for playerDict in items:
        out.append(
            playerData.playerData(
                int(playerDict["game_id"]),
                int(playerDict["user_id"]),
                playerDict["display_name"],
                playerDict["active"],
                playerDict["owes"],
                playerDict["lives"],
                playerDict["last_checkin"],
            )
        )

    return out


def responseToAllBetData(response):
    items = response["Items"]

    if len(items) == 0:
        raise (channelNotFoundException)

    out = []
    for betDict in items:
        out.append(
            betData.betData(
                int(betDict["game_id"]),
                betDict["next_checkin"],
                betDict["last_checkin"],
                betDict["start_date"],
                int(betDict["days_per_checkin_period"]),
                int(betDict["months_per_pay_period"]),
                betDict["next_pay_period"],
                int(betDict["increment_owes"]),
                betDict["admins"],
            )
        )
    return out


def responseToBetData(response):
    items = response["Items"]

    if len(items) != 1:
        raise (channelNotFoundException("No channel with id"))

    betDict = items[0]
    return betData.betData(
        int(betDict["game_id"]),
        betDict["next_checkin"],
        betDict["last_checkin"],
        betDict["start_date"],
        int(betDict["days_per_checkin_period"]),
        int(betDict["months_per_pay_period"]),
        betDict["next_pay_period"],
        int(betDict["increment_owes"]),
        betDict["admins"],
    )
