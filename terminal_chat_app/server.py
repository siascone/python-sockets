import asyncio
from aiohttp import web
import socketio
from json import dumps

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)

@sio.event
async def join_chat(sid, message):
    username = message.get('name', sid)
    print(username + ' joined the chat')
    sio.enter_room(sid, message['room'])
    user_joined = username + ' has joined the chat'
    await sio.emit('get_message', {'message': user_joined, 'from': 'ChatBot', 'name': username})

@sio.event
async def exit_chat(sid, message):
    sio.leave_room(sid, message['room'])

@sio.event
async def send_chat_room(sid, message):
    await sio.emit('get_message', {'message': message['message'], 'from': message['name'], 'name': ''}, room=message['room'])

@sio.event
async def connect(sid, environ):
    await sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)

@sio.event
def disconnect(sid):
    print('Client disconnected')

@sio.event
async def get_message(message):
    print(message['from']+' : '+message['message'])

if __name__ == '__main__':
    web.run_app(app)