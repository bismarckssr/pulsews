from dataclasses import dataclass
from typing import Callable
from deprecated import deprecated
from pulsews.decorators import since
from .functions import should_trigger


@dataclass
class ActivateObject:
	"""Class to keep parameters for the activation condition of the handler.

	Made as class for future extension whilst keeping domain boundaries.

	Args:
		path (list[str]): Indicates the activation path to search for within the JSON object.
		value (str): Indicates the expected value to trigger activation.

	Raises:
		None
	"""

	path: list[str]
	value: str


@dataclass
class PulseHandler:
	"""Main class for handlers used during websocket messaging.

	This class stores an action to run and the conditions under which it should be triggered.
	The activation condition is defined using an ActivateObject instance.

	Attributes:
		activate_object (ActivateObject): The full piece of message to check for activation.
		action (Callable[[str], str]): Function to execute when the activation condition is met.
	"""

	activate_object: ActivateObject
	action: Callable[[str], str]

	@deprecated(
		version='0.0.1-dev.1',
		reason="Use should_trigger as it's more performant and more readable",
	)
	def _create_trigger_recursive(self, json_object: dict, current_index: int = 0):
		"""Recursively checks whether the specified path and value exists in a JSON object.

		This method is deprecated due to performance issues; use `is_triggered` instead.

		Args:
			json_object (dict): The JSON object to search within.
			current_index (int, optional): The current index in the path list. Defaults to 0.

		Returns:
			bool: True if the value at the specified path matches the expected value, False otherwise.

		Raises:
			None
		"""
		keys = list(json_object.keys())
		local_path = self.activate_object.path

		if len(local_path) == current_index + 1:
			final_value = json_object.get(keys[current_index])
			return final_value == self.activate_object.value

		for key in keys:
			if key == local_path[current_index]:
				current_index += 1
				return self._create_trigger(
					json_object[key], current_index=current_index
				)
		return False

	@since(version='0.0.1-dev.1')
	def is_triggered(self, json_object: dict) -> bool:
		"""Checks whether the handler should be triggered for a given JSON object.

		Uses the external `should_trigger` function for better performance and readability.

		Args:
			json_object (dict): The JSON object to check for activation.

		Returns:
			bool: True if the activation condition is met, False otherwise.

		Raises:
			None
		"""
		return should_trigger(
			json_object=json_object,
			path=self.activate_object.path,
			expected_value=self.activate_object.value,
		)
