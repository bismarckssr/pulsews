import functools


def since(version: str):
	"""Decorator used to add descriptive fields to functions / methods.

	Useful to keep track of versions, at least currently.
	In the future might be deprecated in favour of a more generic decorator.

	Args:
		version (str): Describes when such function was introduced in the codebase.

	Returns:
		The decorator function

	Raises:
		None
	"""

	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			return func(*args, **kwargs)

		wrapper._since = version
		return wrapper

	return decorator
