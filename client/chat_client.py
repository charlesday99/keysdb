from keys_client import Keys

def callback(result):
    print(result)

keysDB = Keys("192.168.0.202", 8080)

room = input("Enter the room name: ")
username = input("Enter your username: ")

keysDB.subscribe(room,callback)
keysDB.set(room, username + " has connected!")

while True:
    keysDB.set(room, username + ": " + input())
