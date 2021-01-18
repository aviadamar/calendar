from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routers import event
from dependencies import STATIC_PATH, TEMPLATES_PATH

app = FastAPI()

templates = Jinja2Templates(directory=TEMPLATES_PATH)
app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {
        "request": request,
        "message": "Hello, World!"
    })


@app.get("/profile")
def profile(request: Request):
    # Get relevant data from database
    upcouming_events = range(5)
    current_username = "Chuck Norris"

    return templates.TemplateResponse("profile.html", {
        "request": request,
        "username": current_username,
        "events": upcouming_events
    })


app.include_router(event.router)
