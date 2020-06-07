# Name: Elsy Fernandes(1001602253)

# Server GUI

from tkinter import *
import threading
from socket_server import Server
from utils import create_button

root = Tk()
root.title("Server")

# Label on Server GUI

label = Label(root, text="Server", bg="#B00020", foreground="#ffffff", padx=225)
label.pack()

# Left panel for the Server GUI

left_panel = Frame(root, borderwidth=1, relief="solid", height=500, width=300)
left_panel.pack_propagate(0)
left_panel.pack(side="left", expand=True, fill="both")

file_list_panel = Frame(root, borderwidth=1, relief="solid", height=500, width=300)
Label(file_list_panel, text="File List:", anchor="w", width=300).pack()
file_list_panel.pack_propagate(0)

client_list_panel = Frame(root, borderwidth=1, relief="solid", height=500, width=300)
Label(client_list_panel, text="Client List", anchor="w", width=300).pack()
client_list_panel.pack_propagate(0)

file_list_panel.pack(side="right", expand=True, fill="both")
client_list_panel.pack(side="right", expand=True, fill="both")

# Right panel for the Server GUI

right_panel = Frame(root, borderwidth=1, relief="solid", height=500, width=200, bg="#B00020")
right_panel.pack_propagate(0)

s1 = Server(root)


# Function to start server
# In order to keep the GUI running even after the file transfer to the server implemented a GUI threading

def run_server():
    server = threading.Thread(target=s1.start)
    server.daemon = True
    server.start()
    print_to_left_panel("Started Server")


# Function to stop server

def stop_server():
    s1.stop()


# Function to clear messages

def clear_messages():
    for widget in left_panel.winfo_children():
        widget.destroy()


# Function to print on left panel

def print_to_left_panel(message):
    Label(left_panel, text=message, anchor="w", width=300).pack()

# Function to list the files on Server GUI

def print_to_file_list_panel(message):
    Label(file_list_panel, text=message, anchor="w", width=300).pack()


def print_to_client_list_panel(message):
    Label(client_list_panel, text=message, anchor="w", width=300).pack()


root.print_left = print_to_left_panel
root.print_files = print_to_file_list_panel
root.print_clients = print_to_client_list_panel

# printing the client list
root.file_list_panel = file_list_panel
root.client_list_panel = client_list_panel


# Start/ stop buttons used for client GUI

greet_button = create_button(right_panel, "Start Server", run_server)   # Call start_server function when start button is clicked
greet_button.pack(padx=10, pady=10)

close_button = create_button(right_panel, "Stop Server", stop_server)  # Call stop_server function when stop button is clicked
close_button.pack()

clear_messages_button = create_button(right_panel, "Clear Messages", clear_messages) # Clear all the messages function clear_messages is called
clear_messages_button.pack()

right_panel.pack(side="right", expand=True, fill="both")

root.mainloop()
