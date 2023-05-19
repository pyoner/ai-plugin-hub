import os
import shutil
import pandas as pd

from pathlib import Path
from lancedb.embeddings import with_embeddings
from dotenv import load_dotenv


from .helpers import db_connect, embed_func, load_plugins, search, PLUGINS_TABLE_NAME

load_dotenv()


def prepare():
    db_path = Path(os.environ["LANCE_DB"])
    if db_path.exists():
        shutil.rmtree(db_path)

    plugins = load_plugins()
    df = pd.DataFrame(data=[dict(text=p.text, **p.dict()) for p in plugins])
    df = with_embeddings(
        embed_func,
        df,
        column="text",
        show_progress=True,
    )

    db = db_connect()

    # The output is used to create / append to a table
    return db.create_table(PLUGINS_TABLE_NAME, data=df)


def find():
    query = "Find plugins to work with documents, pdf, sheets"
    df = search(query).limit(10).to_df()
    print(df)
