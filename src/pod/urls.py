from django.contrib import admin
from django.urls import path

from pod.examples.views import InvoiceView, TicketView

from . import views

urlpatterns = [
    path("humans.txt", views.HumansTxt.as_view()),
    path("release.json", views.Release.as_view()),
    path("admin/", admin.site.urls),
    path("invoice/", InvoiceView.as_view()),
    path("ticket/", TicketView.as_view()),
]
