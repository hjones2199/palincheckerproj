"""A TCP server to check if a string supplied by a client is a palindrome"""

def is_palindrome(string):
    """Checks whether the specified string is a palindrome"""
    if string.lower() == (string.lower()[::-1]):
        return True
    else:
        return False

class PalinServer:
    """Wrapper class that handles server logic"""
    host_name = "localhost"
    port_number = 12752

    def __init__(self, host_name, port_number):
        """Instantiates a new palindrome server and sanity checks initial data"""
        self.host_name = host_name
        if port_number > 1024: #Program should never have permissions to use reserved ports
            self.port_number = port_number
        else:
            pass #TODO: Error handling
    
    def start(self):
        """Attempts to start up the server on the instances hostname and port number"""
        pass #TODO: server starting logic


def main():
    """Entry point if the server is run directly"""
    pass #TODO

if __name__ == '__main__':
    main()
