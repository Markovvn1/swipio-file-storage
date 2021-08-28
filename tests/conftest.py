import os

import pytest

from file_storage.controller import Controller
from file_storage.model import Model


@pytest.fixture(name='model')
def _model():
    if os.path.isfile('test.db'):
        os.remove('test.db')
    return Model('sqlite:///test.db')


@pytest.fixture(name='controller')
def _controller():
    if os.path.isfile('test.db'):
        os.remove('test.db')
    return Controller('storage_4del', 'sqlite:///test.db')
