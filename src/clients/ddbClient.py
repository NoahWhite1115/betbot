import boto3
from boto3.dynamodb.conditions import Key, Attr
from src.exceptions.ddbExceptions import (
    playerNotFoundException,
    channelNotFoundException,
)
from src.helpers.conversion_helper import (
    responseToPlayerData,
    responseToBetData,
    responseToAllPlayerData,
    responseToAllBetData,
)


class DynamoClient:
    def __init__(self):
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table("betbot_data")

    def getBetData(self, channelId):
        try:
            response = self.table.query(
                KeyConditionExpression=(
                    Key("game_id").eq(str(channelId)) & Key("user_id").eq("bet_data")
                ),
                ScanIndexForward=False,
            )
        except self.dynamodb.meta.client.exceptions.ResourceNotFoundException:
            raise (channelNotFoundException("No channel with id " + str(channelId)))

        return responseToBetData(response)

    def getAllBetData(self):
        response = self.table.query(
            IndexName="all-bets",
            KeyConditionExpression=(Key("user_id").eq("bet_data")),
            ScanIndexForward=False,
        )

        return responseToAllBetData(response)

    def getPlayerData(self, channelId, playerId):
        try:
            response = self.table.query(
                KeyConditionExpression=(
                    Key("game_id").eq(str(channelId)) & Key("user_id").eq(str(playerId))
                ),
                ScanIndexForward=False,
            )
        except self.dynamodb.meta.client.exceptions.ResourceNotFoundException:
            raise (playerNotFoundException("No channel with id " + str(channelId)))

        return responseToPlayerData(response)

    def getAllPlayerData(self, channelId):
        response = self.table.query(
            KeyConditionExpression=Key("game_id").eq(str(channelId)),
            FilterExpression=Attr("bet_data").eq(False),
        )

        return responseToAllPlayerData(response)

    def updateBetData(self, channelId, betData):

        UpdateExpression = "SET next_checkin = :nextCheckin, last_checkin = :lastCheckin, next_pay_period = :nextPayPeriod"
        ExpressionAttributeValues = {
            ":nextCheckin": str(betData.nextCheckin),
            ":lastCheckin": str(betData.lastCheckin),
            ":nextPayPeriod": str(betData.nextPayPeriod),
        }

        self.table.update_item(
            Key={"game_id": str(channelId), "user_id": "bet_data"},
            UpdateExpression=UpdateExpression,
            ExpressionAttributeValues=ExpressionAttributeValues,
        )

    def updatePlayerData(self, channelId, playerId, playerData):

        UpdateExpression = "SET last_checkin = :lastCheckin, active = :active, lives = :lives, owes = :owes, display_name = :name"
        ExpressionAttributeValues = {
            ":lastCheckin": str(playerData.lastCheckin),
            ":name": playerData.name,
            ":active": playerData.active,
            ":lives": playerData.lives,
            ":owes": playerData.owes,
        }

        self.table.update_item(
            Key={"game_id": str(channelId), "user_id": str(playerId)},
            UpdateExpression=UpdateExpression,
            ExpressionAttributeValues=ExpressionAttributeValues,
        )
