import asyncio
import sys
import signal
import threading
from publisher_module import Publisher_Module

async def run_sample():
    module = Publisher_Module()
    module.initialize()
    while(True):
        await asyncio.sleep(module.module_twin_properties.PublishRate)
        await module._publish_telemetry()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_sample())