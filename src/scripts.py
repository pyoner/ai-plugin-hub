import pandas as pd

from lancedb.embeddings import with_embeddings
from dotenv import load_dotenv


from .helpers import db_connect, embed_func, load_manifests

load_dotenv()


def prepare():
    manifests = load_manifests()
    df = pd.DataFrame(data=manifests)
    with_embeddings(embed_func, df, column="description_for_human")

    db = db_connect()

    # The output is used to create / append to a table
    return db.create_table("plugins", data=df)
