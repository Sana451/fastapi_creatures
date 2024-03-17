from typing import Generator
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from web import explorer, creature, user, game

app = FastAPI()
app.include_router(router=explorer.router)
app.include_router(router=creature.router)
app.include_router(router=user.router)
app.include_router(router=game.router)


@app.post("/small-file")
async def upload_small_file(small_file: bytes = File()) -> str:
    return f"file size: {len(small_file)}"


@app.post("/big-file")
async def upload_big_file(big_file: UploadFile) -> str:
    return f"file size: {big_file.size}, name: {big_file.filename}"


@app.get("/small/{name}")
async def download_small_file(name):
    return FileResponse(name)


def gen_file(path: str) -> Generator:
    with open(file=path, mode="rb") as file:
        yield file.readline()


@app.get("/download_big/{name}")
async def download_big_file(name: str):
    response = StreamingResponse(
        content=gen_file(path=Path(name)),
        status_code=200,
    )
    return response


# Directory containing main.py:
top = Path(__file__).resolve().parent

app.mount(path="/static",
          app=StaticFiles(directory=f"{top}/static", html=True),
          name="free"
          )


@app.get("/who")
def greet(name: str = Form()):
    return f"Hello, {name}"


@app.post("/who2")
def greet2(name: str = Form()):
    return f"Hello, {name}"


template_obj = Jinja2Templates(directory=f"{top}/template")
from fake.creature import fakes as fake_creatures
from fake.explorer import fakes as fake_explorers


@app.get("/list")
def explorer_list(request: Request):
    return template_obj.TemplateResponse("list.html",
                                         {"request": request,
                                          "explorers": fake_explorers,
                                          "creatures": fake_creatures})


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app",
                host="localhost", port="8000", reload=True)
