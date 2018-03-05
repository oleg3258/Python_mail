import socket
import time

class Client:
    def __init__(self, host, port, timeout = None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.connection = socket.create_connection((host, port),timeout)

    def put(self, key, value, timestamp=None):
        try:
            if timestamp is None:
                timestamp = str(int(time.time()))
            message = f'put {key} {value} {timestamp}\n'
            self.connection.sendall(message.encode('utf-8'))
            data = self.connection.recv(1024).decode().split('\n')
            print (data)
            if 'error' in data:
                raise ClientError()
        except socket.error:
            raise ClientError()

    #получаем метрику с сервера
    def get(self, metric):
        message = f'get {metric}\n'
        self.connection.sendall(message.encode("utf-8"))
        try:
            data = self.connection.recv(4096).decode('utf8')
            if data == "error\nwrong command\n\n":
                raise ClientError()
            elif "ok\n\n" in data:
                return {}
            else:
                m = data.split()
                del m[0]
                val_dict = {}
                for i in range(len(m[1:])):
                    if not m[i][:1].isdigit():
                        new_tuple = (int(m[i + 2]), float(m[i + 1]))
                        if (m[i] not in val_dict):
                            val_dict[m[i]] = []
                            val_dict[m[i]].append(new_tuple)
                        else:
                            val_dict[m[i]].append(new_tuple)
                    else:
                        continue
                return val_dict
        except socket.error:
            raise ClientError()

class ClientError(Exception):
    pass


# client = Client('127.0.0.1', 10000, timeout=15)
# client.put("palm.cpu", 0.5, timestamp=1150864247)
# # client.get("palm.cpu")

