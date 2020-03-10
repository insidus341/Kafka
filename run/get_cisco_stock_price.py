from json import dumps
import requests
import datetime
import os

# environmental variables are added in github
STOCK_API_KEY = os.environ['STOCK_API_KEY']


class APIGetStock:

    def get_stock_price(self):

        try:
            response = self._get_api_request(STOCK_API_KEY)
            response_with_timestamp = self._add_timestamp_to_response(response)
            response_with_otherdata = self._add_otherdata_to_response(response_with_timestamp)
        except Exception as e:
            # we don't need to anything if this fails
            return False

        # send this data to our kafka topic
        self._send_to_kafka(response_with_otherdata)

    def _get_api_request(self, api_key):
        response = requests.get(
            "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=CSCO&interval=5min&apikey=" + api_key)

        # 200 indicates this was successful
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError()


    def _add_timestamp_to_response(self, data):
        # this data does not include a timestamp, let's add one
        timestamp = datetime.datetime.now().timestamp()
        data["timestamp"] = timestamp

        return data


    def _add_otherdata_to_response(self, data):
        data["otherdata"] = "hello this is a test"

        return data


    def _send_to_kafka(self, data):
        producer.send('API-CiscoStock', value=data)


if __name__ == "__main__":
    # included here as it's not available for Github CI/CD
    from kafka import KafkaProducer

    # create a handler for our kafka producer
    # makes this global
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))

    # lets go
    kafka_api_cisco_stock = APIGetStock()
    APIGetStock.get_stock_price()
