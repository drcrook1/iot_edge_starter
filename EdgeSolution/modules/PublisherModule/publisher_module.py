"""
@Author: David Crook
@Copyright: Microsoft Corporation 2022
"""
from enum import Enum
import logging
import asyncio
import random
import uuid

from azure.iot.device.aio import IoTHubModuleClient
from azure.iot.device import MethodResponse
from azure.iot.device import Message

# TODO: Module 2 Module Comms & Upstream Telemetry/Messages

class Sample_Twin_Properties():
    """
    Class encapsulating the Twin Properties for this module.
    """
    PublishRate : int = None

    def to_dict(self) -> dict:
        """
        returns a dictionary representation
        """
        result = {}
        for k,v in self.__dict__.items():
            result[k] = v
        return result

class Publisher_Module():
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
        self.module_twin_properties.PublishRate = 25

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
        if("PublishRate" in twin_patch):
            self.module_twin_properties.PublishRate = twin_patch["PublishRate"]
        await self.module_client.patch_twin_reported_properties({"PublishRate" : self.module_twin_properties.PublishRate})

    async def _hello_module_command(self, method_request):
        """
        Receive and handle a method request/command, note, 
        you must respond to the command for it to read as success, otherwise it will fail.
        """
        print("HELLO!!!!!")
        method_response = MethodResponse.create_from_method_request(method_request, 200, "HELLO!!!!")
        await self.module_client.send_method_response(method_response)

    async def _publish_telemetry(self):
        """
        Publishes messages over a route to iot edge hub.
        """
        wind_speed = str(random.randint(0, 50))
        msg = Message("'windspeed' : {}".format(wind_speed))
        msg_id = uuid.uuid4()
        msg.message_id = msg_id
        msg.correlation_id = str(msg_id)
        msg.custom_properties["sample-property"] = "sample"
        await self.module_client.send_message_to_output(msg, "PublisherToSample")
        print("sent message with windspeed: {}".format(wind_speed))