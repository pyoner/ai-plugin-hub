import json
from os import environ
from dotenv import load_dotenv
from fastapi import FastAPI

from .types import Plugin

load_dotenv()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/plugins", summary="Get a list of plugin manifests")
async def plugins() -> list[Plugin]:
    filename: str = environ["PLUGIN_FILE"]
    with open(filename) as f:
        plugins = json.loads(f.read())

        return [
            Plugin(manifest=item["manifest"], categories=item["categories"])
            for item in plugins["items"]
        ]
