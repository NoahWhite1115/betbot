import sys

sys.path.append("../src")

from src.helpers.conversion_helper import responseToAllPlayerData
from src.dataClasses.playerData import playerData
import unittest


class TestConversionHelper(unittest.TestCase):
    def test_responseToAllPlayerData_happy_path(self):
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

        self.assertEqual(expected, output)

    def getTestMultiBetResponse(self):
        response = {
            "Items": [
                {
                    "next_pay_period": "2022-06-01 00:00:01.313461",
                    "bet_data": True,
                    "user_id": "bet_data",
                    "next_checkin": "2022-08-14 00:00:01.099442",
                    "days_per_checkin_period": 1,
                    "start_date": "",
                    "months_per_pay_period": 3,
                    "increment_owes": 25,
                    "last_checkin": "2022-08-13 00:00:01.099439",
                    "game_id": "100000000000000000",
                    "admins": [000000000, 10000000],
                },
                {
                    "next_pay_period": "2022-10-01 06:59:00.313461",
                    "bet_data": True,
                    "user_id": "bet_data",
                    "next_checkin": "2022-08-15 06:59:00.196492",
                    "days_per_checkin_period": 7,
                    "start_date": "2022-01-01 00:00:01.313461",
                    "months_per_pay_period": 3,
                    "increment_owes": 25,
                    "last_checkin": "2022-06-24 12:07:07.196472",
                    "game_id": "100000000000000001",
                    "admins": [000000000, 10000000],
                },
            ],
            "Count": 2,
            "ScannedCount": 2,
            "ResponseMetadata": {
                "RequestId": "9ONDJ0LIDT4DJT4G5H5T5FK78JVV4KQNSO5AEMVJF66Q9ASUAAJG",
                "HTTPStatusCode": 200,
                "HTTPHeaders": {
                    "server": "Server",
                    "date": "Sun, 14 Aug 2022 18:42:49 GMT",
                    "content-type": "application/x-amz-json-1.0",
                    "content-length": "792",
                    "connection": "keep-alive",
                    "x-amzn-requestid": "9ONDJ0LIDT4DJT4G5H5T5FK78JVV4KQNSO5AEMVJF66Q9ASUAAJG",
                    "x-amz-crc32": "3853391611",
                },
                "RetryAttempts": 0,
            },
        }

        return response

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
