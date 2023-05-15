import json
from os import environ
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/plugins", summary="Get a list of plugin manifests")
async def plugins():
    fields = ["manifest", "categories"]
    filename = environ["PLUGIN_FILE"]
    with open(filename) as f:
        plugins = json.loads(f.read())
        return [dict([(k, item[k]) for k in fields]) for item in plugins["items"]]
