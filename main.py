import json
import os
import pprint
import re
import sys
import time
from base64 import b64decode
from typing import Pattern

import requests
from dotenv import load_dotenv

from db import add_data_to_db

load_dotenv()
URL: Pattern = re.compile("(https?)://([^/\r\n]+)(/[^\r\n]*)?")

header = {
    'X-Tasktest-Token': os.getenv('token')
}


def free_chat_data(url: URL, header: dict) -> None:

    """

    Method to get data from free chat.
    :param url: url API
    :param header: heater necessary part of request
    :return:
    """

    response = requests.get(f"{url}chat/spare?crm=TEST&domain=test", headers=header)
    original_stdout = sys.stdout

    with open('free_chat.json', 'w') as file_json:
        sys.stdout = file_json
        print(json.dumps(response.json(), indent=1))
        sys.stdout = original_stdout
        add_data_to_db(json.dumps(response.json()))


def chat_init(url: URL, instance: int, token: str, param: dict, header: dict) -> str:
    """

    Chat initialization method.

    :param url: url API
    :param instance: ID from data json
    :param token: token from data json
    :param param: initialization chat parameter
    :param header: heater necessary part of request
    :return: QR code

    """

    start_time = time.time()
    while True:
        response = requests.get(f"{url}instance{instance}/status?token={token}",
                                params=param,
                                headers=header).json()
        if response.get('state') == 'got qr code':
            return response.get('qrCode')
        end_time = time.time() - start_time
        if end_time > 100:
            return False
        time.sleep(5)


def get_chat():
    load_dotenv()
    url_api = 'https://dev.wapp.im/v3/'
    token = os.getenv('token')

    header = {'X-Tasktest-Token': token}

    free_chat_data(url_api, header)
    with open('free_chat.json', 'r') as file_json:
        data_json = json.load(file_json)
    file_json.close()
    instance = data_json.get('id')
    token = data_json.get('token')
    qr_code = chat_init(url_api, instance=instance, token=token, param={'full': '1'}, header=header)
    if qr_code:
        sys.stdout.write('The QR code save successfully.')
        sys.stdout = open('qr_code.png', 'bw')
        sys.stdout.write(b64decode(qr_code.split(',')[1]))
        sys.stdout.close()
    else:
        sys.stdout.write('Error, initialization chat')


def send_message(url: URL, instance: int, token: str, headers: dict, body: dict) -> None:
    """
    Method to send message
    :param url: url API
    :param instance: ID from data json
    :param token: token from data json
    :param headers: heater necessary part of request
    :param body: body of the request
    :return: None
    """
    response = requests.post(f"{url}instance{instance}/sendMessage?token={token}",
                             headers=headers,
                             data=body)
    pprint(response.json())


def message_init() -> None:
    """
    Main method to initialize send message method.
    :return: None
    """
    load_dotenv()
    token = os.getenv('token')
    phone = os.getenv('phone')
    body_body = os.getenv('body_body')

    header = {'X-Tasktest-Token': token}
    url = 'https://dev.whatsapp.sipteco.ru/v3/'

    body = {'phone': phone, 'body': body_body}

    with open('free_chat.json', 'r') as file_json:
        data_json = json.load(file_json)
    instance = data_json.get('id')
    token = data_json.get('token')
    send_message(url, instance, token, header, body)


def main():
    try:
        get_chat()
    except Exception:
        sys.stdout.write('Error, no free chat data')
        return

    time.sleep(10)

    message_init()


if __name__ == '__main__':
    main()

