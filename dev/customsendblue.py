import os
import requests
import redis
from sendblue import Sendblue
from dotenv import load_dotenv

SENDBLUE_API_KEY = "9b87cae3e57be74bb0dfb7d64089f2f2"
SENDBLUE_API_SECRET = "ea7ef96d1e1596ba6a7df06b9be65af7"


def sendContactCard(numberID):
    endpoint = "https://api.sendblue.co/api/send-message"
    vcfAsset = 'https://storage.cloud.google.com/aiatl/DgVg.vcf'
    status_callback = "https://eo1c50zlelcm28q.m.pipedream.net"

    headers = {
        # "sb-api-key-id": os.environ["send_blue_api_key"],
        # "sb-api-secret-key": os.environ["send_blue_api_secret"],
        "sb-api-key-id": SENDBLUE_API_KEY,
        "sb-api-secret-key": SENDBLUE_API_SECRET,
        "content-Type": "application/json"
    }
    data = {
        "number": numberID,
        "media_url": vcfAsset
    }
    response = requests.post(endpoint, headers=headers, json=data)


def sendMessage(numberID, message):
    endpoint = "https://api.sendblue.co/api/send-message"
    status_callback = "https://eo1c50zlelcm28q.m.pipedream.net"

    headers = {
        "sb-api-key-id": SENDBLUE_API_KEY,
        "sb-api-secret-key": SENDBLUE_API_SECRET,
        "content-Type": "application/json"
    }

    data = {
        "number": numberID,
        "content": message
    }
    response = requests.post(endpoint, headers=headers, json=data)
