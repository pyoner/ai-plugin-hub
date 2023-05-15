import json
from os import environ
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import parse_raw_as

from .types import Manifest, Plugin


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
    with open("./ai-plugin.json") as f:
        return parse_raw_as(Manifest, f.read())


@app.get("/plugins", summary="Get a list of plugin manifests")
async def plugins() -> list[Plugin]:
    filename: str = environ["PLUGIN_FILE"]
    with open(filename) as f:
        plugins = json.loads(f.read())

        return [
            Plugin(manifest=item["manifest"], categories=item["categories"])
            for item in plugins["items"]
        ]
