from pydantic import BaseModel, AnyUrl, FutureDatetime
from typing import Optional, List, Mapping


class JSONResourceDefinitionLink(BaseModel):
    """
    Link element of a JSON Resource Definition (JRD)

    https://www.rfc-editor.org/rfc/rfc7033#section-4.4.4
    """

    rel: str
    type: Optional[str] = None
    href: Optional[AnyUrl] = None
    titles: Optional[Mapping[str, str]] = None
    properties: Optional[Mapping[str, str]] = None
    template: Optional[str] = None


class JSONResourceDefinition(BaseModel):
    """
    JSON Resource Definition (JRD)

    https://www.rfc-editor.org/rfc/rfc6415#appendix-A
    https://www.rfc-editor.org/rfc/rfc7033#section-4.4
    """

    subject: str
    expires: Optional[FutureDatetime] = None
    aliases: Optional[List[str]] = None
    properties: Optional[Mapping[str, str]] = None
    links: Optional[List[JSONResourceDefinitionLink]] = None
