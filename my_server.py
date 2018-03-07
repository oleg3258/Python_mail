import asyncio

class recieved_data(object):
    def __init__(self):
        self.data = {}

    def process_data(self, data):
        if data[0:3] == 'put':
            data_list = data.split()
            try:
                key = data_list[1]
                value = float(data_list[2])
                timestamp = int(data_list[3])
                if key not in self.data:
                    self.data[key] = []
                    self.data[key].append((value, timestamp))
                else:
                    self.data[key].append((value, timestamp))

                # print (self.data)
            except:
                resp = 'error\nwrong command\n\n'
            finally:
                resp = 'ok\n\n'
        elif data[0:3] == 'get':
            # print (self.data)
            data_list = data.split()
            # print (data_list)
            resp = 'ok\n'
            try:
                if '*' in data_list:
                    for key in self.data:
                        for i in self.data[key]:
                            resp = '{0} {1} {2}\n'.format(key, str(i[0]), str(i[1]))
                            print(resp)
                else:
                    key = data_list[1]
                    # print (key)
                    if key in self.data:
                        # print ('key is in a dict')
                        for i in self.data[key]:
                            resp = '{0} {1} {2}\n'.format(key, str(i[0]), str(i[1]))
                            print (resp)
            except Exception as err:
                resp = 'error\nwrong command\n\n'
            finally:
                resp += '\n'
        else:
            resp = 'error\nwrong command\n\n'
        return resp


class ClientServerProtocol(asyncio.Protocol):
    metric = recieved_data()
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.metric.process_data(data.decode())
        self.transport.write(resp.encode())

def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)
    print (f'server was started on {host} {port}')

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

run_server('192.168.0.102', 8887)
