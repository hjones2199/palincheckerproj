**Client Usage**
    The client program is found at client/palinchecker_client.py, and requires
no command line arguments. When run, the client will prompt the user for the
ip address and port number of the server. It will then attempt to establish
a connection and verify that the server is running. Assuming this is successful
it will then prompt the user for strings, and reply with the servers response
as to whether the given string is a palindrome. To quit you simply input q.

**Server Usage**
    The server is found at server/palindrome_server.py, and can either take no
arguments or exactly 2 arguments *<ip address to bind to>* *port*. If no command
line arguments are given it will bind to all IP addresses at port 12752. The server
can be shut down by inputting q.

**Dependencies**
    Both the server and the client require python3 to run correctly. The client can
trivially be converted to python 2 with the program 2to3, but the server relies heavily
on python3 specific features, namely the socketserver module and the object oriented
multiprocessing implementation. The server also relies on a Unix specific multiprocess
system based on the Posix *fork()* system call. I have tested it on multiple Linux
distributions and FreeBSD, but it should run on any POSIX compliant system.
