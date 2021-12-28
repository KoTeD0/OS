import asyncio
import websockets
import win32api
import json

from tendo.singleton import SingleInstance

HOST, PORT = 'localhost', 1111


def display_monitors():
    monitors = win32api.EnumDisplayMonitors()
    dynaMon = []
    [dynaMon.append(monitors[i][2]) for i in range(0, len(monitors))]
    return json.dumps(dynaMon)


async def server(websocket):
    async for message in websocket:
        match json.loads(message):
            case 'stop':
                await websocket.close(code=1000, reason='')
            case 'once':
                try:
                    await websocket.send(display_monitors())
                    await websocket.close()
                except websockets.ConnectionClosedOK:
                    break
            case _:
                try:
                    dataOld = None
                    for i in range(int(json.loads(message))):
                        dataNew = display_monitors()
                        if dataOld == dataNew:
                            await asyncio.sleep(1)
                            continue
                        else:
                            dataOld = dataNew
                            await websocket.send(dataOld)
                            await asyncio.sleep(1)
                    await websocket.close()
                except websockets.ConnectionClosedOK:
                    break


async def main():
    async with websockets.serve(server, HOST, PORT):
        await asyncio.Future()

me = SingleInstance()
asyncio.run(main())
