from datetime import date

from fastapi.testclient import TestClient

from src.app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_customer_and_invoice_and_schedule_reminder():
    customer = client.post(
        "/api/customers",
        json={"name": "Cliente Teste", "email": "cliente@exemplo.com"},
    )
    assert customer.status_code == 201
    customer_id = customer.json()["id"]

    invoice = client.post(
        "/api/invoices",
        json={
            "customer_id": customer_id,
            "amount": 150.75,
            "due_date": date.today().isoformat(),
            "description": "Plano mensal",
        },
    )
    assert invoice.status_code == 201
    invoice_id = invoice.json()["id"]

    reminder = client.post(
        "/api/reminders",
        json={"invoice_id": invoice_id},
    )
    assert reminder.status_code == 200
    payload = reminder.json()
    assert payload["invoice_id"] == invoice_id
    assert "Lembrete registrado" in payload["message"]
