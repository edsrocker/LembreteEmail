from fastapi import APIRouter, HTTPException, status

from ..schemas import (
    Customer,
    CustomerCreate,
    Invoice,
    InvoiceCreate,
    ReminderRequest,
    ReminderResponse,
)
from ..services import reminder_service
from ..storage import storage

router = APIRouter(tags=["reminders"])


@router.post("/customers", response_model=Customer, status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreate) -> Customer:
    return storage.add_customer(payload)


@router.post("/invoices", response_model=Invoice, status_code=status.HTTP_201_CREATED)
def create_invoice(payload: InvoiceCreate) -> Invoice:
    try:
        return storage.add_invoice(payload)
    except ValueError as exc:  # pragma: no cover - mapeado para HTTP
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("/reminders", response_model=ReminderResponse)
def schedule_reminder(payload: ReminderRequest) -> ReminderResponse:
    try:
        return reminder_service.schedule_reminder(payload)
    except ValueError as exc:  # pragma: no cover - mapeado para HTTP
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
