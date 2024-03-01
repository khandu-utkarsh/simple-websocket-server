# #### Code from chat gpt

#  from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
# # from hashlib import sha1
# # from typing import Set
# # from urllib.parse import urlparse
# # import datetime
# # import array
# # import json
# # import logging
# # import os
# # import struct
# # from base64 import b64encode 

# # HOST = ''
# # PORT = 8002
# # CHUNKSZ = 2048
# # MAGIC_STRING = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

# # client_pool = set()
# # ID = 1
# # logger = logging.getLogger(__name__)

# class WebSocketHandler(SimpleHTTPRequestHandler):
#     def __init__(self, *args, **kwargs):
#         print("Inside constructor of web socket handler")
#         SimpleHTTPRequestHandler.__init__(self, *args, **kwargs)
#         self.websocket_mode = False


#     def do_GET(self):

#         #Checking if the connection needs to be upgraded to websocket:
#         if (self.headers.get('connection') == 'Upgrade' and self.headers.get('upgrade', '').lower() == 'websocket'):
#             logger.info('Upgrading HTTP to websocket connection')
#             self.websocket_mode = True
            
#             #Have to make changes to promote it to a websocket
            
#             self.websocket_handshake()
#             return self.serve()

#         if self.path == '/':
#             self.path = '/index.html'
#         path = os.path.abspath(os.path.dirname(self.server.index_file))
#         path = os.path.normpath(path + self.path)
#         path = urlparse(path).path
#         if not os.path.exists(path):
#             self.send_error(404)
#             return
#         self.send_response(200)
#         self.send_header('Content-Type', self.guess_type(path))
#         self.end_headers()
#         with open(path) as f:
#             self.wfile.write(f.read())

#     def finish(self):
#         # when in websocket mode, don't close the connection.
#         # This will block the server if it doesn't use the ThreadingMixIn
#         if not self.websocket_mode:
#             SimpleHTTPRequestHandler.finish(self)

#     def websocket_handshake(self):
#         secret_key = self.headers.dict.get('sec-websocket-key', '')
#         hash = sha1()
#         hash.update(secret_key.encode() + MAGIC_STRING.encode())
#         accept = b64encode(hash.digest()).decode('utf-8')
#         response = [
#             'HTTP/1.1 101 Switching Protocols',
#             'Upgrade: websocket',
#             'Connection: Upgrade',
#             'Sec-WebSocket-Accept: ' + accept,
#             '', '',
#         ]
#         self.request.sendall('\r\n'.join(response).encode('utf-8'))

#     def handle_data(self, data):
#         raise NotImplementedError()

#     def serve(self):
#         while True:
#             data = Frame.unpack(self.connection)
#             if data is None or data == b'\x03\xE9':
#                 self.quit()
#                 break
#             self.handle_data(data)

#     def quit(self):
#         self.request.close()

#     def send(self, data):
#         self.write(data)

#     def write(self, data):
#         if isinstance(data, (list, tuple, set, dict)):
#             data = json.dumps(data)
#         data = data.strip()
#         if data:
#             self.wfile.write(Frame.pack(data.encode()))
#             self.wfile.flush()

#     def flush(self):
#         self.wfile.flush()


# # class Frame(object):
# #     """
# #     WebSocket Frame Reference

# #          0                   1                   2                   3
# #          0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# #         +-+-+-+-+-------+-+-------------+-------------------------------+
# #         |F|R|R|R| opcode|M| Payload len |    Extended payload length    |
# #         |I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
# #         |N|V|V|V|       |S|             |   (if payload len==126/127)   |
# #         | |1|2|3|       |K|             |                               |
# #         +-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
# #         |     Extended payload length continued, if payload len == 127  |
# #         + - - - - - - - - - - - - - - - +-------------------------------+
# #         |                               |Masking-key, if MASK set to 1  |
# #         +-------------------------------+-------------------------------+
# #         | Masking-key (continued)       |          Payload Data         |
# #         +-------------------------------- - - - - - - - - - - - - - - - +
# #         :                     Payload Data continued ...                :
# #         + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
# #         |                     Payload Data continued ...                |
# #         +---------------------------------------------------------------+
# #     """
# #     OP_CONTINUE = 0x0
# #     OP_TEXT      = 0x1
# #     OP_BINARY    = 0x2

