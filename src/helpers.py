import os
import pydantic
import lancedb
from sentence_transformers import SentenceTransformer

from .types import Plugin

name = "paraphrase-albert-small-v2"
model = SentenceTransformer(name)


# used for both training and querying
def embed_func(batch):
    return [model.encode(sentence) for sentence in batch]


def create_manifest_url(domain: str):
    return "https://{domain}/.well-known/ai-plugin.json".format(domain=domain)


def load_plugins(filename=os.environ["PLUGIN_FILE"]) -> list[Plugin]:
    return pydantic.parse_file_as(list[Plugin], filename)


def db_connect(uri=os.environ["LANCE_DB"]) -> lancedb.LanceDBConnection:
    return lancedb.connect(uri)
