from fastapi import APIRouter
from lnbits.db import Database

from .views import where39_generic_router

db = Database("ext_where39")

where39_ext: APIRouter = APIRouter(prefix="/where39", tags=["where39"])
where39_ext.include_router(where39_generic_router)

where39_static_files = [
    {
        "path": "/where39/static",
        "name": "where39_static",
    }
]

__all__ = ["db", "where39_ext", "where39_static_files"]
