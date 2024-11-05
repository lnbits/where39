from fastapi import APIRouter, Depends, Request
from starlette.responses import HTMLResponse

from lnbits.core.models import User
from lnbits.decorators import check_user_exists
from lnbits.settings import settings
from lnbits.helpers import template_renderer

where39_generic_router: APIRouter = APIRouter()

def where39_renderer():
    return template_renderer(["where39/templates"])

@where39_generic_router.get("/", response_class=HTMLResponse)
async def index(request: Request, user: User = Depends(check_user_exists)):
    return where39_renderer().TemplateResponse(
        "where39/index.html", {"request": request, "user": user.dict()}
    )

# Public page

@where39_generic_router.get("/shared")
async def where39(request: Request):
    return where39_renderer().TemplateResponse(
        "where39/where39.html",
        {
            "request": request,
            "web_manifest": f"/where39/manifest/shared.webmanifest",
        },
    )

@where39_generic_router.get("/manifest/shared.webmanifest")
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
