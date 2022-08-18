import boto3


class SecretClient:
    def __init__(self, region):
        session = boto3.session.Session()
        self.client = session.client(service_name="secretsmanager", region_name=region)

    def getSecret(self, secret_name):

        get_secret_value_response = self.client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response["SecretString"]
        return secret
