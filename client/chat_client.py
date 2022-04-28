from keys_client import Keys

def callback(result):
    print(result)

if "c" in input("Is the server local or cloud? "):
    keysDB = Keys("178.62.83.212", 8080)
else:
    keysDB = Keys("localhost", 80)

room = input("Enter the room name: ")
username = input("Enter your username: ")

keysDB.subscribe(room,callback)
keysDB.set(room, username + " has connected!")

while True:
    keysDB.set(room, username + ": " + input())
