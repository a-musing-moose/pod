import typing

from django import http
from django.core import exceptions
from django.template import base as template_base
from django.template import response
from django.views.generic import base

from . import generation


class PDFTemplateResponse(response.TemplateResponse):
    def __init__(
        self,
        request: http.HttpRequest,
        template: list[str] | template_base.Template | str,
        context: dict[str, object] | None = None,
        content_type: str | None = None,
        status: int | None = None,
        charset: None = None,
        using: str | None = None,
        filename: str | None = None,
        attachment: bool = True,
    ) -> None:
        super().__init__(
            request=request,
            template=template,
            context=context,
            content_type=content_type or "application/pdf",
            status=status,
            charset=charset,
            using=using,
        )
        self.filename = filename

        if filename:
            display = "attachment" if attachment else "inline"
            self.headers["Content-Disposition"] = f'{display};filename="{filename}"'

    @property
    def rendered_content(self) -> bytes:  # type: ignore[override]
        """
        Returns rendered PDF pages.
        """
        template = self.resolve_template(self.template_name)
        context = self.resolve_context(self.context_data)
        generator = generation.WeasyPrintPDFGenerator(
            template=template,
            context=context,
        )
        return generator.get_pdf()


class PDFTemplateResponseMixin(base.TemplateResponseMixin):
    response_class = PDFTemplateResponse
    content_type = "application/pdf"
    pdf_attachment = True
    pdf_filename: str

    def get_pdf_filename(self) -> str:
        """
        Resolve the PDF filename to use
        """
        if getattr(self, "pdf_filename", None) is None:
            raise exceptions.ImproperlyConfigured(
                "Document requires either a definition of 'pdf_filename' or an "
                "implementation of 'get_pdf_filename()' method"
            )
        return self.pdf_filename

    def render_to_response(
        self, context: dict[str, typing.Any], **response_kwargs: typing.Any
    ) -> http.HttpResponse:
        """
        Render the template and return a PDFTemplateResponse.
        """
        response_kwargs.update(
            {
                "attachment": self.pdf_attachment,
                "filename": self.get_pdf_filename(),
            }
        )
        return super().render_to_response(context, **response_kwargs)
