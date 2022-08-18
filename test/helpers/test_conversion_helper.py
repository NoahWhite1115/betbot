import sys

sys.path.append("../src")

from src.helpers.conversion_helper import responseToAllPlayerData
from src.dataClasses.playerData import playerData
import unittest


class TestConversionHelper(unittest.TestCase):
    def test_responseToPlayerData_happy_path(self):
        testResponse = self.getTestMultiPlayerResponse()

        expected = [
            playerData(
                000000000000000,
                123445677890000000,
                "TEST_USER_1",
                True,
                150,
                2,
                "2022-08-12 16:29:58.051291",
            ),
            playerData(
                000000000000000,
                123445677890000001,
                "TEST_USER_2",
                True,
                150,
                1,
                "2022-08-14 00:47:57.151372",
            ),
        ]

        output = responseToAllPlayerData(testResponse)

        self.assertEquals(expected, output)

    def getTestMultiPlayerResponse(self):
        response = {
            "Items": [
                {
                    "bet_data": False,
                    "active": True,
                    "user_id": "123445677890000000",
                    "owes": 150,
                    "display_name": "TEST_USER_1",
                    "last_checkin": "2022-08-12 16:29:58.051291",
                    "lives": 2,
                    "game_id": "000000000000000",
                },
                {
                    "bet_data": False,
                    "active": True,
                    "user_id": "123445677890000001",
                    "owes": 150,
                    "display_name": "TEST_USER_2",
                    "last_checkin": "2022-08-14 00:47:57.151372",
                    "lives": 1,
                    "game_id": "000000000000000",
                },
            ],
            "Count": 4,
            "ScannedCount": 5,
            "ResponseMetadata": {
                "RequestId": "14TBKO5DI6P7NCR2OMGMGO161FVV4KQNSO5AEMVJF66Q9ASUAAJG",
                "HTTPStatusCode": 200,
                "HTTPHeaders": {
                    "server": "Server",
                    "date": "Sun, 14 Aug 2022 18:41:53 GMT",
                    "content-type": "application/x-amz-json-1.0",
                    "content-length": "1010",
                    "connection": "keep-alive",
                    "x-amzn-requestid": "14TBKO5DI6P7NCR2OMGMGO161FVV4KQNSO5AEMVJF66Q9ASUAAJG",
                    "x-amz-crc32": "3787604465",
                },
                "RetryAttempts": 0,
            },
        }

        return response
