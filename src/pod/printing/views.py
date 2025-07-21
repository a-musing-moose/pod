import typing

from django import http
from django.db import models
from django.views.generic import base, detail

from . import responses

ModelType = typing.TypeVar("ModelType", bound=models.Model)


class PDFTemplateView(responses.PDFTemplateResponseMixin, base.ContextMixin, base.View):
    """
    Django class-based template view that renders to a PDF.
    """

    def get(
        self, request: http.HttpRequest, *args: typing.Any, **kwargs: typing.Any
    ) -> http.HttpResponse:
        """
        Handle GET requests
        """
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class PDFDetailView(
    responses.PDFTemplateResponseMixin, detail.BaseDetailView[ModelType]
):
    """
    Django class-based detail view that renders as a PDF.

    For all intents and purposes, this class behaves like a normal DetailView. The only
    difference is that the response is rendered as a PDF.

    You can control whether it should attempt to download the PDF or display it inline
    with the `pdf_attachment` attribute. By default, the PDF is downloaded.

    The name of the PDF file can be controlled with the `pdf_filename` attribute or by
    overriding the `get_pdf_filename` method.
    """
