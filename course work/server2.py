import asyncio
import websockets
import psutil
import os
import json

from tendo.singleton import SingleInstance

HOST, PORT = 'localhost', 1112
DEFAULT_TIMER = 10

def disc_free(unit):
    disc = psutil.disk_usage('/')
    return disc[2] / (2 ** 30)


def get_process():
    p = psutil.Process(os.getpid()).as_dict(attrs=[
        'pid', 'ppid', 'name', 'exe', 'cpu_percent', 'num_threads', 'username'
    ])
    return p

async def server(websocket):
    async for message in websocket:
        match json.loads(message):
            case 'stop':
                await websocket.close(code=1000, reason='')
            case 'once':
                try:
                    await websocket.send(json.dumps(get_process()))
                    await websocket.send(json.dumps(disc_free(json.loads(message))))
                    await websocket.close()
                except websockets.ConnectionClosedOK:
                    break
            case _:
                try:
                    dataOld1 = None
                    dataOld2 = None
                    for i in range(int(json.loads(message))):
                        dataNew1 = get_process()
                        dataNew2 = disc_free(json.loads(message))
                        if dataOld1 == dataNew1 and dataOld2 == dataNew2:
                            await asyncio.sleep(1)
                            continue
                        elif dataOld1 != dataNew1:
                            dataOld1 = dataNew1
                            await websocket.send(json.dumps(dataOld1))
                        elif dataOld2 != dataNew2:
                            dataOld2 = dataNew2
                            await websocket.send(json.dumps(dataOld2))
                        else:
                            await websocket.send(json.dumps(get_process()))
                            await websocket.send(json.dumps(disc_free(json.loads(message))))
                            await asyncio.sleep(1)
                    await websocket.close()
                except websockets.ConnectionClosedOK:
                    break


async def main():
    async with websockets.serve(server, HOST, PORT):
        await asyncio.Future()

me = SingleInstance()
asyncio.run(main())
