from keys_client import Keys

def callback(result):
    with open(key + "-stream.log", 'a+') as f:
        f.write(str(result) + "\n")
    print(result)

server = input("Is the server local or remote? ")

if server[0] == "l":
    keysDB = Keys("localhost", 80)
else:
    keysDB = Keys("192.168.0.202", 8080)

key = input("Enter Key to stream: ")
keysDB.subscribe(key, callback)
