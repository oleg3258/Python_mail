import asyncio

class Client:
    def __init__(self, host, port, timeout):
        self.host = host
        self.port = port
        self.timeout = timeout

    #сохраняем метрику на сервере
async def put(self, key, value):
    loop = asyncio.get_event_loop()
    writer = await asyncio.open_connection(self.host, self.port, loop = loop)

    message =
    writer.write()
    #получаем метрику с сервера
    def get(self):
        pass

import asyncio
@asyncio.coroutine
def hello_world():
    while True:
        print("Hello World!")
        yield from asyncio.sleep(1.0)

loop = asyncio.get_event_loop()
loop.run_until_complete(hello_world())
loop.close()





