from collections import defaultdict
from itertools import count
from typing import Dict

from .schemas import Customer, CustomerCreate, Invoice, InvoiceCreate


class InMemoryStorage:
    def __init__(self) -> None:
        self._customer_counter = count(start=1)
        self._invoice_counter = count(start=1)
        self._customers: Dict[int, Customer] = {}
        self._invoices: Dict[int, Invoice] = {}
        self._customer_invoices: dict[int, list[int]] = defaultdict(list)

    def add_customer(self, payload: CustomerCreate) -> Customer:
        customer_id = next(self._customer_counter)
        customer = Customer(id=customer_id, **payload.model_dump())
        self._customers[customer_id] = customer
        return customer

    def get_customer(self, customer_id: int) -> Customer | None:
        return self._customers.get(customer_id)

    def add_invoice(self, payload: InvoiceCreate) -> Invoice:
        if payload.customer_id not in self._customers:
            raise ValueError("Cliente não encontrado para o boleto informado.")

        invoice_id = next(self._invoice_counter)
        invoice = Invoice(id=invoice_id, **payload.model_dump())
        self._invoices[invoice_id] = invoice
        self._customer_invoices[payload.customer_id].append(invoice_id)
        return invoice

    def get_invoice(self, invoice_id: int) -> Invoice | None:
        return self._invoices.get(invoice_id)

    def list_invoices_for_customer(self, customer_id: int) -> list[Invoice]:
        ids = self._customer_invoices.get(customer_id, [])
        return [self._invoices[i] for i in ids]


storage = InMemoryStorage()
