from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import parse_file_as

from .helpers import load_plugins, to_about

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


@app.get("/.well-known/ai-plugin.json", summary="Get a plugin manifest")
async def manifest():
    return parse_file_as(Manifest, "./ai-plugin.json")


@app.get("/plugins", summary="Get a list of plugins")
async def plugins() -> list[AboutPlugin]:
    plugins = load_plugins()
    return [to_about(i, p) for (i, p) in enumerate(plugins)]


@app.get("/plugin", summary="Get a plugin manifest")
async def plugin(index: int):
    plugins = load_plugins()
    return plugins[index]


# @app.get("/search", summary="Search plugins in the store")
# async def search(query: str) -> list[Plugin]:
#     raise NotImplementedError