# #     @staticmethod
# #     def unpack(socket):
# #         data = socket.recv(2)
# #         unpacked = struct.unpack('BB', data)
# #         fin = unpacked[0] & 0x80
# #         rsv1 = unpacked[0] & 0x40
# #         rsv2 = unpacked[0] & 0x20
# #         rsv3 = unpacked[0] & 0x10
# #         opcode = unpacked[0] & 0x0f
# #         payload_sz = unpacked[1] & 0x7f
# #         has_mask = bool(unpacked[1] & 0x80)

# #         if payload_sz == 126:
# #             payload_sz = socket.recv(2)
# #             payload_sz = struct.unpack('!H', payload_sz)[0]
# #         elif payload_sz == 127:
# #             raise Exception('TODO: handle data larger than 2**16 bytes.')
# #         mask = None
# #         if has_mask:
# #             mask = socket.recv(4)
# #         data = socket.recv(payload_sz)
# #         data = Frame.unmask(mask, data)
# #         return data

# #     @staticmethod
# #     def unmask(mask, data):
# #         if mask is None:
# #             return data
# #         mask = array.array('B', mask)
# #         data = array.array('B', data)
# #         for idx, old_byte in enumerate(data):
# #             data[idx] = old_byte ^ mask[idx % 4]
# #         return data.tostring()

# #     @staticmethod
# #     def pack(data, fin=1, rsv1=0, rsv2=0, rsv3=0, opcode=OP_TEXT):
# #         header = b''
# #         sz = len(data)
# #         header += struct.pack(
# #             '!B', (
# #               (fin << 7)
# #             | (rsv1 << 6)
# #             | (rsv2 << 5)
# #             | (rsv3 << 4)
# #             | opcode
# #             )
# #         )
# #         # ignore the mask bit since it's not required by the server
# #         if sz < 126:
# #             header += struct.pack('!B', sz)
# #         elif sz <= 2 ** 16:
# #             # 126 says to check the next 2 bytes for the payload sz
# #             header += struct.pack('!B', 126) + struct.pack('!H', sz)
# #         elif sz > 2 ** 16:
# #             header += struct.pack('!B', 127) + struct.pack('!Q', sz)

# #         data = data.encode('utf-8')
# #         return header + data


# # class Client(object):
# #     _ID = 1
# #     def __init__(self, username, handler):
# #         self.username = username
# #         self.connection = handler

# #         self.ID = self._ID
# #         self._ID += 1


# # class ChatServer(ThreadingHTTPServer):
# #     index_file = './index.html'     #Class variable
# #     def __init__(self, address, handler_class):
# #         ThreadingHTTPServer.__init__(self, address, handler_class)
# #         self.clients = set()

# #     def add_client(self, client):
# #         self.clients.add(client)
# #         self.send_server_message('{} has joined'.format(client.username))

# #     def send_server_message(self, message):
# #         data = {
# #             'type': 'notice',
# #             'message': message,
# #             'datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# #         }
# #         for client in self.clients:
# #             client.connection.send(data)

# #     def send_user_message(self, sent_from, message):
# #         data = {
# #             'type': 'user_message',
# #             'message': message,
# #             'username': sent_from.username,
# #             'datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# #         }
# #         for client in self.clients:
# #             client.connection.send(data)


# # class ChatHandler(WebSocketHandler):
# #     def __init__(self, *args, **kwargs):
# #         super().__init__(*args, **kwargs)
# #         self.websocket_mode = False

# #     def handle_data(self, data):
# #         try:
# #             self.data = json.loads(data)
# #         except ValueError:
# #             logger.debug('data received: %s', data)
# #             return
# #         message_type = self.data['type']
# #         fn = getattr(self, 'handle_{}'.format(message_type))
# #         if fn is None:
# #             logger.debug('unknown message type: %s', message_type)
# #             return self.send_error_message('Invalid Message Type: {}'.format(message_type))
# #         fn()

# #     def handle_new_user(self):
# #         self.client = Client(self.data['username'], self)
# #         self.server.add_client(self.client)

# #     def handle_user_message(self):
# #         self.server.send_user_message(self.client, self.data['message'])

# #     def send_error_message(self, message):
# #         data = {
# #             'type': 'error',
# #             'message': message,
# #         }
# #         self.send(data)


