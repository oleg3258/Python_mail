import asyncio
import time

def async_loop(f):
    loop = asyncio.get_event_loop()
    def decorated(*args, **kwargs):
        loop.run_until_complete(f(*args, **kwargs))
    return decorated


class Client:
    def __init__(self, host, port, timeout = None):
        self.host = host
        self.port = port
        self.timeout = timeout

    @async_loop
    async def put(self, key, value, timestamp=None):
        reader, writer = await asyncio.open_connection(self.host, self.port)

        if timestamp == None:
            timestamp = str(int(time.time()))

        message = 'put ' + key + ' ' + str(value) + ' ' + str(timestamp) + '\n'
        print('Send: %r' % message)
        writer.write(message.encode())

        data = await reader.read(100)
        print('Received: %r' % data.decode())
        if not data:
            raise ClientError

        print('Close the socket')
        writer.close()

    #получаем метрику с сервера
    @async_loop
    async def get(self, metric):
        reader, writer = await asyncio.open_connection(self.host, self.port)

        print('Send: %r' % metric)
        writer.write(metric.encode())

        data = await reader.read(300)
        print (data.decode())
        print('Received: %r' % data.decode())
        if not data:
            raise ClientError

        m = data.decode().split()
        val_dict = {}
        key_words = ['eardrum.cpu', 'palm.cpu']
        for i in range(len(m)):
            if (m[i] in key_words):
                new_tuple = (int(m[i + 2]), float(m[i + 1]))
                if (m[i] not in val_dict):
                    val_dict[m[i]] = []
                    val_dict[m[i]].append(new_tuple)
                else:
                    val_dict[m[i]].append(new_tuple)
            else:
                continue
        return val_dict

class ClientError(Exception):
    pass


client = Client('127.0.0.1', 8887, timeout=15)
client.put("palm.cpu", 0.5, timestamp=1150864247)
# client.get("palm.cpu")

