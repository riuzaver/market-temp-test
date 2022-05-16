import uvicorn as uvicorn
from fastapi import FastAPI
from alchql.app import SessionQLApp
from alchql.middlewares import DebugMiddleware, LoaderMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from api.root import root_router
from config import log, sentry_sdk, settings  # noqa: F401
from db import persistent_engine
from gql.schema import schema
import models as m

docs_conf = {}
if settings.ENABLE_DOCS:
    docs_conf["docs_url"] = "/docs"
    docs_conf["redoc_url"] = "/redoc"
    docs_conf["openapi_url"] = "/openapi.json"


app = FastAPI(
    version="{{cookiecutter.version}}",
    title="{{cookiecutter.project_name}}",
    description="{{cookiecutter.description}}",
    **docs_conf,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SentryAsgiMiddleware)


app.add_route(
    "/graphql",
    SessionQLApp(
        schema=schema,
        middleware=[
            LoaderMiddleware(m.Model.registry.mappers),
            DebugMiddleware(log),
        ],
        engine=persistent_engine,
        on_get=lambda request: RedirectResponse(
            url=f"https://sandbox.apollo.dev/?endpoint={request.url}"
        ),
    ),
)
app.include_router(root_router)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False,
        log_config=None,
    )
