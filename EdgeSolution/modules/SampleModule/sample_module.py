"""
@Author: David Crook
@Copyright: Microsoft Corporation 2022
"""
from enum import Enum
import logging
import asyncio

from azure.iot.device.aio import IoTHubModuleClient

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
        

    def _receive_twin_patch_handler(self, twin_patch):
        """
        Receive a twin patch update.
        """
        logging.info("Twin Patch received")
        print("I received a twin patch")

        # Did they update Temperature Threshold?
        if("SleepTime" in twin_patch):
            self.module_twin_properties.SleepTime = twin_patch["SleepTime"]
        self.module_client.patch_twin_reported_properties(self.Sample_Twin_Properties.to_dict())
