from http import client
from socketio import AsyncClient
import asyncio
from json import dumps
from aioconsole import ainput

if __name__ == '__main__':
    IP = '172.17.156.51'
    PORT = '8080'

    clientName = 'Alice'
    roomName = 'Home'
    messageToSend = ''

    sio = AsyncClient()
    FullIp = 'http://'+IP+':'+PORT

    @sio.event
    async def connect():
        print('Connected to server')
        await sio.emit('join_chat', {'room': roomName, 'name': clientName})

    @sio.event
    async def get_message(message):
        if clientName == message['from']:
            print('You: ' + message['message'])
        else:
            print(message['from']+' : '+message['message'])

    async def send_message():
        while True:
            await asyncio.sleep(0.01)
            messageToSend = await ainput()
            await sio.emit('send_chat_room', {'message': messageToSend, 'name': clientName, 'room': roomName})

    async def connectToServer():
        await sio.connect(FullIp)
        await sio.wait()

    async def main(IP):
        await asyncio.gather(
            connectToServer(),
            send_message()
        )
    
loop = asyncio.get_event_loop()
loop.run_until_complete(main(FullIp))
