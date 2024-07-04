from fastapi import Depends, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from lnbits.core.models import User
from lnbits.decorators import check_user_exists
from lnbits.settings import settings

from . import where39_ext, where39_renderer

myex = Jinja2Templates(directory="myex")

@where39_ext.get("/", response_class=HTMLResponse)
async def index(request: Request, user: User = Depends(check_user_exists)):
    return where39_renderer().TemplateResponse(
        "where39/index.html", {"request": request, "user": user.dict()}
    )

# Public page

@where39_ext.get("/shared")
async def where39(request: Request):
    return where39_renderer().TemplateResponse(
        "where39/where39.html",
        {
            "request": request,
            "web_manifest": f"/where39/manifest/shared.webmanifest",
        },
    )

@where39_ext.get("/manifest/shared.webmanifest")
async def manifest():
    return {
        "short_name": settings.lnbits_site_title,
        "name": "Where39 - " + settings.lnbits_site_title,
        "icons": [
            {
                "src": settings.lnbits_custom_logo
                if settings.lnbits_custom_logo
                else "https://cdn.jsdelivr.net/gh/lnbits/lnbits@0.3.0/docs/logos/lnbits.png",
                "type": "image/png",
                "sizes": "900x900",
            }
        ],
        "start_url": "/eightball/shared",
        "background_color": "#1F2234",
        "description": "For dead drops and treasure hunts.",
        "display": "standalone",
        "scope": "/eightball/shared",
        "theme_color": "#1F2234",
        "shortcuts": [
            {
                "name": "Where39 - " + settings.lnbits_site_title,
                "short_name": "Where39",
                "description": "Where39 - " + settings.lnbits_site_title,
                "url": "/eightball/shared",
            }
        ],
    }
