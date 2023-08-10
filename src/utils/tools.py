from discord import Webhook
import aiohttp


async def send(text: str, webhook: str):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(webhook, session=session)
        await webhook.send(text)
