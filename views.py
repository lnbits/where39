from http import HTTPStatus

from fastapi import Depends, Request
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException
from starlette.responses import HTMLResponse

from lnbits.core.models import User
from lnbits.decorators import check_user_exists
from lnbits.settings import settings

from . import where39_ext, where39_renderer
from .crud import get_where39

myex = Jinja2Templates(directory="myex")


#######################################
##### ADD YOUR PAGE ENDPOINTS HERE ####
#######################################


# Backend admin page


@where39_ext.get("/", response_class=HTMLResponse)
async def index(request: Request, user: User = Depends(check_user_exists)):
    return where39_renderer().TemplateResponse(
        "where39/index.html", {"request": request, "user": user.dict()}
    )


# Frontend shareable page


@where39_ext.get("/{where39_id}")
async def where39(request: Request, where39_id):
    where39 = await get_where39(where39_id, request)
    if not where39:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Where39 does not exist."
        )
    return where39_renderer().TemplateResponse(
        "where39/where39.html",
        {
            "request": request,
            "where39_id": where39_id,
            "lnurlpay": where39.lnurlpay,
            "web_manifest": f"/where39/manifest/{where39_id}.webmanifest",
        },
    )


# Manifest for public page, customise or remove manifest completely


@where39_ext.get("/manifest/{where39_id}.webmanifest")
async def manifest(where39_id: str):
    where39 = await get_where39(where39_id)
    if not where39:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Where39 does not exist."
        )

    return {
        "short_name": settings.lnbits_site_title,
        "name": where39.name + " - " + settings.lnbits_site_title,
        "icons": [
            {
                "src": settings.lnbits_custom_logo
                if settings.lnbits_custom_logo
                else "https://cdn.jsdelivr.net/gh/lnbits/lnbits@0.3.0/docs/logos/lnbits.png",
                "type": "image/png",
                "sizes": "900x900",
            }
        ],
        "start_url": "/where39/" + where39_id,
        "background_color": "#1F2234",
        "description": "Minimal extension to build on",
        "display": "standalone",
        "scope": "/where39/" + where39_id,
        "theme_color": "#1F2234",
        "shortcuts": [
            {
                "name": where39.name + " - " + settings.lnbits_site_title,
                "short_name": where39.name,
                "description": where39.name + " - " + settings.lnbits_site_title,
                "url": "/where39/" + where39_id,
            }
        ],
    }
