import typing

from django.views import generic

from pod.printing import views


class InvoiceView(views.PDFTemplateView):
    pdf_filename = "invoice.pdf"
    template_name = "invoice/invoice.html"
    pdf_attachment = False

    def get_context_data(self, **kwargs: typing.Any) -> dict[str, typing.Any]:
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "invoice_number": "12345",
                "invoice_date": "March 31, 2018",
                "items": [
                    {
                        "description": "Website design",
                        "price": "$34.20",
                        "quantity": 100,
                        "subtotal": "$3,420.00",
                    },
                    {
                        "description": "Website development",
                        "price": "$45.50",
                        "quantity": 100,
                        "subtotal": "$4,550.00",
                    },
                    {
                        "description": "Website integration",
                        "price": "$25.75",
                        "quantity": 100,
                        "subtotal": "$2,575.00",
                    },
                ],
                "total_due": "$10,545.00",
                "due_date": "May 10, 2018",
                "account_number": "132 456 789 012",
            }
        )
        return context


class TicketView(generic.TemplateView):
    template_name = "ticket/ticket.typ"
    template_engine = "typst"
    content_type = "application/pdf"

    def get_context_data(self, **kwargs: typing.Any) -> dict[str, typing.Any]:
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "name": "Jonathan Moss",
                "flight": "QF171",
                "gate": "29",
                "seat": "26E",
                "zone": "4",
                # "when": datetime.now(zoneinfo.ZoneInfo("Australia/Melbourne")),
                "date": "Sept 12, 2025",
                "time": "5:10pm",
                "barcode": "19780912",
                "from": "MEL",
                "to": "WLG",
            }
        )
        return context
