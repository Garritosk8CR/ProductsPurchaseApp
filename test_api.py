from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_order_with_valid_product_id_and_quantity():
    product_id = "01JQ3MT4NPYGH2BC6EEHR9WH5A"
    quantity = 5

    response = client.post(
        "http://localhost:8003/orders",
        json={
            "id": product_id,
            "quantity": quantity
        }
    )

    assert response.status_code == 200