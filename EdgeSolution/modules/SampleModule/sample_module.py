"""
@Author: David Crook
@Copyright: Microsoft Corporation 2022
"""
from enum import Enum
import logging
import asyncio

from azure.iot.device.aio import IoTHubModuleClient
from azure.iot.device import MethodResponse

# TODO: Module 2 Module Comms & Upstream Telemetry/Messages

class Sample_Twin_Properties():
    """
    Class encapsulating the Twin Properties for this module.
    """
    SleepTime : int = None

    def to_dict() -> dict:
        """
        returns a dictionary representation
        """
        result = {}
        for k,v in self.__dict__.items():
            result[k] = v
        return result

class Sample_Module():
    """
    Representation of the Module Object
    """
    module_client : IoTHubModuleClient = None
    module_twin_properties : Sample_Twin_Properties = None

    def initialize(self):
        """
        Initialize the stateful object of this module.
        """
        self.module_twin_properties = Sample_Twin_Properties()
        self.module_twin_properties.SleepTime = 25

        # Configure Client & Handlers
        self.module_client = IoTHubModuleClient.create_from_edge_environment()
        self.module_client.on_twin_desired_properties_patch_received = self._receive_twin_patch_handler
        self.module_client.on_method_request_received = self._hello_module_command

    async def _receive_twin_patch_handler(self, twin_patch):
        """
        Receive a twin patch update.
        """
        logging.info("Twin Patch received")
        print("I received a twin patch")

        # Did they update Temperature Threshold?
        if("SleepTime" in twin_patch):
            self.module_twin_properties.SleepTime = twin_patch["SleepTime"]
        self.module_client.patch_twin_reported_properties(self.module_twin_properties.to_dict())

    async def _hello_module_command(self, method_request):
        """
        Receive and handle a method request/command, note, 
        you must respond to the command for it to read as success, otherwise it will fail.
        """
        print("HELLO!!!!!")
        method_response = MethodResponse.create_from_method_request(method_request, 200, "HELLO!!!!")
        await self.module_client.send_method_response(method_response)