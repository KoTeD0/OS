import asyncio
import websockets
import json


async def cServer1(msg='once'):
    uri = 'ws://localhost:1111'
    async with websockets.connect(uri) as client:
        while client:
            try:
                await client.send(json.dumps(msg))
                data = json.loads(await client.recv())
                [print(f"Monitor {i + 1} specs: {data[i]}") for i in range(0, len(data))]
            except websockets.ConnectionClosedOK:
                break


async def cServer2(msg='once'):
    uri = 'ws://localhost:1112'
    async with websockets.connect(uri) as client:
        while client:
            try:
                await client.send(json.dumps(msg))
                data = json.loads(await client.recv())
                print(data)
            except websockets.ConnectionClosedOK:
                break


async def main():
    while True:
        action = input("\n1 - connect to 1 server \n2 - connect to 2 server\nexit - Exit\n\n").split()
        if action and action[0] == '1':
            if len(action) != 1:
                asyncio.create_task(cServer1(action[1]))
            else:
                asyncio.create_task(cServer1())
        if action and action[0] == '2':
            if len(action) != 1:
                asyncio.create_task(cServer2(action[1]))
            else:
                asyncio.create_task(cServer2())
        if action and action[0] == 'exit':
            break


if __name__ == '__main__':
    asyncio.run(main())
