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

"""A runtime implementation for configarium-models's MQTT model."""

import ssl

from configarium_models.models.mqtt import MQTTConnectionModel
from paho.mqtt.client import Client
from paho.mqtt.enums import CallbackAPIVersion, MQTTErrorCode


class MQTTConnectionRuntimeError(Exception):
    """Exceptions thrown by MQTTConnectionRuntime class."""


class MQTTConnectionRuntime:
    """Runtime class to create and connect a MQTT client to the specified broker."""

    @classmethod
    def create_client_from_model(cls, model: MQTTConnectionModel) -> Client:
        """Create a MQTT client from the provided model."""
        client = Client(
            client_id=model.client_id,
            clean_session=model.clean_session,
            transport=model.transport,
            callback_api_version=CallbackAPIVersion.VERSION2,
        )
        setattr(client, "model", model) # noqa: B010 my IDE whines about client.model = model
        client.ws_set_options(path=model.websocket_path)
        if model.ssl:
            client.tls_set(
                ca_certs=None,
                certfile=None,
                keyfile=None,
                cert_reqs=[ssl.CERT_NONE, ssl.CERT_REQUIRED][model.ssl_verify],
                tls_version=ssl.PROTOCOL_TLS,
                ciphers=None)

        if model.username is not None:
            client.username_pw_set(model.username, model.password)

        return client

    @classmethod
    def connect(cls, client: Client) -> MQTTErrorCode:
        """Connect to the MQTT broker with a client created by MQTTConnectionRuntime.create_client_from_model."""
        model: MQTTConnectionModel | None = getattr(client, "model", None)
        if model:
            return client.connect(model.host, port=model.port, keepalive=model.keepalive)
        msg = "Model not found on Client. Call MQTTConnectionRuntime.create_client_from_model before this method."
        raise MQTTConnectionRuntimeError(msg)
