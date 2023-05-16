from typing import Optional, Dict, Union
from pydantic import BaseModel, Field
from enum import Enum


class HttpAuthorizationType(str, Enum):
    BEARER = "bearer"
    BASIC = "basic"


class ManifestAuthType(str, Enum):
    NONE = "none"
    SERVICE_HTTP = "service_http"
    USER_HTTP = "user_http"
    OAUTH = "oauth"


class BaseManifestAuth(BaseModel):
    type: ManifestAuthType
    instructions: Optional[str] = None


class ManifestNoAuth(BaseManifestAuth):
    type: ManifestAuthType = Field("none", const=True)


class ManifestServiceHttpAuth(BaseManifestAuth):
    type: ManifestAuthType = Field("service_http", const=True)
    authorization_type: HttpAuthorizationType
    verification_tokens: Dict[str, Optional[str]]


class ManifestUserHttpAuth(BaseManifestAuth):
    type: ManifestAuthType = Field("user_http", const=True)
    authorization_type: HttpAuthorizationType


class ManifestOAuthAuth(BaseManifestAuth):
    type: ManifestAuthType = Field("oauth", const=True)
    client_url: str
    scope: str
    authorization_url: str
    authorization_content_type: str
    verification_tokens: Dict[str, Optional[str]]


ManifestAuth = Union[
    ManifestNoAuth,
    ManifestServiceHttpAuth,
    ManifestUserHttpAuth,
    ManifestOAuthAuth,
]


class Api(BaseModel):
    type: str = Field("openapi", const=True)
    url: str
    is_user_authenticated: Optional[bool]


class Manifest(BaseModel):
    schema_version: str
    name_for_human: str
    name_for_model: str
    description_for_human: str
    description_for_model: str
    auth: Union[
        ManifestNoAuth,
        ManifestServiceHttpAuth,
        ManifestUserHttpAuth,
        ManifestOAuthAuth,
    ]
    api: Api
    logo_url: str
    contact_email: str
    legal_info_url: str


class Categories(BaseModel):
    id: Optional[str]
    title: Optional[str]


class Plugin(BaseModel):
    manifest: Manifest
    categories: Categories
