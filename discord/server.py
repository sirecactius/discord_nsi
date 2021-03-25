from sql_interactions import *
import socket, os, select, sys

port = 5050
HEADER_LENGTH = 10

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

ip = socket.gethostbyname(socket.gethostname())

server.bind((ip, port))
server.listen()

sockets_list = [server]

clients = {}

print(f'Listening dor connection on {ip}:{port}...')

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:
        return False

def scan(message):
    print('scan in progress')
    print(message['data'][:3])
    #if login:
    if message['data'][:3] == b'000':
        print('login detected')
        message['data'] = message['data'][3:]
        for i in range(len(message['data'])):
            if message['data'][i] == 194:
                if message['data'][i+1] == 164:
                    pseudo = message['data'][:i]
                    password = message['data'][i+2:]
        login = loginSQL(pseudo, password)
        print(login)
    
    #if signup:
    elif message['data'][:3] == b'001':
        print('sign up detected')
        message['data'] = message['data'][3:]
        print(message['data'])
        for i in range(len(message['data'])):
            print(message['data'][i])
            if message['data'][i] == 194:
                if message['data'][i+1] == 164:
                    pseudo = message['data'][:i]
                    password = message['data'][i+2:]
        signup = signupSQL(pseudo, password)
        print(signup)






while 1:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server:
            client_socket, client_address = server.accept()
            user = receive_message(client_socket)
            if user is False:
                continue

            sockets_list.append(client_socket)
            clients[client_socket] = user
            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))

        else:
            message = receive_message(notified_socket)
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            scan(message)
            user = clients[notified_socket]
            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]