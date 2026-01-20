from pulsews.decorators import since
from typing import Any


@since(version='0.0.1-dev.1')
def should_trigger(json_object: dict, path: list[str], expected_value: Any) -> bool:
	"""Determines whether a given JSON object satisfies a specific activation condition.

	This function navigates through the `json_object` following the sequence of keys
	in `path` and checks whether the value at the final key matches `expected_value`.

	Args:
		json_object (dict): The JSON object to check.
		path (list[str]): A list of keys representing the nested path to follow in the JSON object.
		expected_value (Any): The value expected at the end of the path to trigger activation.

	Returns:
		bool: True if the value at the specified path matches `expected_value`, False otherwise.

	Raises:
		TypeError: json_object is not of type dict
	"""
	# If input json_object is an empty dict or it's not instance of dict, raise TypeError
	if not json_object or not isinstance(json_object, dict):
		raise TypeError('json_object must be of type dict')

	for key in path:
		if key in json_object:
			json_object = json_object[key]
		else:
			return False
	return json_object == expected_value
