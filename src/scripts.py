import pandas as pd

from lancedb.embeddings import with_embeddings
from dotenv import load_dotenv


from .helpers import db_connect, embed_func, load_manifests

load_dotenv()


def prepare():
    manifests = load_manifests()
    df = pd.DataFrame(data=[m.dict() for m in manifests])
    df = with_embeddings(
        embed_func,
        df[["name_for_human", "description_for_human"]],
        column="description_for_human",
        show_progress=True,
    )

    db = db_connect()

    # The output is used to create / append to a table
    return db.create_table("plugins", data=df)


def search():
    db = db_connect()
    t = db.open_table("plugins")

    query = "Find plugins to work with documents, pdf, sheets"
    query_vec = embed_func([query])[0]
    df = t.search(query_vec).limit(10).to_df()
    print(df)
