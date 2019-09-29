import logging

from fastapi import FastAPI
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket, WebSocketDisconnect

from notifier import Notifier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
notifier = Notifier()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI</title>
    </head>
    <body>
        <h1>WebSocket Test</h1>
        <form action="" onsubmit="connectWS1(event)">
            <button>Connect to ws://localhost/ws</button>
        </form>
        <ul id='messages'></ul>
        <script>
            function connectWS1(event) {
                var ws = new WebSocket("ws://localhost/ws");
                ws.addEventListener('open', (event) => {
                    alert('WebSocket Connected!')
                });
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.post("/push")
async def push_to_connected_websockets(message: str):
    if not notifier.is_ready:
        await notifier.setup("test")
    await notifier.push(f"! Push notification: {message} !")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await notifier.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        notifier.remove(websocket)


@app.get("/")
async def get():
    return HTMLResponse(html)
