from json import dumps
import requests
import datetime

# environmental variables are added in github
import os

class API_Get_Stock():

    def get_stock_price(self):

        try:
            response = self.get_api_request(os.environ['STOCK_API_KEY'])
            response_with_timestamp = self.add_timestamp_to_response(response)
            response_with_otherdata = self.add_otherdata_to_response(response_with_timestamp)
        except:
            # we don't need to anything if this fails
            return False

        # send this data to our kafka topic
        self.send_to_kafka(response_with_otherdata)

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
    kafka_api_cisco_stock = API_Get_Stock()
    API_Get_Stock.run()
