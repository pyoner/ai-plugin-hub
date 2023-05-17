import os
import pydantic
import lancedb
from typing import Optional

from .types import AboutPlugin, Plugin


# used for both training and querying
def embed_func(batch):
    # from sentence_transformers import SentenceTransformer

    # name = "paraphrase-albert-small-v2"
    # model = SentenceTransformer(name)
    # return [model.encode(sentence) for sentence in batch]
    raise NotImplementedError


def create_manifest_url(domain: str):
    return "https://{domain}/.well-known/ai-plugin.json".format(domain=domain)


def load_plugins(filename: Optional[str] = None) -> list[Plugin]:
    filename = filename or os.environ["PLUGIN_FILE"]
    return pydantic.parse_file_as(list[Plugin], filename)


def db_connect(uri: Optional[str] = None) -> lancedb.LanceDBConnection:
    uri = uri or os.environ["LANCE_DB"]
    return lancedb.connect(uri)


def to_about(id: int, p: Plugin) -> AboutPlugin:
    return AboutPlugin(
        id=id,
        name=p.manifest.name_for_human,
        description=p.manifest.description_for_human,
    )
