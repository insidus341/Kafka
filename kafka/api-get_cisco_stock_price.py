from kafka import KafkaProducer
from json import dumps
import requests
import datetime

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x:
                         dumps(x).encode('utf-8'))



def run():
    response = requests.get(
        "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=CSCO&interval=5min&apikey=PR1WOTAE73NO13KD")

    if response.status_code is 200:
         data = response.json()
         timestamp = datetime.datetime.now().timestamp()

         data["Global Quote"]["timestamp"] = timestamp
         producer.send('API-GET-CiscoStock', value=data)

if __name__ == "__main__":
    run()
