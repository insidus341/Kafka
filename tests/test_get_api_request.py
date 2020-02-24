from run import get_cisco_stock_price


def test_get_api_request():
    out = get_cisco_stock_price.get_api_request()
    assert out is not False