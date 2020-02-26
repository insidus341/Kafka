from run import get_cisco_stock_price
import os

from run.webhook_server import app

def test_webhook_server_startup():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert response.data == b'<h1>Webhook Listener</h1>'