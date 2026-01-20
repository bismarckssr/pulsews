import json
import logging
from dataclasses import dataclass, field

import websockets
from websockets import CloseCode
from websockets.asyncio.client import connect, ClientConnection

from .definitions import PulseHandler

logger = logging.getLogger(__name__)


@dataclass
class PulseClient:
	"""A websocket client that connects to a server, receives messages, and dispatches them to handlers.

	This class manages a continuous receive/transmit loop over a websocket connection.
	Incoming messages are parsed as JSON and checked against the list of registered handlers.
	The first handler that triggers will process the message and send a response back to the server.
	Messages without a matching handler will be logged as warnings.

	Args:
		client_id (int): A unique identifier for this client.
		websocket_server_url (str): The URL of the websocket server to connect to.
		message_handler_list (list[PulseHandler]): A list of handlers to process incoming messages.
		mean_delay (float): Average delay between operations (initialized internally).
	"""

	client_id: int
	websocket_server_url: str = ''
	message_handler_list: list[PulseHandler] = field(default_factory=list[PulseHandler])
	mean_delay: float = field(default=0.0, init=False)

	async def connect(self):
		"""Connect to the websocket server and start the receive/transmit loop.

		Opens a websocket connection using `websocket_server_url` and starts
		the `rx_tx_loop` to handle incoming and outgoing messages.

		Raises:
			websockets.exceptions.InvalidURI: If the websocket_server_url is invalid.
			websockets.exceptions.WebSocketException: For other websocket connection errors.
		"""
		async with connect(self.websocket_server_url) as websocket:
			await self.rx_tx_loop(websocket)

	async def disconnect(self, websocket: ClientConnection):
		"""Disconnect from the websocket server gracefully.

		Attempts to close the websocket connection with a normal closure code.
		Ignores errors if the connection is already closed.

		Args:
			websocket (ClientConnection): The websocket connection to close.
		"""
		try:
			await websocket.close(code=CloseCode.NORMAL_CLOSURE, reason='')
		except websockets.exceptions.ConnectionClosedError:
			pass

	async def rx_tx_loop(self, websocket: ClientConnection):
		"""Run the receive/transmit loop for processing websocket messages.

		Continuously listens for messages from the websocket server.
		Each message is parsed as JSON and evaluated against the registered handlers.
		The first handler that triggers will execute its action and send a response back.
		If no handler triggers, a warning is logged.

		Args:
			websocket (ClientConnection): The active websocket connection for receiving and sending messages.
		"""
		while True:
			message = await websocket.recv()
			json_message = json.loads(message)
			for handler in self.message_handler_list:
				if handler.is_triggered(json_object=json_message):
					logger.debug(f'{json_message} is triggering handler {handler}')
					result = handler.action(
						message
					)  # sync for now, potentially async later
					await websocket.send(result)
					break
			else:
				logger.warning(f'{json_message} is missing handler')
