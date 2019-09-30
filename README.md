# Websocket Broadcasting with FastAPI
Simple example showing how to broadcast to websockets using rabbitmq and aio-pika on FastAPI

## Usage
Bring the containers up with:
```bash
docker-compose up -d --build
```

Open up three internet browesers and navigate each one to the following addresses
1. http://localhost
2. http://localhost
3. http://localhost/docs

You should have something that looks like this:

![Open these windows](https://i.ibb.co/zZp9Pjs/display.png)

Click the button in windows (1) and (2) and then window (3), expand down the "push" endpoint, click "Try It", enter a message and click execute. All being well, you should see the message appear in both windows! :smiley: :rocket:
