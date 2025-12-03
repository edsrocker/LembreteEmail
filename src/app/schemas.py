from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class CustomerCreate(BaseModel):
    name: str = Field(..., examples=["Maria Silva"])
    email: EmailStr = Field(..., examples=["contato@cliente.com"])


class Customer(CustomerCreate):
    id: int


class InvoiceCreate(BaseModel):
    customer_id: int = Field(..., examples=[1])
    amount: float = Field(..., gt=0, examples=[199.9])
    due_date: date = Field(..., examples=["2024-10-15"])
    description: Optional[str] = Field(None, examples=["Mensalidade"])


class Invoice(InvoiceCreate):
    id: int


class ReminderRequest(BaseModel):
    invoice_id: int = Field(..., examples=[1])
    send_at: Optional[date] = Field(
        None,
        description="Data alvo para o lembrete; se omitida, assume hoje",
        examples=["2024-10-10"],
    )


class ReminderResponse(BaseModel):
    message: str
    invoice_id: int
