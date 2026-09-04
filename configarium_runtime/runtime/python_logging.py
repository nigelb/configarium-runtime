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

"""A runtime implementation for configarium-models's python_logging model."""

import logging

from configarium_models.models.python_logging import LoggingConfig


class PythonLoggingRuntime:
    """Runtime class to apply the LoggingConfig configuration."""

    @classmethod
    def apply_model(cls, model: LoggingConfig, **kwargs: str | int | None) -> None:
        """Apply the model and configure python logging by calling logging.basicConfig."""
        kwargs.update(
            format=model.format,
            datefmt=model.date_format,
            style=model.style,
            level=logging._nameToLevel[model.log_level.upper()], # noqa: SLF001 getLevelNamesMapping not until python3.12
            filename=model.filename,
            filemode=model.filemode,
        )
        logging.basicConfig(**kwargs)
        for lgr in model.logger_configs:
            logging.getLogger(lgr.logger_name).setLevel(logging._nameToLevel[lgr.log_level.upper()]) # noqa: SLF001 getLevelNamesMapping not until python3.12
