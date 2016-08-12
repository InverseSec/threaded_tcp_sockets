import socket
import json

def connect(address=None):
    s = socket.socket()
    if address == "":
        address = "127.0.0.1"
    s.connect((address, 2000))
    print("->connected")
    return s

def createRequest(filename, mode='a+', content= ""):
    request = {"filename": filename,
               "mode": mode,
               "content": content,
               }
    return request

def sendRequest(socket, request):
    try:
        socket.send(json.dumps(request).encode("utf-8"))
        content = json.loads(socket.recv(1024).decode("utf-8"))
    except ConnectionResetError:
        print("the server reset the connection")
    return content

def receiveContent(socket):
    try:
        content = socket.recv(1024).decode("utf-8")
    except ConnectionResetError:
        print("the server reset the connection")
        
    return content




    

def main():
    cont = True
    server = connect(input("->enter the address of the server\n->"))
    while cont:
        fname = input("->enter the name of the file you wish to open/create\n->")
        content = input("-> hit enter to open the file's contents or type a message to add to the file\n->")
        request = createRequest(fname, 'a', content)
        sendRequest(server, request)
        print(recieveContent(server))

        msg = input("->enter 'quit' to exit\n->")
        server.send(msg.encode("utf-"))

        if msg == "quit":
            cont = False
            server.shutdown()
            server.close()
        
        
        




if __name__ == "__main__":
    main()
    

