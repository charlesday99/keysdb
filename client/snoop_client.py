from keys_client import Keys

def callback(result):
    with open(key + "-snoop.log", 'a+') as f:
        f.write(str(result) + "\n")
    print(result)

server = input("Is the server local, pi or cloud? ")

if server[0] == "l":
    keysDB = Keys("localhost", 80)
elif server[0] == "p":
    keysDB = Keys("192.168.0.202", 8080)
else:
    keysDB = Keys("db.charlieday.dev", "https")

key = input("Enter Key to snoop: ")
keysDB.subscribe(key, callback)
