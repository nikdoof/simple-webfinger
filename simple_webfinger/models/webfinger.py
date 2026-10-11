from collections.abc import Mapping

from pydantic import AnyUrl, BaseModel, FutureDatetime


class JSONResourceDefinitionLink(BaseModel):
    """
    Link element of a JSON Resource Definition (JRD)

    https://www.rfc-editor.org/rfc/rfc7033#section-4.4.4
    """

    rel: str
    type: str | None = None
    href: AnyUrl | None = None
    titles: Mapping[str, str] | None = None
    properties: Mapping[str, str] | None = None
    template: str | None = None


class JSONResourceDefinition(BaseModel):
    """
    JSON Resource Definition (JRD)

    https://www.rfc-editor.org/rfc/rfc6415#appendix-A
    https://www.rfc-editor.org/rfc/rfc7033#section-4.4
    """

    subject: str
    expires: FutureDatetime | None = None
    aliases: list[str] | None = None
    properties: Mapping[str, str] | None = None
    links: list[JSONResourceDefinitionLink] | None = None
