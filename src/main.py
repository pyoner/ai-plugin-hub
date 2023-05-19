from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .helpers import load_plugins, to_about, search
from .types import AboutPlugin, Plugin


load_dotenv()
app = FastAPI()


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/plugins", summary="Get a list of plugins")
async def api_plugins() -> list[AboutPlugin]:
    plugins = load_plugins()
    return [to_about(p) for p in plugins]


@app.get("/api/plugin", summary="Get a plugin")
async def api_plugin(id: str) -> Plugin:
    for p in load_plugins():
        if p.id == id:
            return p
    raise HTTPException(404, detail="Plugin not found")


@app.get("/api/search", summary="Search plugins in the hub")
async def api_search(query: str) -> list[AboutPlugin]:
    df = search(query).limit(10).to_df()
    items = []
    for _, row in df.iterrows():
        m = row["manifest"]
        items.append(
            AboutPlugin(
                id=row["id"],
                name=m["name_for_human"],
                description=m["description_for_human"],
            )
        )
    return items


# mount root at the end of code
app.mount("/", StaticFiles(directory="static"), name="static")
