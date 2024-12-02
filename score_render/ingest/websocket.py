import time
import asyncio
import websockets

class WebSocketClient:
    def __init__(self, uri, on_message_callback):
        """
        Initialize the WebSocket client.

        Args:
            uri (str): WebSocket server URI.
            on_message_callback (callable): A function to call when a message is received.
        """
        self.uri = uri
        self.on_message_callback = on_message_callback
        self.running = False
        self.websocket = None

    async def connect(self):
        """Connect to the WebSocket server."""
        self.running = True
        try:
            async with websockets.connect(self.uri) as websocket:
                self.websocket = websocket
                await self.listen(websocket)
        finally:
            # Ensure the connection is properly closed
            self.running = False
            self.websocket = None
            print("WebSocket connection closed.")

    async def listen(self, websocket):
        """Listen for messages from the WebSocket server."""
        try:
            while self.running:
                message = await websocket.recv()
                if self.on_message_callback:
                    self.on_message_callback(message)
        except websockets.exceptions.ConnectionClosedOK:
            print("WebSocket closed by the server.")
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"WebSocket connection error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    async def close(self):
        """Gracefully close the WebSocket connection."""
        if self.websocket:
            try:
                await self.websocket.close()
                print("WebSocket connection gracefully closed.")
            except Exception as e:
                print(f"Error during WebSocket close: {e}")

    def stop(self):
        """Stop the WebSocket client."""
        self.running = False


class WebSocketHandler:
    def __init__(self, uri, on_message_callback, reconnect_delay=5):
        self.uri = uri
        self.on_message_callback = on_message_callback
        self.reconnect_delay = reconnect_delay
        self.client = None
        self.running = True

    def start(self):
        """Start the WebSocket client and manage reconnection."""
        while self.running:
            try:
                asyncio.run(self.connect_and_listen())
            except Exception as e:
                print(f"WebSocket connection failed: {e}. Retrying in {self.reconnect_delay} seconds...")
                time.sleep(self.reconnect_delay)

    async def connect_and_listen(self):
        """Create a WebSocket client and listen for messages."""
        self.client = WebSocketClient(self.uri, self.on_message_callback)
        try:
            await self.client.connect()
        finally:
            await self.client.close()

    def stop(self):
        """Stop the WebSocket client."""
        self.running = False
        if self.client:
            asyncio.run(self.client.close())
