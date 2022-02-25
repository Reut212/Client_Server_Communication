from _thread import start_new_thread
# import socket module
from socket import *
import sys  # In order to terminate the program

num_of_threads = 0

# client's Port: user's name
names = {55000: str, 55001: str, 55002: str, 55003: str, 55004: str, 55005: str,
         55006: str, 55007: str, 55008: str,  55009: str, 55010: str, 55011: str,
         55012: str, 55013: str, 55014: str, 55015: str}

# name: [ip, port, connection, [msg1, msg2,..]]
users = {}


# connect to chat! In this point we already have a connection to the server
def connect(name, port, ip):
    if name not in users:
        names[port] = name
        users[name] = [ip, port, connectionSocket, str]
        connectionSocket.send('<connected>'.encode())
        print(name + " connected")
    else:
        connectionSocket.send('<available_name>'.encode())


# message_send- is the massage according to protocol
# online_users_print- will display on the screen
def get_users():
    online_users_print = ""
    online_users_send = ""
    for key, val in users.items():
        if val[2] != 0:
            online_users_print = online_users_print + str(key) + ","
            online_users_send = online_users_send + "<" + str(key) + ">"

    print("online users: " + online_users_print[0:-1])
    message_send = "<users_lst><" + str(num_of_threads) + ">" + str(online_users_send) + "<end>"
    connectionSocket.send(message_send.encode())


# we need to free the port
def disconnect(port):
    name = names[port]
    users.pop(names[port])
    # del users[names[port]]
    names[port] = str
    connectionSocket.send("<disconnected>".encode())
    print(name + ' left chat')


def set_msg(rest_of_msg, port, ip):
    # rest_of_msg="name><msg>"
    index = rest_of_msg.find(">")
    name = rest_of_msg[0:index - 1]
    msg = rest_of_msg[index + 2:-1]
    if name in users:
        other_client_socket = users[name][2]
        my_name = names[port]
        send_to_client = "<" + str(my_name) + "><" + str(msg) + ">"
        other_client_socket.send(send_to_client.encode())
        users[name][3] += "," + msg
        connectionSocket.send("<msg_sent>".encode())
    else:
        connectionSocket.send("<invalid_name>".encode())


def set_msg_all(msg, port):
    # msg = "msg>"
    my_name = names[port]
    for key, val in users.items():
        if key is not my_name:
            other_client_socket = users[key][2]
            other_client_socket.send(msg.encode())
    connectionSocket.send("<msg_sent>".encode())


def get_list_file():
    return "h"


def download():
    return "h"


def proceed():
    return "h"


def actions(action, rest_of_msg, port, ip):
    if action == "connect":
        connect(rest_of_msg, port, ip)
    elif action == "get_users":
        get_users()
    elif action == "disconnect":
        disconnect(port)
    elif action == "set_msg":
        set_msg(rest_of_msg, port, ip)
    elif action == "set_msg_all":
        set_msg_all(rest_of_msg, port)
    elif action == "get_list_file":
        get_list_file()
    elif action == "download":
        download()
    elif action == "proceed":
        proceed()
    else:
        return "Invalid action"


# Given server port
serverPort = 50000
# choosing type of protocol
# af_inet- Ivp4
# SOCK_STREAM = TCP
serverSocket = socket(AF_INET, SOCK_STREAM)

# bind socket to a specific address and port
# '' means listen to all ip's
serverSocket.bind(('', serverPort))

# define at least 5 connections
serverSocket.listen(5)

print("Ready to serve!")


# this function is executed whenever a thread is being activated
def multi_threaded_client(connectionSocket):
    while True:
        # receiving other messages
        message = connectionSocket.recv(1024).decode()
        index = message.find(">")
        action = message[1:index]
        # sending to a switch case action and other relevant info
        actions(action, message[index + 2:-1], addr[1], addr[0])
        if action == "disconnect":
            break
    connectionSocket.close()


while True:
    # connectionSocket is the socket after the connection has been accepted
    # addr[0]= client's ip, addr[1]= client's port
    connectionSocket, addr = serverSocket.accept()
    connectionSocket.send("<connection_established>".encode())
    start_new_thread(multi_threaded_client, (connectionSocket,))
    num_of_threads += 1
