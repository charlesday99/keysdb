from keys_client import Keys

def callback(result):
    print(result)

server = input("Is the server local, pi or cloud? ")

if server[0] == "l":
    keysDB = Keys("localhost", 80)
elif server[0] == "p":
    keysDB = Keys("192.168.0.202", 8080)
else:
    keysDB = Keys("db.charlieday.dev", "https")
    
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

