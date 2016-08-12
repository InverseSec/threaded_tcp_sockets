import threading
import socket
import json


'''
thread class that handles a connection, is spawned per connection
manages files and dumps data to/from a client to/from files
'''
class Connection(threading.Thread):
    def __init__(self, queue, client=None, address=None):
        threading.Thread.__init__(self)
        self._queue = queue
        self._client = client
        self._addr = address
        self._data = {}
        self._lock = threading.Lock()
        '''
keys =
/filename/, /mode/, /content/ from client, /response/ to client 
        '''
        self._lock = threading.Lock()

    def bind(self):
        self._lock.acquire()
        if not self._queue.empty():
            self._client, self._addr = self._queue.get()
        self._lock.release()
        if self._client != None:
            print("'{0}' has connected".format(self._addr))

    def receiveRequest(self):
        try:
            self._data = json.loads(self._client.recv(1024).decode("utf-8"))
        except ConnectionResetError:
            print("connection terminated by client '" + str(self._addr) + "'")
            
    def handleFile(self):
        try:
            self._lock.acquire()
            with open(self._data["filename"], self._data["mode"]) as f:
                f.write(self._data["content"])
                f.seek(0,0)
                self._data["response"] = f.readlines()
            self._lock.release()
        except KeyError:
            print("bad client response: " + str(self._data))
            #?raise a flag to not continue operations with this request?
        #except IOError:
         #   print("io error: " + str(self._data))

    def sendResponse(self):
        if self._data["response"] != "":
            msg = "content at '" + self._data["filename"] + "':\n" + "\n".join(self._data["response"])
            try:
                self._client.send(msg.encode("utf-8"))            
            except ConnectionResetError:
                print("connection terminated by client '" + str(self._addr) + "'")
        else:
            try:
                self._client.send("appended to file '" + self._data["filename"] + "'")
            except ConnectionResetError:
                print("connection terminated by client '" + str(self._addr) + "'")
        


    def run(self):
        while True:
            while self._client != None:
                self.receiveRequest()
                self.handleFile()
                self.sendResponse()
                
            #continue file operations

                try:
                    operation = self._client.recv(1024).decode("utf-8")
                    if operation == "quit":
                        self._client.close()
                        print("client '{0}' has exited".format(self._addr))
                        self._client = None
                        self._addr = None
                except ConnectionResetError:
                    print("connection terminated by client '" + str(self._addr) + "'")
                    

            if self._client == None:
                self.bind()
            
                
        
            
                


            
            

