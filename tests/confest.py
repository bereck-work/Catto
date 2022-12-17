# -*- coding: utf-8 -*-

import logging

import pytest
from _pytest.logging import caplog as _caplog
from loguru import logger


@pytest.fixture
def caplog(caplog: _caplog):
    class PropagateHandler(logging.Handler):
        def emit(self, record):
            logging.getLogger(record.name).handle(record)

    handler_id = logger.add(PropagateHandler(), format="{message}")
    yield caplog
    logger.remove(handler_id)
