import asyncio
from typing import Annotated

from fastapi import APIRouter, Form, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from telegram.error import RetryAfter

from src.configs.runtime_config import RuntimeConfig
from src.logic.logic import FotoLogic

router = APIRouter()
logic = FotoLogic()
background_tasks = set()


@router.post("/uploadfiles/")
async def create_upload_files(
    files: list[UploadFile],
    token: Annotated[str, Form()] | None = Form(default=None),
    channel_id: Annotated[str, Form()] | None = Form(default=None),
):
    channel_id = RuntimeConfig().CHANNEL_ID if channel_id is None else channel_id
    token = RuntimeConfig().BOT_TOKEN if token is None else token

    for file in files:
        try:
            await logic.send_photo(
                token=token,
                chat_id=channel_id,
                file=file,
            )
        except RetryAfter as e:
            await asyncio.sleep(e.retry_after)

    return RedirectResponse(url=f"/?count={len(files)}", status_code=303)


@router.get("/")
async def main():
    with open("index.html") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)


@router.on_event('startup')
async def startup():
    task = asyncio.create_task(logic.get_queue_worker())
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)
