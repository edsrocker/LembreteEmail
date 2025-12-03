from datetime import date

from .schemas import Invoice, ReminderRequest, ReminderResponse
from .storage import storage


class ReminderService:
    def __init__(self, repo=storage) -> None:
        self.repo = repo

    def schedule_reminder(self, payload: ReminderRequest) -> ReminderResponse:
        invoice = self.repo.get_invoice(payload.invoice_id)
        if not invoice:
            raise ValueError("Boleto não encontrado para agendamento.")

        send_date = payload.send_at or date.today()
        return ReminderResponse(
            message=(
                "Lembrete registrado para envio em "
                f"{send_date.isoformat()} para o boleto #{invoice.id}"
            ),
            invoice_id=invoice.id,
        )


reminder_service = ReminderService()
