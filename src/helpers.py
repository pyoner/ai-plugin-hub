import os
import pydantic
import lancedb
from typing import Optional
from sentence_transformers import SentenceTransformer

from .types import AboutPlugin, Manifest, Plugin

PLUGINS_TABLE_NAME = "plugins"

model_name = "paraphrase-albert-small-v2"
model = SentenceTransformer(model_name)


# used for both training and querying
def embed_func(batch):
    return [model.encode(sentence) for sentence in batch]


def create_manifest_url(domain: str):
    return "https://{domain}/.well-known/ai-plugin.json".format(domain=domain)


def load_plugins(filename: Optional[str] = None) -> list[Plugin]:
    filename = filename or os.environ["PLUGIN_FILE"]
    return pydantic.parse_file_as(list[Plugin], filename)


def load_manifests(filename: Optional[str] = None) -> list[Manifest]:
    return [p.manifest for p in load_plugins(filename)]


def db_connect(uri: Optional[str] = None) -> lancedb.LanceDBConnection:
    uri = uri or os.environ["LANCE_DB"]
    return lancedb.connect(uri)


def to_about(p: Plugin) -> AboutPlugin:
    return AboutPlugin(
        id=p.id,
        name=p.manifest.name_for_human,
        description=p.manifest.description_for_human,
    )


def search(query: str):
    db = db_connect()
    t = db.open_table(PLUGINS_TABLE_NAME)

    query_vec = embed_func([query])[0]
    return t.search(query_vec)
