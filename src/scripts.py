import pandas as pd

from lancedb.embeddings import with_embeddings
from dotenv import load_dotenv


from .helpers import db_connect, embed_func, load_plugins

load_dotenv()


def prepare():
    plugins = load_plugins()
    df = pd.DataFrame(data=plugins)
    with_embeddings(embed_func, df)  # TODO add column

    db = db_connect()

    # The output is used to create / append to a table
    return db.create_table("plugins", data=df)
