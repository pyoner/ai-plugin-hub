import os
import shutil
import pandas as pd

from lancedb.embeddings import with_embeddings
from dotenv import load_dotenv


from .helpers import db_connect, embed_func, load_manifests, search, PLUGINS_TABLE_NAME

load_dotenv()


def prepare():
    shutil.rmtree(os.environ["LANCE_DB"])

    manifests = load_manifests()
    df = pd.DataFrame(data=[m.dict() for m in manifests])
    df = with_embeddings(
        embed_func,
        df,
        column="description_for_human",
        show_progress=True,
    )

    db = db_connect()

    # The output is used to create / append to a table
    return db.create_table(PLUGINS_TABLE_NAME, data=df)


def find():
    query = "Find plugins to work with documents, pdf, sheets"
    df = search(query).limit(10).to_df()
    print(df)
