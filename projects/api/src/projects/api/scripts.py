import os
import pandas as pd

from sentence_transformers import SentenceTransformer
from lancedb.embeddings import with_embeddings
from dotenv import load_dotenv

from libs.shared.helpers import (
    db_connect,
    embed_func,
    load_openai_plugins,
    search,
    PLUGINS_TABLE_NAME,
)

load_dotenv()


def download():
    model_name = os.environ["EMBEDDING_MODEL_NAME"]
    SentenceTransformer(model_name)


def prepare():
    openai_plugins = load_openai_plugins()
    df = pd.DataFrame(
        data=[dict(p.to_plugin(), text=p.to_plugin().text) for p in openai_plugins]
    )
    df = with_embeddings(
        embed_func,
        df,
        column="text",
        show_progress=True,
    )

    db = db_connect()

    # The output is used to create / append to a table
    return db.create_table(PLUGINS_TABLE_NAME, data=df, mode="overwrite")


def find():
    query = "Find plugins to work with documents, pdf, sheets"
    df = search(query).limit(10).to_df()
    print(df)
