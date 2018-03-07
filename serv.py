# создание сокета, сервер
import socket
# https://docs.python.org/3/library/socket.html
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('192.168.0.102', 8887)) # max port 65535
sock.listen(socket.SOMAXCONN)
conn, addr = sock.accept()
while True:
    data = conn.recv(1024)
    if not data:
        break
    print (data.decode('utf8'))
    conn.send(b'pidor')

conn.close()
sock.close()



#
# import asyncio
# async def handle_echo(reader, writer):
#     data = await reader.read(1024)
#     message = data.decode()
#     addr = writer.get_extra_info("peername")
#     print("received %r from %r" % (message, addr))
#     writer.close()
#
# loop = asyncio.get_event_loop()
# coro = asyncio.start_server(handle_echo, '192.168.0.102', 8887,loop=loop)
# server = loop.run_until_complete(coro)
# try:
#     loop.run_forever()
# except KeyboardInterrupt:
#     pass
# server.close()
# loop.run_until_complete(server.wait_closed())
# loop.close()
