from threading import Thread
import sqlite3
import socket
import queue


# Global Variables
MAX_LENGTH = 1000


class KeysDB:

    def __init__(self, file_path):
        # Connect to local database
        self.conn = sqlite3.connect(file_path, check_same_thread=False)
        cursor = self.conn.cursor()

        # Checks if the table exists and creates one if needed
        if cursor.execute('SELECT tbl_name FROM "main".sqlite_master;').fetchone() == None:
            cursor.execute('CREATE TABLE "Strings" ("key" TEXT NOT NULL UNIQUE,"value" TEXT, PRIMARY KEY("key"));')
            print("Created new database at '{}',".format(file_path))

        # Commit & close database connection
        self.conn.commit()
        print("Loaded Database.")

        # Create recieving socket
        s = socket.socket()
        s.bind(('', 4000))
        s.listen(5)

        # Start connections server
        self.threads = []
        server_thread = Thread(target=self.connectionsServer,args=(s,)).start()
        print("Started connections server...")


    def setValue(self, key, value): #POST, PUT
        cursor = self.conn.cursor()

        if self.hasKey(key):
            cursor.execute("UPDATE Strings SET value = ? WHERE key = ?", (value,key))
        else:
            cursor.execute("INSERT INTO Strings VALUES (?,?)",(key,value))

        self.updateNotification(key, value)
        self.conn.commit()

        return key,value


    def getValue(self, key): #GET
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Strings WHERE key = ?;",(key,))
        
        return cursor.fetchone()


    def deleteKey(self, key): #DELETE
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM Strings WHERE key = ?;",(key,))
        result = cursor.fetchone()

        self.conn.commit()
        return key


    def hasKey(self, key):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Strings WHERE key = ?;",(key,))

        result = cursor.fetchone()

        if result == None:
            return False
        else:
            return True


    def dump(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Strings;")
        return cursor.fetchall()


    def getConnections(self):
        return self.threads


    def updateNotification(self, key, value):
        for thread in self.threads:
            thread.processKey(key, value)


    def connectionsServer(self, s):
        while True:
            conn, addr = s.accept()
            print('Got connection from', addr)

            t = SubscriberThread(conn, self.threads)
            t.start()
            self.threads.append(t)

    def __exit__(self):
        self.conn.close()


class SubscriberThread(Thread):
    def __init__(self, conn, threads):
        Thread.__init__(self)
        self.conn = conn
        self.queue = queue.Queue()
        self.threads = threads
        self.key = "default"

    def processKey(self, key, value):
        if key == self.key:
            self.queue.put(value)

    def run(self):
        self.key = self.conn.recv(1024).decode("utf-8")
        print("Client subscribed too:", self.key)

        while True:
            value = self.queue.get()

            try:
                self.conn.sendall(str.encode(value))
            except:
                print("Client closed connection.")
                self.conn.close
                self.threads.remove(self)
                self._is_running = False
                break
