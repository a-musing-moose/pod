from django.contrib import admin
from django.urls import path

from pod.examples.views import InvoiceView, TicketView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("invoice/", InvoiceView.as_view()),
    path("ticket/", TicketView.as_view()),
]
