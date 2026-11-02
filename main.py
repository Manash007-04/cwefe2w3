import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from webapp.config import APP_NAME, APP_TAGLINE, STATIC_DIR
from webapp.routers import about, diagnose, guide, home
from webapp.templating import templates


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title=APP_NAME,
    description=APP_TAGLINE,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.include_router(home.router)
app.include_router(diagnose.router)
app.include_router(guide.router)
app.include_router(about.router)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "img-src 'self' data:; "
        "style-src 'self'; "
        "script-src 'self'; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "frame-ancestors 'none'"
    )
    return response


@app.get("/health", include_in_schema=False)
def health():
    return JSONResponse({"status": "ok", "app": APP_NAME})


@app.exception_handler(StarletteHTTPException)
async def http_error(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "active": "",
                "page_title": "Page not found · Leafwise",
                "page_description": "The requested page was not found.",
                "status_code": 404,
                "title": "Page not found",
                "message": "That page does not exist. Start from the home page or run a leaf diagnosis.",
            },
            status_code=404,
        )
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={
            "active": "",
            "page_title": "Request failed · Leafwise",
            "page_description": "The request could not be completed.",
            "status_code": exc.status_code,
            "title": "Request failed",
            "message": "The request could not be completed. Go back and try again.",
        },
        status_code=exc.status_code,
    )


@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError):
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={
            "active": "",
            "page_title": "Check the form · Leafwise",
            "page_description": "Some form values were not accepted.",
            "status_code": 400,
            "title": "Check the form",
            "message": "Some values were not accepted. Go back, check each field and try again.",
        },
        status_code=400,
    )


@app.exception_handler(Exception)
async def unhandled_error(request: Request, exc: Exception):
    logger.exception("Unhandled application error")
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={
            "active": "",
            "page_title": "Something went wrong · Leafwise",
            "page_description": "The application encountered an unexpected error.",
            "status_code": 500,
            "title": "Something went wrong",
            "message": "The page could not be completed. Try again, or return to the home page.",
        },
        status_code=500,
    )
