from urllib.parse import urljoin
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .helpers import load_plugins, to_about, search
from .types import AboutPlugin, Api, Manifest, ManifestNoAuth, Plugin


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


@app.get("/api/plugin/{id}", summary="Get a plugin")
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


@app.get("/.well-known/ai-plugin.json")
async def ai_plugin(request: Request) -> Manifest:
    base_url = str(request.base_url)
    return Manifest(
        schema_version="v1",
        name_for_human="Plugin Hub AI",
        name_for_model="PluginHunAI",
        description_for_human="A hub for exploring, installing a variety of ChatGPT AI plugins.",
        description_for_model="A hub for exploring, installing a variety of ChatGPT AI plugins.",
        auth=ManifestNoAuth(type="none", instructions=None),
        api=Api(
            type="openapi",
            url=urljoin(base_url, "/openapi.json"),
            is_user_authenticated=False,
        ),
        logo_url=urljoin(base_url, "/images/logo.png"),
        contact_email="devex.soft@gmail.com",
        legal_info_url=urljoin(base_url, "/legal.html"),
    )


# mount root at the end of code
app.mount("/", StaticFiles(directory="static"), name="static")
