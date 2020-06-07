# Name: Fernandes Elsy (1001602253)

from constants import *
from tkinter import filedialog
from tkinter import *
import threading
import time
import shutil
import ntpath
import os
import random
from stat import *
from pathlib import Path
from utils import receive, create_save_file, create_button, generate_filler_data, print_file_list


class Client:

    # Initializing all the variables used in the program
    def __init__(self, root, folder_path):
        self.client = None
        self.gui = root
        self.message_panel = root.left_panel
        self.action_panel = root.right_top_panel
        self.form_panel = root.right_bottom_panel
        self.user_name = None
        self.user_name_field = None
        self.file_upload_button = None
        self.file_name = None
        self.directory = ROOT + folder_path + "/"
        self.server_handler = None
        self.files_mt_times = {}
        self.file_watcher = None

    #  Function to bind to server socket
    def start(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Sets up the socket
        self.client.connect((HOST, PORT))  # Client is connted to the server
        self.show_user_name_field("Enter your username")  # Enter username in the username field
        self.server_handler = threading.Thread(target=self.listen_to_server)  # Start the multi-threading in the client
        self.server_handler.start()
        self.file_watcher = threading.Thread(target=self.file_watch_handler)
        self.file_watcher.start()

    # Function to disconnect the client
    def stop(self):
        if self.client:
            self.print_it(self.user_name + ": Disconnecting from Server")
            self.client.shutdown(socket.SHUT_RDWR)
            self.client.close()
        self.client = None

    # Function to display the username field
    # When the client gives the wrong username it destroy the previous username widget

    def show_user_name_field(self, message):
        self.destroy_widgets()
        Label(self.form_panel, text=message, bg="#B00020", foreground="#ffffff").pack()
        self.user_name_field = Entry(self.form_panel)
        self.user_name_field.pack()
        create_button(self.form_panel, "Send", self.user_name_field_handler).pack()

    # Function to remove the username field if the client has successfully connected
    def remove_user_name_field(self):
        self.user_name_field.delete(0, END)

    # Function to send the message to server
    def send_to_server(self, value):
        print("Message to server: " + value)
        self.client.sendall((value + generate_filler_data(value)).encode())

    # Function to send the messages to server without encoding
    def send_to_server_no_encode(self, value):
        self.client.sendall(value)

    # Function to send the entered username to the server

    def user_name_field_handler(self):
        self.user_name = self.user_name_field.get()
        self.send_to_server(USERNAME)
        self.send_to_server(self.user_name)

    # Function to remove the old widgets and update to new

    def destroy_widgets(self):
        for widget in self.form_panel.winfo_children():
            widget.destroy()

    # After destroying the widget , show a new file dialog

    def show_file_dialog(self):
        self.destroy_widgets()
        create_button(self.form_panel, "Upload file", self.file_upload_handler).pack()

    # Open the file you want to upload (It can upload any type of files)
    # Copy the file name selected to the required client directory
    # Notify the server that file is uploaded to the client through socket
    # Sends the file that is in client directory to server through socket

    def file_upload_handler(self):
        print("file_upload_handler")
        self.file_name = filedialog.askopenfilename(initialdir="/", title="Select file")

        if self.file_name:
            shutil.copy(self.file_name, self.directory)  # copy the file to the client directory
            self.print_file_list()  # print the list of files in right side of panel
            filename = ntpath.basename(self.file_name)  # separate out filename from a directory

            file = self.directory + '/' + filename  # append the filenane to the directory(client)
            self.send_to_server(UPLOADING_FILE)  # Sending uploading file message to server
            self.print_it("Uploading file to server: " + filename)
            self.send_to_server(filename)  # send the filename to the server
            self.send_file_to_server(file)
            self.files_mt_times[filename] = self.get_mtime(filename)

    # Function to print the message on GUI
    def print_it(self, message):
        self.gui.print_on_gui(message)

    # Function to receive a file from the server after server broadcast the file
    def receive_file(self):
        file_name = receive(self.client)
        print(file_name)
        file_location = self.directory + file_name
        create_save_file(file_location, self.client)
        self.files_mt_times[file_name] = self.get_mtime(file_name)

        self.print_file_list()

    # Function yto list the file list on the right side of the panel

    def print_file_list(self):
        print_file_list(self.directory, self.gui.print_files, self.gui.file_list_panel,
                        "Files in " + self.user_name + " Directory:")

    # Listen to the server for the various commands
    # if the server sends the error message for the username it prints on the right gui
    # if the username is accepted ,remove the username field and show the file dialogue
    # If the 'UPLOADING_FILE' command is received then receive a file
    # Stop the client of 'SHUTDOWN' Command is received
    def listen_to_server(self):
        while self.client:
            command = receive(self.client)
            print("Command from Server: " + command)
            if command == ERROR:
                self.remove_user_name_field()
                self.show_user_name_field("Username exists. Enter another username")
            elif command == ACCEPTED:
                self.print_it(self.user_name + ": is Connected to the server")
                self.print_file_list()
                self.remove_user_name_field()
                self.show_file_dialog()
            elif command == UPLOADING_FILE:
                self.receive_file()
            elif command == INVALIDATE:
                file_name = receive(self.client)
                self.print_it("Server Invalidation " + file_name)
                self.send_to_server(PULL)
                self.send_to_server(file_name)
                self.print_it("Client pulling " + file_name)
            elif command == VOTING:
                file_name = receive(self.client)
                print("Server has started the voting", file_name)
                time.sleep(3)
                option = random.choice([True, False])
                if option:
                    self.print_it("Voting For Deleting: \n" + file_name)
                    self.print_it("My Vote: " + COMMIT)
                else:
                    self.print_it("Voting For Deleting: \n" + file_name)
                    self.print_it("My Vote:" + ABORT)
                self.send_to_server(VOTING_RESPONSE)
                self.send_to_server(file_name)
                self.send_to_server(COMMIT if option else ABORT)
            elif command == DELETE:
                file_name = receive(self.client)
                self.print_it("Deleting: " + file_name)
                os.remove(self.directory + file_name)
                del self.files_mt_times[file_name]
                self.print_it("Deleted: " + file_name)
                self.print_file_list()
            elif command == VOTING_RESULT:
                decision = receive(self.client)
                file_name = receive(self.client)
                self.print_it("Vote for: " + file_name)
                self.print_it("Vote Result: " + decision)
                if decision == COMMIT:
                    self.send_to_server(DELETE)
                    self.send_to_server(file_name)
                    self.print_it("Deleted file Committed")
                else:
                    self.send_to_server(FETCH)
                    self.send_to_server(file_name)
                    self.print_it("Deleted file Restored")
            elif command == SHUTDOWN:
                self.stop()
            time.sleep(0.01)

    # file watch handler checks the file in the directory
    # if its found once made the changes to the file
    # client pushes the file to the server by sending push command

    def file_watch_handler(self):
        while True:
            time.sleep(5)
            file_times_dictionary = self.files_mt_times
            for filename in list(file_times_dictionary):
                if os.path.isfile(self.directory + filename):
                    try:
                        mtime = os.path.getmtime(self.directory + filename)
                        if mtime != file_times_dictionary[filename]:
                            self.print_it("Pushing " + filename)
                            self.send_to_server(UPLOADING_CHANGED_FILE)
                            self.send_to_server(filename)
                            self.send_file_to_server(self.directory + filename)
                            file_times_dictionary[filename] = mtime
                    except FileNotFoundError:
                        print("exception")
                else:
                    self.print_file_list()
                    self.print_it("Acting as Coordinator:")
                    self.send_to_server(DELETED)
                    self.send_to_server(filename)
                    del self.files_mt_times[filename]

    def get_mtime(self, filename):
        path = self.directory + filename
        return os.path.getmtime(path)

    def send_file_to_server(self, file):
        with open(file, "r+b") as f:  # open the filename
            file_content = f.read(1024)  # read file content
            while file_content:
                self.send_to_server_no_encode(file_content)  # send the file content to server
                file_content = f.read(1024)
            f.close()
            print("File uploaded to server")
