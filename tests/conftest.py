import pytest

from file_storage.controller import Controller


@pytest.fixture(name='controller')
def _controller():
    return Controller()
