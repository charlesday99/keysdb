from keys_client import Keys

def callback(result):
    with open(key + "-snoop.log", 'a+') as f:
        f.write(str(result) + "\n")
    print(result)

key = input("Enter Key to snoop: ")

keysDB = Keys("192.168.0.202", 8080)
keysDB.subscribe(key, callback)
