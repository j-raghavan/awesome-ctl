import os

import sass
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger
from starlette.responses import HTMLResponse

app = FastAPI()
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

template_dir = os.path.join(os.path.dirname(__file__), "templates")
templatest = Jinja2Templates(directory=template_dir)


@app.on_event("startup")
async def lifecycle():
    logger.info("Starting up")
    file_name = os.path.join(os.path.dirname(__file__), "scss", "style.scss")
    logger.info(f"Compiling {file_name}")
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "scss")):
        logger.error("Style Files missing, please ensure you have the correct file")
        return

    in_dir = os.path.join(os.path.dirname(__file__), "scss")
    out_dir = os.path.join(os.path.dirname(__file__), "static", "css")

    for filename in os.listdir(in_dir):
        if filename.endswith(".scss"):
            input_file = os.path.join(in_dir, filename)
            output_file = os.path.join(out_dir, filename.replace(".scss", ".css"))
            with open(input_file, "r") as f:
                scss = f.read()
                css = sass.compile(string=scss)
            with open(output_file, "w") as out:
                out.write(css)
            logger.info(f"Compiled {filename} to {output_file}")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templatest.TemplateResponse("base.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templatest.TemplateResponse(
        "shared/_stub_dashboard.html", {"request": request}
    )
