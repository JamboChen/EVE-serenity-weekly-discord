from discord import Webhook
from dotenv import load_dotenv
import aiohttp

import os

load_dotenv()


async def send(text: str):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(os.getenv("Webhook"), session=session)
        await webhook.send(text)
