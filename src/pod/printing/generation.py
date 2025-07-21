import pathlib
import typing

import weasyprint
from django.template import base as template_base
from django.template import context as template_context
from django.template import loader
from weasyprint.text import fonts


class WeasyPrintPDFGenerator:
    def __init__(
        self,
        template: template_base.Template,
        context: dict[str, object] | None = None,
    ) -> None:
        self.template = template
        self.context = context or {}

    def get_base_url(self) -> pathlib.Path:
        """
        Determine the base URL to use for the template.

        The base URL is the file system path to the folder containing the template. All
        URLs in the CSS/template are resolved relative to this path.
        """
        return pathlib.Path(self.template.origin.name).parent

    def get_font_config(self) -> fonts.FontConfiguration:
        return fonts.FontConfiguration()

    def get_document(self) -> weasyprint.Document:
        """
        Render the template and return a WeasyPrint Document object.
        """

        base_url = self.get_base_url()
        font_config = self.get_font_config()
        template_name = (
            self.template.name
            if isinstance(self.template, template_base.Template)
            else self.template
        )
        if not template_name:
            raise ValueError("The provided template is missing a name.")

        html = weasyprint.HTML(
            string=self.template.render(template_context.Context(self.context)),
            base_url=base_url,
        )
        return html.render(font_config=font_config)

    def get_pdf(self) -> bytes:
        """
        Returns rendered PDF pages.
        """
        document = self.get_document()
        return typing.cast(bytes, document.write_pdf())

    def resolve_template(
        self,
        template: list[str] | tuple[str, ...] | template_base.Template | str,
    ) -> template_base.Template:
        """Resolve and return the template."""
        if isinstance(template, template_base.Template):
            return template
        elif isinstance(template, (list, tuple)):
            # Use the first valid template found from the list / tuple
            return typing.cast(
                template_base.Template, loader.select_template(list(template))
            )
        elif isinstance(template, str):
            return typing.cast(template_base.Template, loader.get_template(template))
        raise ValueError("Invalid template type provided")
