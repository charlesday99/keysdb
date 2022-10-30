from keys_client import Keys

def callback(result):
    print(result)

keysDB = Keys("keys.iterator.me", web_port=443)
    
room = input("Enter the room name: ")
username = input("Enter your username: ")

t = keysDB.subscribe(room,callback)
keysDB.set(room, username + " has connected!")

while True:
    try:
        keysDB.set(room, username + ": " + input())
    except:
        print("Connection error! Ending chat.")
        t.stop()
        break

