from run import get_cisco_stock_price
import os


def test_get_api_request():
    kafka_api_get_cisco_stock = get_cisco_stock_price.API_Get_Stock()
    print("KEY")
    print(os.environ['STOCK_API_KEY'])

    out = kafka_api_get_cisco_stock._get_api_request(os.environ['STOCK_API_KEY'])
    assert out is not False


def test_add_timestamp_to_response():
    # Create some example data to add
    data = {
        "key": "value"
    }

    kafka_api_get_cisco_stock = get_cisco_stock_price.API_Get_Stock()

    out = kafka_api_get_cisco_stock._add_timestamp_to_response(data)
    assert out['timestamp'] >= 1
