import asyncio
import sys
import signal
import threading
from sample_module import Sample_Module

async def run_sample():
    module = Sample_Module()
    module.initialize()
    while(True):
        print("sleeping for {}".format(module.module_twin_properties.SleepTime))
        await asyncio.sleep(module.module_twin_properties.SleepTime)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_sample())