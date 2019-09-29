from typing import List
from starlette.websockets import WebSocket

import asyncio
from aio_pika import connect, Message, IncomingMessage


class Notifier:
    def __init__(self):
        self.connections: List[WebSocket] = []
        self.is_ready = False

    async def setup(self, queue_name: str):
        self.rmq_conn = await connect(
            "amqp://guest:guest@rabbitmq/",
            loop=asyncio.get_running_loop()
        )
        self.channel = await self.rmq_conn.channel()
        self.queue_name = queue_name
        queue = await self.channel.declare_queue(self.queue_name)
        await queue.consume(self._notify, no_ack=True)
        self.is_ready = True

    async def push(self, msg: str):
        await self.channel.default_exchange.publish(
            Message(msg.encode("ascii")),
            routing_key=self.queue_name,
        )

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def remove(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def _notify(self, message: IncomingMessage):
        living_connections = []
        while len(self.connections) > 0:
            websocket = self.connections.pop()
            await websocket.send_text(f"{message.body}")
            living_connections.append(websocket)
        self.connections = living_connections
