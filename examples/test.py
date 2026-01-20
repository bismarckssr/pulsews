# used for random tests every now and then. committed for fun

import json

json_str = '{"name": "John", "age": 30, "city": "New York"}'
more_complex_json_str = '{"name": "John", "age": 30, "city": "New York", "address": {"street": "Main St", "number": 123}}'


# Parse JSON
y = json.loads(more_complex_json_str)

# the result is a Python dictionary:
print(list(y.keys()))
