# Elsy Fernandes (1001602253)

from constants import *
import threading
from utils import send, send_no_encode, get_socket_address_string, receive, create_save_file, print_file_list, \
    print_client_list
import os


class Server:

    # Initializing the variables those are used in the program

    def __init__(self, root):
        self.server_socket = None
        self.gui = root
        self.connections = []
        self.users = []
        self.directory = ROOT + 'Server/'
        self.votes = {}

    # Function to start the server and listen to any client connections available
    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a socket
        self.server_socket.bind((HOST, PORT))  # bind the socket with host and port
        print_file_list(self.directory, self.gui.print_files, self.gui.file_list_panel,
                        "Files in Server:")  # print the files on the right side of panel
        self.server_socket.listen()  # server listening to the client
        self.listen_for_connections()

    # Function to stop the server when server stops client will automatically shuts down

    def stop(self):
        for client in self.connections:
            send(client, SHUTDOWN)
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None

    # Function to print on the left panel of gui

    def print_on_left_gui(self, command, client_name, message):
        self.gui.print_left(command + "(" + client_name + "):" + message)

    # Function to Listen to connections and implemented multi-threading to handle multiple clients

    def listen_for_connections(self):
        while self.server_socket:
            (client_socket, address) = self.server_socket.accept()
            client_handler = threading.Thread(target=self.handle_client_connection, args=[client_socket, address])
            self.connections.append(client_socket)
            client_handler.start()

    # Function to broadcast the file to all the clients that are actively listening to the server

    def broadcast_to_all_clients(self, file_name):
        for client_socket in self.connections:
            self.send_file_to_clients(client_socket, file_name)

    # Function to send the filename and file to the server those are actively listening

    def invalidate_clients(self, file_name, current_client_socket):
        for client_socket in self.connections:
            if client_socket != current_client_socket:
                send(client_socket, INVALIDATE)
                send(client_socket, file_name)

    def send_file_to_clients(self, client_socket, file_name):
        file = self.directory + '/' + file_name
        send(client_socket, UPLOADING_FILE)
        send(client_socket, file_name)

        with open(file, "r+b") as f:
            file_content = f.read(1024)
            while file_content:
                send_no_encode(client_socket, file_content)
                file_content = f.read(1024)
            f.close()
            print("File uploaded at the client client")

    # Function to handle the client connection
    # Handles the username (if username exist sends the error message else prints the username)
    # printing of the error message and username is handled in the left gui
    # Receives the file from client and put it in its server directory
    # Once the file in the server directory it sends the file to all the clients those are still connected and listening
    # once the changed file has been noted in the server
    # server sends the invalidation message to remaining clients
    # server sends the updated file to the remaining clients

    def handle_client_connection(self, client_socket, address):
        user_name = get_socket_address_string(client_socket)  # get socket address string to display on the panel
        while client_socket:
            command = receive(client_socket)  # receive a command from the client
            self.print_on_left_gui(COMMAND, user_name, command)  # print the commands on the left side of gui
            if command == USERNAME:
                user_name = receive(client_socket)  # if the recieved command is 'USERNAME'
                if self.check_if_user_exists(user_name):  # checks if the username exist
                    client_socket.send(ERROR.encode())  # if username is already present the sends out the error
                else:
                    self.users.append(user_name)  # appends the username to the user_name list
                    self.print_on_left_gui(MESSAGE, user_name, "Connected")  # username message displayed on gui
                    client_socket.send(ACCEPTED.encode())  # sends the message to the server saying username is accepted
                    print_client_list(self.users, self.gui.print_clients, self.gui.client_list_panel,
                                      "Connected Clients")

            elif command == UPLOADING_FILE:
                self.receive_file(client_socket, user_name, "Uploaded",
                                  BROADCAST)  # sending the updated file to other clients
            elif command == DELETED: #if command isdeleted
                file_name = receive(client_socket)
                self.start_voting(client_socket, file_name)
            elif command == VOTING_RESPONSE:
                file_name = receive(client_socket)
                option = receive(client_socket)
                print(command, file_name, option)
                self.votes[file_name][client_socket] = option
                print(self.votes)
                current_file_voting = self.votes[file_name].values()
                if None not in current_file_voting:
                    currently_voted_clients = self.votes[file_name].keys()
                    client_started_deletion = list(set(self.connections) - set(currently_voted_clients))[0]
                    if len(set(current_file_voting)) == 1 and COMMIT in current_file_voting:
                        send(client_started_deletion, VOTING_RESULT) #checks for the voting result
                        send(client_started_deletion, COMMIT) #if the client commits
                        send(client_started_deletion, file_name)
                    else:
                        send(client_started_deletion, VOTING_RESULT) #checks for the voting result
                        send(client_started_deletion, ABORT) #if the client aborts
                        send(client_started_deletion, file_name)
            elif command == DELETE:
                file_name = receive(client_socket)
                self.print_on_left_gui(MESSAGE, user_name,
                                       "Deleting " + file_name)
                os.remove(self.directory + file_name)
                print_file_list(self.directory, self.gui.print_files, self.gui.file_list_panel,
                                "Files in Server:")  # print the files on the right side of panel
                self.delete_file_from_all_clients(file_name)
            elif command == FETCH:
                file_name = receive(client_socket)
                self.send_file_to_clients(client_socket, file_name)
            elif command == UPLOADING_CHANGED_FILE:
                self.receive_file(client_socket, user_name, "Updated",
                                  INVALIDATE)  # sending invalidate message to clients
            elif command == PULL:
                file_name = receive(client_socket)
                self.print_on_left_gui(MESSAGE, user_name,
                                       "Pulling " + file_name)  # once the pull command is printed it sends the file to other clientsSe
                self.send_file_to_clients(client_socket, file_name)
            elif command == "":
                self.print_on_left_gui(MESSAGE, user_name, "Disconnected ")  # if the recieved command is ''
                if client_socket in self.connections:
                    self.connections.remove(client_socket)  # remove the connections from list
                if user_name in self.users:
                    self.users.remove(user_name)  # remove username from the list
                    print_client_list(self.users, self.gui.print_clients, self.gui.client_list_panel,
                                      "Connected Clients")
                client_socket = None

    # Function to check if the username exist

    def check_if_user_exists(self, user_name):
        return user_name in self.users

    def receive_file(self, client_socket, user_name, text, command):
        file_name = receive(client_socket)  # if the received command is 'UPLOADING_FILE'
        server_location = self.directory + file_name
        if file_name:
            create_save_file(server_location, client_socket)  # puts the recieved file in the server location
        self.print_on_left_gui(MESSAGE, user_name, text + " " + file_name)  # print the message on gui
        if command == BROADCAST:
            self.broadcast_to_all_clients(file_name)  # calls broadcast function
        else:
            self.invalidate_clients(file_name, client_socket)
        print_file_list(self.directory, self.gui.print_files, self.gui.file_list_panel,
                        "Files in Server:")  # print the message on gui

# function to let the server to send the messages to cliets and let the clients start voting
    def start_voting(self, client_socket_coordinator, file_name):
        print("came to start voting")
        self.votes[file_name] = {}
        print("came to start voting")
        for client_socket in self.connections:
            if client_socket != client_socket_coordinator:
                self.votes[file_name][client_socket] = None
                send(client_socket, VOTING)
                send(client_socket, file_name)
# delete all the files from the client when you recieve the commit message from all the clients.
    def delete_file_from_all_clients(self, file_name):
        for client_socket in self.connections:
            send(client_socket, DELETE)
            send(client_socket, file_name)
