from fastapi import FastAPI, Request
from aiogram import Dispatcher
from bot import bot, dp
from config import WEBHOOK_URL
import asyncio

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)

@app.post("/webhook")
async def webhook(request: Request):
    update = await bot.parse_update(await request.json())
    await dp._process_update(update)
    return {"ok": True}
