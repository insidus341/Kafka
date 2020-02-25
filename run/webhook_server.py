from flask import Flask, request
from OpenSSL import SSL

from json import dumps
from kafka import KafkaProducer

import os

# Create a handler for Flask
app = Flask(__name__)
SSL_CERT = os.environ['SSL_CERT']
SSL_KEY = os.environ['SSL_KEY']
HOST = os.environ['WEBHOOK_HOST']
PORT = os.environ['WEBHOOK_PORT']


@app.route('/', methods=['POST', 'GET'])
def index():
        if request.method == 'GET':
            return '<h1>Webhook Listener</h1>'

        if request.method == 'POST':
            data = request.get_json()
            producer.send('', value=data)

            return '{"success":"true"}'


if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))

    context = (SSL_CERT, SSL_KEY) # certificate and key file
    app.run(host=HOST, port=PORT, ssl_context=context, threaded=True, debug=True)

