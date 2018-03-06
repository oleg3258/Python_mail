import asyncio

class Data(object):
    def __init__(self):
        self.data = {}
    def process_data(self, data):
        if data[0:3] == 'put':
            data_strip = data.lstrip('put')
            try:
                answer = data_strip.split(' ')
                key = answer[1]
                value = float(answer[2])
                timestamp = int(answer[3])
                if self.data.get(key) is None:
                    self.data[key] = [(value, timestamp)]
                else:
                    self.data[key].append((value, timestamp))
#                print ('put: ', self.data[key])
            except:
                resp = 'error\nwrong command\n\n'
            finally:
                resp = 'ok\n\n'
        elif data[0:3] == 'get':
            data_strip = data.lstrip('get').rstrip('\n')
            resp = 'ok\n'
            try:
                if not data.find('*') == -1:
                    for key in self.data:
                        for i in self.data[key]:
                            resp += key
                            resp += ' '
                            resp += str(i[0]) + ' ' + str(i[1]) + '\n'
                            #print(resp)
                else:
                    key = str(data_strip.split(' ')[1])
                    key = key.strip(' \n')
                    key = key.rstrip('\n')
                    #print('get', key, '!', sep = '')
                    if not self.data.get(key) is None:
                        for i in self.data[key]:
                            print(i)
                            resp += key
                            resp += ' '
                            resp += str(i[0]) + ' ' + str(i[1]) + '\n'
            except Exception as err:
                #print('ex in get:', err.args)
                resp = 'error\nwrong command\n\n'
            finally:
                resp += '\n'
        else:
            resp = 'error\nwrong command\n\n'
        return resp


class ClientServerProtocol(asyncio.Protocol):
    metrics = Data()
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.metrics.process_data(data.decode())
        #print (resp)
        self.transport.write(resp.encode())

def run_server(host, port):

    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)

    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

#run_server('127.0.0.1', 2233)