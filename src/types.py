from typing import Dict, Literal
from pydantic import BaseModel, Field


HttpAuthorizationType = Literal["bearer", "basic"]


ManifestAuthType = Literal["none", "service_http", "user_http", "oauth"]


class BaseManifestAuth(BaseModel):
    type: ManifestAuthType
    instructions: str | None


class ManifestNoAuth(BaseManifestAuth):
    type: ManifestAuthType = Field("none", const=True)


class ManifestServiceHttpAuth(BaseManifestAuth):
    type: ManifestAuthType = Field("service_http", const=True)
    authorization_type: HttpAuthorizationType
    verification_tokens: Dict[str, str | None]


class ManifestUserHttpAuth(BaseManifestAuth):
    type: ManifestAuthType = Field("user_http", const=True)
    authorization_type: HttpAuthorizationType


class ManifestOAuthAuth(BaseManifestAuth):
    type: ManifestAuthType = Field("oauth", const=True)
    client_url: str
    scope: str
    authorization_url: str
    authorization_content_type: str
    verification_tokens: Dict[str, str | None]


ManifestAuth = (
    ManifestNoAuth | ManifestServiceHttpAuth | ManifestUserHttpAuth | ManifestOAuthAuth
)


class Api(BaseModel):
    type: str = Field("openapi", const=True)
    url: str
    is_user_authenticated: bool | None


class Manifest(BaseModel):
    schema_version: str
    name_for_human: str
    name_for_model: str
    description_for_human: str
    description_for_model: str
    auth: ManifestAuth
    api: Api
    logo_url: str
    contact_email: str
    legal_info_url: str


class Categories(BaseModel):
    id: str | None
    title: str | None


class OpenAIPlugin(BaseModel):
    id: str
    domain: str
    manifest: Manifest
    categories: Categories

    def to_plugin(self) -> "Plugin":
        from .helpers import generate_unique_id

        m = self.manifest
        return Plugin(
            id=generate_unique_id(self.domain, digest_size=16),
            url="https://{}".format(self.domain),
            name=m.name_for_human,
            description=m.description_for_human,
            logo_url=m.logo_url,
            contact_email=m.contact_email,
            legal_info_url=m.legal_info_url,
        )


class Plugin(BaseModel):
    id: str
    url: str
    name: str
    description: str
    logo_url: str
    contact_email: str
    legal_info_url: str

    @property
    def text(self) -> str:
        return "{0.name} {0.description}".format(self)
