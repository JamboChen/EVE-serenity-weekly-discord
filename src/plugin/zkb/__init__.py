from register import register_plugin

# from session import session
import asyncio
import aiohttp
from . import groups
from logger import get_logger
from utils.tools import send


log = get_logger(__name__)
attention = []


def add_attention(func):
    attention.append(func)


@register_plugin
async def listen():
    url = "wss://zkillboard.com/websocket/"
    data = {"action": "sub", "channel": "killstream"}
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.ws_connect(url, receive_timeout=10 * 60) as ws:
                    await ws.send_json(data)
                    log.info("Connected to zkillboard")
                    async for msg in ws:
                        msg = msg.json()
                        log.debug(msg["killmail_id"])
                        await asyncio.gather(*[func(msg) for func in attention])
            except aiohttp.ServerTimeoutError:
                log.error("Server timeout")


@add_attention
async def super_and_10b(killmail: dict):
    ship_type_id = killmail["victim"]["ship_type_id"]

    if not (
        ship_type_id in groups.Supercarrier | groups.Titan
        or killmail["zkb"]["totalValue"] > 10e10
    ):
        return

    system_id = killmail["solar_system_id"]
    hour = killmail["killmail_time"][:13].replace("T", "").replace("-", "")

    zkb = killmail["zkb"]["url"]
    br = f"https://br.evetools.org/related/{system_id}/{hour}00"
    log.info(f"{zkb}\n{br}\n\n")
    await send(f"{zkb}\n{br}\n\n")
