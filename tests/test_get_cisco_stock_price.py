from run import get_cisco_stock_price
import os

def test_get_api_request():
    out = get_cisco_stock_price.get_api_request(os.environ['STOCK_API_KEY'])
    assert out is not False


def test_add_timestamp_to_response():
    data = {
        "key": "value"
    }

    out = get_cisco_stock_price.add_timestamp_to_response(data)
    assert out['timestamp'] >= 1
