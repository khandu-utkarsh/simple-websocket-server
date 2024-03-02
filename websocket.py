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


if __name__ == '__main__':
    asyncio.run(startServer())


#TODO: Things to do, way to stop the chat and gracefull exit the conversation.