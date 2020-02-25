from json import dumps
import requests
import datetime

# environmental variables are added in github
import os


def run():

    try:
        response = get_api_request(os.environ['STOCK_API_KEY'])
        response_with_timestamp = add_timestamp_to_response(response)
    except:
        # we don't need to anything if this fails
        return False

    # send this data to our kafka topic
    send_to_kafka(response_with_timestamp)


def get_api_request(api_key):
    response = requests.get(
        "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=CSCO&interval=5min&apikey=" + api_key)

    # 200 indicates this was successful
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError()


def add_timestamp_to_response(data):
    # this data does not include a timestamp, let's add one
    timestamp = datetime.datetime.now().timestamp()
    data["timestamp"] = timestamp

    return data


def send_to_kafka(data):
    producer.send('API-CiscoStock', value=data)


if __name__ == "__main__":
    # included here as it's not available on github
    from kafka import KafkaProducer

    # create a handler for our kafka producer
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))

    # lets go
    run()
