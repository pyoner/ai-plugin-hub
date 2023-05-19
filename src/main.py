from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import parse_obj_as

from .helpers import load_plugins, to_about, search
from .types import AboutPlugin, Manifest


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
    return [to_about(i, p) for (i, p) in enumerate(plugins)]


@app.get("/api/manifest", summary="Get a plugin manifest")
async def api_manifest(index: int) -> Manifest:
    plugins = load_plugins()
    return plugins[index].manifest


@app.get("/api/search", summary="Search plugins in the hub")
async def api_search(query: str):
    df = search(query).limit(10).to_df()
    d = df.to_dict(orient="records")
    # return d
    return parse_obj_as(list[Manifest], d)


# mount root at the end of code
app.mount("/", StaticFiles(directory="static"), name="static")
