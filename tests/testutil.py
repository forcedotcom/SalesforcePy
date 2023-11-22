import json
import os
import responses
import SalesforcePy as sfdc

username = "jsoap@universalcontainers.com"
password = "p@ssword1"
client_id = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
client_secret = "123456789123456789"
login_url = "login.salesforce.com"
org_id = "00Di0000000xxxx"
version = "39.0"
proxies = {"https": "mock.proxy.server.com:8080"}
tests_dir = os.path.dirname(os.path.realpath(__file__))
mock_responses = {}


def add_response(res_key):
    if res_key in mock_responses:
        res = mock_responses[res_key]
    else:
        with open(os.path.join(tests_dir, "fixtures/%s.json" % res_key)) as f:
            res = mock_responses[res_key] = json.loads(f.read())

    body =  None if res["body"] is None else json.dumps(res["body"])

    responses.add(
        res["method"],
        res["url"],
        body=body,
        status=res["status_code"],
        content_type=res["content_type"])


def get_client():
    client = sfdc.client(
        username=username,
        password=password,
        client_id=client_id,
        client_secret=client_secret
    )
    client.login()
    return client


def get_client_with_proxy():
    client = sfdc.client(
        username=username,
        password=password,
        client_id=client_id,
        client_secret=client_secret,
        proxies=proxies
    )
    client.login()
    return client
