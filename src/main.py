from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .helpers import load_plugins, to_about
from .types import AboutPlugin


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

app.mount("/", StaticFiles(directory="static"), name="static")


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
