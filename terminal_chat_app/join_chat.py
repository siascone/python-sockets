from client import Client


name = input('What is your name? ')

new_user = Client(name)
new_user.join()