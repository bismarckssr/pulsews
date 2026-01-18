from pulsews import PulseEngine, PulseHandler, ActivateObject
import json, logging, asyncio

# Parameter "enforced" by Callable type definition on action parameter
handler1 = PulseHandler(
    activate_object=ActivateObject(path=["type"], value="ping"),
    action=lambda message : json.dumps({"type": "pong"})
)

handler2 = PulseHandler(
    activate_object=ActivateObject(path=["type"], value="welcome"),
    action=lambda message : json.dumps({"type": "options"})
)

stresser = PulseEngine(
    websocket_server_url="wss://ws.playscopa.online/",
    number_of_clients=4,
    duration=60,
    list_of_message_handlers=[
        handler1, handler2
    ]
)

async def main():
    await stresser.run()

if __name__ == "__main__":
   # Logging configuration
   logger = logging.getLogger("pulsews")
   logger.setLevel(logging.DEBUG)

   # Starting the loop
   logging.info("Starting loop")
   asyncio.run(main())