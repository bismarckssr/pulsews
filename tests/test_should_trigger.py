import pytest
from typing import Any
from pulsews.definitions import should_trigger


@pytest.mark.parametrize(
	'json_object, path, expected, expected_result',
	[
		# Positive test cases that return True
		({'a': {'b': 10}}, ['a', 'b'], 10, True),
		({'x': {'y': {'z': 'ok'}}}, ['x', 'y', 'z'], 'ok', True),
		(
			{'user': {'address': {'street': 'Main St'}}},
			['user', 'address', 'street'],
			'Main St',
			True,
		),
		(
			{'level1': {'level2': {'level3': 42}}},
			['level1', 'level2', 'level3'],
			42,
			True,
		),
		({'outer': {'inner': None}}, ['outer', 'inner'], None, True),
		# Negative test cases that return False due to various problems
		({'a': {'b': 1}}, ['a', 'b'], 2, False),  # Wrong value
		(
			{'user': {'address': {}}},
			['user', 'address', 'street'],
			'Main St',
			False,
		),  # Missing key
		({'a': {'b': 0}}, ['a', 'b'], 1, False),  # falsy ma non coincide
		({'flag': False}, ['flag'], True, False),  # falsy boolean non coincide
	],
)
def test_create_trigger(
	json_object: dict, path: list[str], expected: Any, expected_result: bool
):
	result = should_trigger(json_object=json_object, path=path, expected_value=expected)
	assert result == expected_result


def test_should_trigger_type_errors():
	# TypeError case: input is not a dict
	with pytest.raises(TypeError):
		should_trigger(json_object=None, path=['a'], expected_value=1)

	with pytest.raises(TypeError):
		should_trigger(json_object=[], path=['a'], expected_value=1)

	with pytest.raises(TypeError):
		should_trigger(json_object={}, path=['a'], expected_value=1)
