"""A TCP server to check if a string supplied by a client is a palindrome"""
import sys
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
        """
        Runs once per client connection in its own process. Accepts string from client
        and replies True or False depending on whether the string was a palindrome.
        """
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
        """Runs periodically to check whether the server should shut down"""
        super().service_actions()
        if self.queueref.empty() != True:
            if self.queueref.get() == 'q':
                self.server_close() #Unbinds from socket
                exit(0)
    
    def queued_serve_forever(self, q1):
        """
        Helper method run once per server instance and allows communcation
        between the server processes and the server command line interface.
        """
        self.queueref = q1
        self.serve_forever()

        

class PalinServer:
    """Wrapper class that handles server logic in an interface agnostic manner"""
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
        self.pserv = Process(target=server.queued_serve_forever, args=(self.pqueue,))
        self.pserv.start()
        self.running = True
        print("Server process started on: " + self.host_name  + ":" + str(self.port_number))
        sys.stdout.flush()
    
    def stop(self):
        """Signals the server process to stop gracefully"""
        if self.running != True:
            exit(127) #maybe error check
        self.pqueue.put('q')
        self.pserv.join()
        print("Server successfully shutdown")

def main():
    """Entry point if the server is run directly"""
    mainserv = None
    if len(sys.argv) == 1:
        mainserv = PalinServer("", 12752)
    elif len(sys.argv) == 2:
        mainserv = PalinServer(sys.argv[1], 12752)
    elif len(sys.argv) == 3:
        mainserv = PalinServer(sys.argv[1], int(sys.argv[2]))
    else:
        print("Error: invalid syntax\nUsage:" + sys.argv[0] + " [ip addr] [port number]")
        exit(1)
    mainserv.run()
    userIn = input("Enter q to shutdown: ")
    while userIn != 'q':
        userIn = input("Enter q to shutdown: ")
    mainserv.stop()


if __name__ == '__main__':
    main()
