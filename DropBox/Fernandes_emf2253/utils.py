# Name: Elsy Fernandes(1001602253)

# Utils.py has all the common functions that are used both in client as well as server

from constants import *
from tkinter import Button
import os


# This function is used to make every byte 1024 when the packet is received by the server or the client

def generate_filler_data(message):
    return FILLER * max(PACKET_SIZE - len(message), 0)

# Common function used in client and server in order to send the encoded messages

def send(socket_to_send, message):
    socket_to_send.sendall((message + generate_filler_data(message)).encode())

# Common function used in client and server in order to send the  messages without encoding

def send_no_encode(socket_to_send, message):
    socket_to_send.sendall(message)

# Common function used in client and server in order to get the socket address to be displayed on GUI

def get_socket_address_string(socket_to_send):
    return str(socket_to_send.getsockname())

# Common function used in client and server in order to recieve the messages sent to each other and decode the messages

def receive(socket_to_receive):
    data = socket_to_receive.recv(1024).decode().rstrip('\x00')
    return data

# Common function used in client and server in order to recieve the messages sent to each other without decode

def receive_no_encode(socket_to_receive):
    data = socket_to_receive.recv(1024)
    return data

# Common function used in client and server in order to receive the file content


def create_save_file(location, socket_to_receive):
    with open(location, "wb") as f:     # Open the file in write mode
        file_data = receive_no_encode(socket_to_receive)  # received the file content
        while file_data:
            f.write(file_data)                       # Write the file-content to the file
            if len(file_data) < 1024:                # To find the end of file
                file_data = None                     # File data is now empty and exits from the file loop
            else:
                file_data = receive_no_encode(socket_to_receive) # Else it will keep receiving the content and writes it
        f.close()

# Common button to used in both server and client GUI

def create_button(gui, text, handler):
    return Button(gui, text=text, command=handler, highlightbackground="#000000",
                  disabledforeground="#000000",
                  background="#000000",
                  activebackground="#000000",
                  foreground="#FFFFFF", padx="20", pady="10")

# List the files in GUI from client and server folder

def print_file_list(directory, print_method, panel, message):
    for widget in panel.winfo_children():
        widget.destroy()

    print_method(message)
    for file in os.listdir(directory):
        print_method(file)


def print_client_list(clients, print_method, panel, message):
    for widget in panel.winfo_children():
        widget.destroy()

    print_method(message)
    for client in clients:
        print_method(client)
