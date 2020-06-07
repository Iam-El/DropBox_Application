# Name: Elsy Fernandes(1001602253)

# Client GUI

from tkinter import *
import threading
from socket_client import Client
from utils import create_button
import sys

root = Tk()
root.title("Client")

# Label for the Client gui
label = Label(root, text="Client", bg="#B00020", foreground="#ffffff", padx=225)
label.pack()

# Left panel for the Client GUI
root.left_panel = Frame(root, borderwidth=1, relief="solid", height=500, width=300)
root.left_panel.pack_propagate(0)
root.left_panel.pack(side="left", expand=True, fill="both")

# Right panel for the Client GUI
root.right_panel = Frame(root, borderwidth=1, relief="solid", height=500, width=200, bg="#B00020")

root.right_top_panel = Frame(root.right_panel, relief="solid", height=200, width=200, bg="#B00020")

root.right_bottom_panel = Frame(root.right_panel, relief="solid", height=300, width=200, bg="#B00020")
root.right_bottom_panel.pack_propagate(0)
root.right_bottom_panel.pack(side="bottom", expand=True, fill="x")

# File list panel for the Client GUI

file_list_panel = Frame(root, borderwidth=1, relief="solid", height=500, width=300)
Label(file_list_panel, text="File List:", anchor="w", width=300).pack()
file_list_panel.pack_propagate(0)
file_list_panel.pack(side="right", expand=True, fill="both")

print(sys.argv)
c1 = Client(root, sys.argv[1])


# Function to connect client
def connect_client():
    client = threading.Thread(target=c1.start)
    client.daemon = True
    client.start()


# Function to disconnect client
def disconnect_client():
    c1.stop()


# Function to print the content on GUI
def print_on_gui(message):
    Label(root.left_panel, text=message, anchor="w", width=300).pack()

# Function to print the file list on the left side of the panel
def print_to_file_list_panel(message):
    Label(file_list_panel, text=message, anchor="w", width=300).pack()


root.print_on_gui = print_on_gui
root.print_files = print_to_file_list_panel

root.file_list_panel = file_list_panel

# Connect Disconnect buttons used for client GUI

greet_button = create_button(root.right_top_panel, "Connect", connect_client)  # Call connect_client function when connect button is clicked
greet_button.pack(padx=10, pady=30)
close_button = create_button(root.right_top_panel, "Disconnect", disconnect_client)  # Call disconnect_client function when Disconnect button is clicked
close_button.pack()
root.right_top_panel.pack(side="top", expand=True, fill="x")

root.right_panel.pack_propagate(0)
root.right_panel.pack(side="right", expand=True, fill="both")

root.mainloop()
