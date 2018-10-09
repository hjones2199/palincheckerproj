"""A TCP server to check if a string supplied by a client is a palindrome"""
import socketserver
import os
from multiprocessing import Process, Queue

def is_palindrome(string):
    """Checks whether the specified string is a palindrome"""
    if string.lower() == (string.lower()[::-1]):
        return True
    else:
        return False

class TCPForkHandler(socketserver.BaseRequestHandler):
    """Handles multiprocess logic for an a TCP server that accepts ASCII"""
    def handle(self):
        """TODO"""
        client_req = self.request.recv(2048)
        answer = is_palindrome(str(client_req, 'ascii').rstrip()) #True or False
        if answer:
            self.request.sendall("True\n".encode())
        else:
            self.request.sendall("False\n".encode())

class ForkingServerTCP(socketserver.ForkingMixIn, socketserver.TCPServer):
    """Handles Unix fork logic automatically"""
    queueref = None
    def service_actions(self):
        super().service_actions()
        if self.queueref.empty() != True:
            if self.queueref.get() == 'q':
                self.shutdown()
                self.server_close()
                exit(0)
    
    def queued_serve_forever(self, q1):
        self.queueref = q1
        self.serve_forever()

        

class PalinServer:
    """Wrapper class that handles server logic"""
    host_name = "localhost"
    port_number = 12752
    pserv = None
    running = False
    pqueue = None

    def __init__(self, host_name, port_number):
        """Instantiates a new palindrome server and sanity checks initial data"""
        self.host_name = host_name
        if port_number > 1024: #Program should never have permissions to use reserved ports
            self.port_number = port_number
        else:
            print("Invalid port number")
            exit(127) #Maybe change error code
    
    def run(self):
        """Attempts to start up the server on the instances hostname and port number"""
        if self.running:
            return #Maybe add error checking
        self.pqueue = Queue()
        server = ForkingServerTCP((self.host_name, self.port_number), TCPForkHandler)
        self.pserv = Process(server.queued_serve_forever(self.pqueue))
        self.pserv.start()
        self.running = True
        print("Server process started on: " + self.host_name  + ":" + str(self.port_number))
    
    def stop(self):
        if self.running != True:
            exit(127) #maybe error check
        self.pqueue.put('q')
        self.pserv.join()

            

def main():
    """Entry point if the server is run directly"""
    mainserv = PalinServer("localhost", 12752)
    mainserv.run()
    userIn = input("Enter q to shutdown: ")
    while userIn != 'q':
        userIn = input("Enter q to shutdown: ")
    mainserv.stop()


if __name__ == '__main__':
    main()
