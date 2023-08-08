import asyncio
import importlib
import os

from register import registered_functions
from logger import configure_logging, get_logger
from dotenv import load_dotenv

load_dotenv()


log_level = os.getenv("LOG_LEVEL", "INFO")
configure_logging(log_level)
log = get_logger(__name__)
log.info(f"Log level: {log_level}")


def load_plugins():
    plugin_files = os.listdir(os.path.join(os.path.dirname(__file__), "plugin"))
    for plugin_file in plugin_files:
        if os.path.isdir(
            os.path.join(os.path.dirname(__file__), "plugin", plugin_file)
        ):
            importlib.import_module(f"plugin.{plugin_file}")
        elif plugin_file.endswith(".py"):
            module_name = plugin_file[:-3]
            importlib.import_module(f"plugin.{module_name}")

    log.debug(f"Registered plugins: {len(registered_functions)}")


async def run_plugins():
    tasks = [func() for func in registered_functions]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    log.info("Starting bot")
    load_plugins()
    asyncio.run(run_plugins())
