import socket

def query_server(msg, ip, port, buffSize):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.send(msg.encode())
    reply = sock.recv(buffSize)
    sock.close()
    return reply.decode()

def term_interface():
    buffSize = 2048 #not configurable in current server implementation without editing code
    IP = input("Enter IP address of palindrome server: ")
    PORT = int(input("Enter port number of palindrome server: "))
    userIn = ""
    while(True):
        userIn = input("Enter a string to check for palindrome or q to quit: ")
        if userIn == 'q':
            return
        else:
            print("Server says: " + query_server(userIn, IP, PORT, buffSize))

def main():
    term_interface()

if __name__ == '__main__':
    main()