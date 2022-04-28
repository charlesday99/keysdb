from multiprocessing import connection
from threading import Thread
import requests
import socket
import json
import time

class Keys():

    streams = {}

    def __init__(self, host, web_port=80, sub_port=4000):
        self.host = host
        self.subscribe_port = sub_port
        self.base_url = "http://{}:{}/key/".format(host, web_port)
        
    def get(self, key):
        response = requests.get(self.base_url + key)
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()['value']

    def delete(self, key):
        response = requests.delete(self.base_url + key)
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()['status']

    def set(self, key, value):
        payload = {'value': value}
        headers = {'content-type': 'application/json'}
        response = requests.post(self.base_url + key, data=json.dumps(payload), headers=headers)
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()['status']

    def hasKey(self, key):
        response = requests.get(self.base_url + key)
        if response.status_code != 200:
            if response.status_code == 404:
                return False
            else:
                raise Exception(response.text)
        else:
            return True

    def subscribe(self, key, callback):
        if key in self.streams:
            self.streams[key].addCallback(callback)
        else:
            t = SubscriberThread(key,self.host,self.subscribe_port,callback)
            t.start()
            self.streams[key] = t

    def unsubscribe(self, key, callback):
        if key in self.streams:
            self.streams[key].removeCallback(callback)

            if len(self.streams[key].getCallbacks()) == 0:
                self.streams[key].stop()
                del self.streams[key]
        else:
            raise KeyError("Key was not found current subscribe streams.")
        
        
class SubscriberThread(Thread):
    def __init__(self,key,host,port,callback):
        Thread.__init__(self)
        self.key = key
        self.host = host
        self.port = port
        self.callbacks = [callback]
        self.running = True

    def addCallback(self, callback):
        self.callbacks.append(callback)

    def removeCallback(self, callback):
        for current_callback in self.callbacks:
            if current_callback is callback:
                self.callbacks.remove(callback)

    def getCallbacks(self):
        return self.callbacks
        
    def run(self):
        while self.running:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                s.connect((self.host, self.port))
            except:
                print("Failed to connect, sleeping for 10 secs...")
                time.sleep(10)
                continue
            
            self.connected = True
            s.sendall(str.encode(self.key))

            while self.connected:
                try:
                    data = s.recv(1024).decode("utf-8")

                    for callback in self.callbacks:
                        callback(data)
                except:
                    self.connected = False

        s.close()

    def stop(self):
        self.connected = False
        self.running = False

