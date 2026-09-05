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
from typing import Any

from configarium_models.models.python_logging import LoggingConfig


class PythonLoggingRuntime:
    """Runtime class to apply the LoggingConfig configuration."""

    @classmethod
    def apply_model(cls,
                    model: LoggingConfig,
                    **kwargs: Any, #noqa: ANN401 ruff/ty 🤯
                    ) -> None:
        """Apply the model and configure python logging by calling logging.basicConfig."""
        for name in model.model_fields_set:
            value = getattr(model, name)
            if value is not None:
                kwargs.update({name: value})
        logging.basicConfig(**kwargs)
        for lgr in model.logger_configs:
            logging.getLogger(lgr.logger_name).setLevel(logging._nameToLevel[lgr.log_level.upper()]) # noqa: SLF001 getLevelNamesMapping not until python3.12
