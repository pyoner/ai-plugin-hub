import json
from os import environ
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/plugins", summary="List of plugin manifest")
async def plugins():
    fields = ["manifest", "categories"]
    plugins = json.loads(environ["PLUGIN_FILE"])
    return [dict([(k, item[k]) for k in fields]) for item in plugins["items"]]
