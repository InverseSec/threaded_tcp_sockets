import socket
import queue
import threading
import TCP_connection as tcpC

##the accept method is blocking

def acceptConnections(server, queue):
    lock = threading.Lock()
    while True:
        lock.acquire()
        queue.put(server.accept())
        lock.release()

def interface():
    x = input("->mode?\n")
    if x == "1":
        address = "127.0.0.1"
    elif x == "2":
        address = input("->enter address\n")
    else:
        address = "192.168.1.5"
    port=2000
    binder = (address, port)
    return binder
    
  

def main():

    tcp_server = socket.socket()
    tcp_server.bind(interface())

    conn_queue = queue.Queue()
    lock = threading.Lock()
    adder = threading.Thread(target=acceptConnections,
                             args=(tcp_server, conn_queue))
    
    connections = []
    for x in range(0,2):
        connections.append(tcpC.Connection(conn_queue))

    tcp_server.listen(4)

    adder.start()
    for conn in connections:
        conn.start()

    while True:
        pass



if __name__ == "__main__":
    main()
