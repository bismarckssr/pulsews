from pulsews.decorators import since
from pulsews import PulseHandler


@since(version='0.0.1-dev.1')
def foo(x, y='bar'):
	return x


def test_since_decorator_attr():
	assert foo._since == '0.0.1-dev.1'
	assert foo.__name__ == 'foo'


def test_since_pulsehandler():
	assert PulseHandler.is_triggered._since == '0.0.1-dev.1'
	assert PulseHandler.is_triggered.__name__ == 'is_triggered'
