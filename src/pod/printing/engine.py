from __future__ import annotations

import json
import pathlib
import typing

import typst
from django.core.serializers.json import DjangoJSONEncoder
from django.http.request import HttpRequest
from django.template import Origin, TemplateDoesNotExist
from django.template.backends.base import BaseEngine

UNKNOWN_SOURCE = "<unknown source>"


class TypstEngine(BaseEngine):
    """
    A template engine for rendering Typst templates.
    """

    def __init__(self, params: dict[str, typing.Any]) -> None:
        params = params.copy()
        params.pop("OPTIONS", None)
        super().__init__(params)

    def from_string(self, template_code: str) -> TypstTemplate:  # type: ignore[override]
        return TypstTemplate(template_code.encode("utf-8"))

    def get_template(self, template_name: str) -> TypstTemplate:  # type: ignore[override]
        tried = []

        for template_path in self.iter_template_filenames(template_name):
            path = pathlib.Path(template_path)
            origin = Origin(
                name=path.as_posix(),
                template_name=template_name,
            )
            tried.append((origin, template_name))

            if path.exists() and path.is_file():
                template_code = path.read_bytes()
                return TypstTemplate(template_code, origin=origin)

        raise TemplateDoesNotExist(template_name, tried=tried, backend=self)


class TypstTemplate:
    """
    A Typst template that can be rendered.
    """

    def __init__(
        self,
        template_code: bytes,
        origin: Origin | None = None,
    ):
        self.source = template_code
        if origin is None:
            self.origin = Origin(UNKNOWN_SOURCE)
        else:
            self.origin = origin

    def render(
        self,
        context: dict[str, typing.Any] | None = None,
        request: HttpRequest | None = None,
    ) -> bytes:
        if context is None:
            context = {}

        # If I was making a more complex Typst template engine, I would probably want to
        # pass the request object to Typst so it can access request data like user,
        # session, etc. But that would require me making them JSON serializable, which I
        # cannot be bothered to do right now. Same with the "view" context variable.

        context.pop("view", None)  # views are not json serializable

        root = None
        font_paths = []
        if self.origin.name != UNKNOWN_SOURCE:
            # Use the directory of the template as the root for relative paths
            # again if this was a proper Typst template engine, I would probably
            # want to make these configurable via the settings.
            root = pathlib.Path(self.origin.name).parent.as_posix()
            font_paths = [root]

        encoded_context = json.dumps(context, cls=DjangoJSONEncoder)

        return typst.compile(
            input=self.source,  # type: ignore[misc]
            root=root,
            sys_inputs={"context": encoded_context},
            font_paths=font_paths,
        )
