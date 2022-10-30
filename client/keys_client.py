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

        if web_port == 443:
            self.base_url = "https://{}/key/".format(host)
        else:
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
        t = SubscriberThread(key,self.host,self.subscribe_port,callback)
        t.setDaemon(True)
        t.start()
        
        return t        
        
class SubscriberThread(Thread):
    def __init__(self,key,host,port,callback):
        Thread.__init__(self)
        self.key = key
        self.host = host
        self.port = port
        self.callback = callback
        
        self.running = True
        self.daemon = True
        
    def run(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))
            
        self.s.sendall(str.encode(self.key))

        while self.running:
            try:
                data = self.s.recv(1024).decode("utf-8")
                self.callback(data)
            except:
                print("Connection to server closed!")
                break

        self.stop()

    def stop(self):
        self.s.close()
        self._is_running = False
        self.running = False

