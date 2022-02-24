from xmlrpc import client
from socketio import AsyncClient
from aioconsole import ainput
from json import dumps
import asyncio


class Client:
    def __init__(self, name):
        self.name = name

    def join(self):
        # if __name__ == '__main__':
        IP = '0.0.0.0'
        PORT = '8080'

        clientName = self.name
        roomName = 'main'
        messageToSend = ''

        sio = AsyncClient()
        FullIp = 'http://'+IP+':'+PORT

        @sio.event
        async def connect():
            print('Connected to ChatBot')
            await sio.emit('join_chat', {'room': roomName, 'name': clientName})

        @sio.event
        async def get_message(message):
            if clientName != message['name']:
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
