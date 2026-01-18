"""
PulseClient module. ???

Main worker for PulseEngine.
Handles websocket communication. Executes actions based off the handlers that were passed as argument.
"""

import json, logging
from dataclasses import dataclass, field

import websockets
from websockets import CloseCode
from websockets.asyncio.client import connect, ClientConnection

from .definitions import PulseHandler

logger = logging.getLogger(__name__)

@dataclass
class PulseClient:
    """
    PulseClient class.

    Executes websocket requests and handles server communication.

    Parameters
    ----------
    Not required.
    """

    client_id: int
    websocket_server_url: str = ""
    message_handler_list: list[PulseHandler] = field(default_factory=list[PulseHandler])
    mean_delay: float = field(default=0.0, init=False)

    async def connect(self):
        """
        Connect to the websocket server and start RX/TX loop.
        """
        async with connect(self.websocket_server_url) as websocket:
            await self.rx_tx_loop(websocket)

    async def disconnect(self, websocket: ClientConnection):
        """
        Disconnect from the websocket server.
        :param websocket:
        :return:
        """
        try:
            await websocket.close(code=CloseCode.NORMAL_CLOSURE, reason='')
        except websockets.exceptions.ConnectionClosedError:
            pass

    async def rx_tx_loop(self, websocket: ClientConnection):
        """
        Handle receive/transmit loop.
        """
        while True:
            message = await websocket.recv()
            json_message = json.loads(message)
            # Goes through all handlers till it finds one that matches the incoming message
            for handler in self.message_handler_list:
                if handler.is_triggered(json_object=json_message):
                    logger.debug(f"{json_message} is triggering handler {handler}")
                    result = handler.action(message) #sync for now, potentially async in the future
                    await websocket.send(result)
                    break
            else:
                logger.warning(f"{json_message} is missing handler")

