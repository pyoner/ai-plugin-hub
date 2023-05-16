import pandas as pd

from lancedb.embeddings import with_embeddings
from dotenv import load_dotenv


from .helpers import db_connect, embed_func, load_plugins

load_dotenv()


def prepare():
    plugins = load_plugins()
    df = pd.DataFrame(plugins)
    with_embeddings(embed_func, df)

    db = db_connect()

    # The output is used to create / append to a table
    db.create_table("my_table", data=df)
