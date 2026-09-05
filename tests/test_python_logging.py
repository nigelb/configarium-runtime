# Configarium-runtime provides runtime utilities for configarium-models.
# Copyright (C) 2026 NigelB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for the configarium-runtime library's python_logging runtime."""

import logging
import sys

from configarium_models.models.python_logging import LoggingConfig

from configarium_runtime.runtime.python_logging import PythonLoggingRuntime


def test_basic_config() -> None:
    """Tests for the configarium-runtime library's python_logging runtime."""
    config = LoggingConfig()
    PythonLoggingRuntime.apply_model(config)


def test_apply_model_configures_stderr_stream() -> None:
    """Test that apply_model configures a stderr stream handler."""
    original_handlers = logging.root.handlers[:]

    logging.root.handlers.clear()

    try:
        config = LoggingConfig()

        PythonLoggingRuntime.apply_model(config, stream=sys.stderr)

        assert len(logging.root.handlers) == 1

        handler = logging.root.handlers[0]
        assert isinstance(handler, logging.StreamHandler)
        assert handler.stream is sys.stderr
    finally:
        logging.root.handlers.clear()
        logging.root.handlers.extend(original_handlers)
