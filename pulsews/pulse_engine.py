import asyncio
import logging
from dataclasses import dataclass, field

from pulsews.definitions import PulseHandler

from pulsews.pulse_client import PulseClient as pc

logger = logging.getLogger(__name__)


@dataclass
class PulseEngine:
	websocket_server_url: str
	number_of_clients: int
	list_of_message_handlers: list[PulseHandler]
	# on_boot_action: Callable[[], str] - will allow clients to send this as the first thing when connecting. to be implemented.
	duration: int = 300  # in seconds
	client_list: list[pc] = field(default_factory=list[pc])

	async def run(self):
		logger.info('Starting PulseEngine')
		tasks = []
		for i in range(self.number_of_clients):
			logger.debug(f'Starting PulseClient {i}')
			current_client = pc(
				client_id=i,
				websocket_server_url=self.websocket_server_url,
				message_handler_list=self.list_of_message_handlers,
			)
			self.client_list.append(current_client)
			tasks.append(current_client.connect())

		# Start all tasks using gather. If one of the tasks fails, the rest will NOT be affected as opposed to TaskGroup.
		await asyncio.gather(*tasks)
