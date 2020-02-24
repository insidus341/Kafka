from run import get_cisco_stock_price


def test_add_timestamp_to_response():
    data = {
        "key": "value"
    }

    out = get_cisco_stock_price.add_timestamp_to_response(data)
    assert out['timestamp'] >= 1