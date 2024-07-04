import asyncio
from lnbits.db import Database
from fastapi import APIRouter
from lnbits.helpers import template_renderer
from loguru import logger

db = Database("ext_where39")

where39_ext: APIRouter = APIRouter(
    prefix="/where39", tags=["Where39"]
)

where39_static_files = [
    {
        "path": "/where39/static",
        "name": "where39_static",
    }
]
def where39_renderer():
    return template_renderer(["where39/templates"])
