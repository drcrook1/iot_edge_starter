# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

# Check out this repo: https://social.technet.microsoft.com/wiki/contents/articles/53668.python-azure-iot-sdk-how-to-receive-direct-methods-from-iot-hub.aspx

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