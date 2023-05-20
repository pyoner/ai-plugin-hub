import os
import hashlib
import base64
import pydantic
import lancedb
from typing import Optional
from sentence_transformers import SentenceTransformer

from .types import Manifest, OpenAIPlugin

PLUGINS_TABLE_NAME = "plugins"

model_name = "paraphrase-albert-small-v2"
model = SentenceTransformer(model_name)


# used for both training and querying
def embed_func(batch):
    return [model.encode(sentence) for sentence in batch]


def create_manifest_url(domain: str):
    return "https://{domain}/.well-known/ai-plugin.json".format(domain=domain)


def load_openai_plugins(filename: Optional[str] = None) -> list[OpenAIPlugin]:
    filename = filename or os.environ["PLUGIN_FILE"]
    return pydantic.parse_file_as(list[OpenAIPlugin], filename)


def load_manifests(filename: Optional[str] = None) -> list[Manifest]:
    return [p.manifest for p in load_openai_plugins(filename)]


def db_connect(uri: Optional[str] = None) -> lancedb.LanceDBConnection:
    uri = uri or os.environ["LANCE_DB"]
    return lancedb.connect(uri)


def search(query: str):
    db = db_connect()
    t = db.open_table(PLUGINS_TABLE_NAME)

    query_vec = embed_func([query])[0]
    return t.search(query_vec)


def generate_unique_id(s: str, digest_size=64):
    sig = hashlib.blake2b(s.encode(), digest_size=digest_size).digest()
    return base64.urlsafe_b64encode(sig).decode("ascii").rstrip("=")
