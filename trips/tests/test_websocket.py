from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
import pytest

from taxiapp import asgi


TEST_CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

application = asgi.application
path = "/taxiapp/"

websocket_config = dict(application=application, path=path)


@pytest.mark.asyncio
class TestWebSocket:
    async def test_can_connect_to_server(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(**websocket_config)
        connected, _ = await communicator.connect()
        assert connected is True
        await communicator.disconnect()

    async def test_can_send_and_receive_messages(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(**websocket_config)
        connected, _ = await communicator.connect()
        message = {
            "type": "echo.message",
            "data": "This is a test message.",
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_can_send_and_receive_broadcast_messages(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(**websocket_config)
        connected, _ = await communicator.connect()
        message = {
            "type": "echo.message",
            "data": "This is a test message.",
        }
        channel_layer = get_channel_layer()
        await channel_layer.group_send("test", message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()