# # if __name__ == '__main__':
# #     logging.basicConfig(level=logging.DEBUG)
# #     ChatServer(('127.0.0.1', 8000), ChatHandler).serve_forever()



# import asyncio
# import json
# import logging
# import os
# import datetime
# from base64 import b64encode
# from hashlib import sha1
# from typing import Set
# from urllib.parse import urlparse
# import websockets

# HOST = ''
# PORT = 8002
# MAGIC_STRING = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

# client_pool = set()
# ID = 1
# logger = logging.getLogger(__name__)


# class WebSocketHandler:
#     def __init__(self, websocket, path):
#         self.websocket = websocket

#     async def handle(self):
#         async for message in self.websocket:
#             await self.handle_data(message)

#     async def handle_data(self, data):
#         try:
#             self.data = json.loads(data)
#         except ValueError:
#             logger.debug('data received: %s', data)
#             return
#         message_type = self.data['type']
#         fn = getattr(self, 'handle_{}'.format(message_type), None)
#         if fn is None:
#             logger.debug('unknown message type: %s', message_type)
#             return await self.send_error_message('Invalid Message Type: {}'.format(message_type))
#         await fn()

#     async def handle_new_user(self):
#         self.client = Client(self.data['username'], self)
#         self.server.add_client(self.client)

#     async def handle_user_message(self):
#         self.server.send_user_message(self.client, self.data['message'])

#     async def send_error_message(self, message):
#         data = {
#             'type': 'error',
#             'message': message,
#         }
#         await self.send(data)

#     async def send(self, data):
#         await self.websocket.send(json.dumps(data))


# class Client:
#     _ID = 1

#     def __init__(self, username, handler):
#         self.username = username
#         self.connection = handler
#         self.ID = self._ID
#         self._ID += 1


# class ChatServer:
#     index_file = './index.html'  # Class variable

#     def __init__(self):
#         self.clients = set()

#     async def add_client(self, client):
#         self.clients.add(client)
#         await self.send_server_message('{} has joined'.format(client.username))

#     async def send_server_message(self, message):
#         data = {
#             'type': 'notice',
#             'message': message,
#             'datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         }
#         for client in self.clients:
#             await client.connection.send(json.dumps(data))

#     async def send_user_message(self, sent_from, message):
#         data = {
#             'type': 'user_message',
#             'message': message,
#             'username': sent_from.username,
#             'datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         }
#         for client in self.clients:
#             await client.connection.send(json.dumps(data))


# async def websocket_handler(websocket, path):
#     handler = WebSocketHandler(websocket, path)
#     await handler.handle()


# if __name__ == '__main__':
#     logging.basicConfig(level=logging.DEBUG)
#     start_server = websockets.serve(websocket_handler, "localhost", 8000)
#     asyncio.get_event_loop().run_until_complete(start_server)
#     asyncio.get_event_loop().run_forever()



import asyncio
import websockets
import sys

#create two tasks -- one for recieving input from the console and other from the web page


async def console_send(ws):
    while True:
        consoleinput = await asyncio.to_thread(sys.stdin.readline)
        consoleinput.rstrip('\n')
        await asyncio.to_thread(sys.stdout.write, f'{consoleinput} ')
        await ws.send(consoleinput)


async def socket_receive(ws):
    while True:
        message = await ws.recv()
        print(message)
        # print(f'Msg [{message}]')


##TODO: Implement this
# async def socket_send(ws):
# {

# }


#This is an handler which will process, incoming messagess.
async def websocket_handler(ws:str, path:int):
    #This is triggered only when the connection is establish.
    inp = input('Client joined. Greet it. \nType ')
    await ws.send(inp)

    #Create two tasks        
    sendTask = asyncio.create_task(console_send(ws))
    receiveTask = asyncio.create_task(socket_receive(ws))

    await asyncio.gather(sendTask, receiveTask)


    #Have to schedule these events on event loop

async def startServer():
    async with websockets.serve(websocket_handler, "127.0.0.1", 8000):
        await asyncio.Future() #For it to be running forewer.
asyncio.run(startServer())


#Things to do, way to stop the chat and gracefull exit the conversation.


#asyncio.get_event_loop().run_until_complete(Server)
#asyncio.get_event_loop().run_forever()
