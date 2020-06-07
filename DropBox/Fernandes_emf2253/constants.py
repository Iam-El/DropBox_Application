# Name: Elsy Fernandes (1001602253)


# Constants used in the program

import socket

HOST = socket.gethostbyname("localhost")  # get the hostname
PORT = 65045  # Port to listen on (non-privileged ports are > 1023)
ERROR = 'ERROR'  # Error variable having a message 'ERROR'
FILE_RECEIVED = 'FILE_RECEIVED'  # FILE_RECEIVED variable having a message 'FILE_RECEIVED'
ACCEPTED = 'ACCEPTED'  # ACCEPTED variable having a message 'ACCEPTED'
USERNAME = 'USER_NAME'  # USERNAME variable having a message 'USER_NAME'
UPLOADING_FILE = 'UPLOADING_FILE'  # UPLOADING_FILE variable having a message 'UPLOADING_FILE'
ROOT = '/Users/el/Desktop/'  # Set a root directory for the files
FILE_NAME_RECEIVED = "FILE_NAME_RECEIVED"  # FILE_NAME_RECEIVED variable having a message 'FILE_NAME_RECEIVED'
PACKET_SIZE = 1024  # Maximum packet size (file size ) received will be 1024
FILLER = '\x00'  # Filler data is used to make every byte 1024
COMMAND = "Command"  # COMMAND variable having a message 'COMMAND'
MESSAGE = "Message"  # MESSAGE variable having a message 'Message'
SHUTDOWN = "Shutdown"  # SHUTDOWN variable having a message 'Shutdown'
UPLOADING_CHANGED_FILE = "Push"  # Push the file to server
PULL = "Pull"  # pull the file  from the server
INVALIDATE = "Invalidate"  # server invalidate message
BROADCAST = "Broadcast"  # server broad cast message
DELETED = "Deleted" # to delete the file
DELETE = "Delete"  # to delete the file
FETCH = "Fetch"# to fetch the file
VOTING = "Voting" # to vote for the file
VOTING_RESPONSE = "Voting_Response" # voting response
VOTING_RESULT = "Voting_Result" # voting result
COMMIT = "Commit" # commit
ABORT = "Abort" # abort
