from json import dumps
import requests
import datetime

import os


def run():

    try:
        response = get_api_request(os.environ['stock_api_key'])
        response_with_timestamp = add_timestamp_to_response(response)
    except:
        return False

    send_to_kafka(response_with_timestamp)


def get_api_request(api_key):
    response = requests.get(
        "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=CSCO&interval=5min&apikey=" + api_key)

    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError()


def add_timestamp_to_response(data):
    timestamp = datetime.datetime.now().timestamp()

    data["timestamp"] = timestamp
    return data


def send_to_kafka(data):
    producer.send('API-CiscoStock', value=data)
    producer.send('API-CiscoStock', value="test")


if __name__ == "__main__":
    from kafka import KafkaProducer
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))

    run()
