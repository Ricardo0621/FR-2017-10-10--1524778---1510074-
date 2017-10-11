#!/usr/bin/env python3

import argparse

import sys
import itertools
import socket
import os 
from socket import socket as Socket

# A simple web server

# Issues:
# Ignores CRLF requirement
# Header must be < 1024 bytes
# ...
# probabaly loads more


def main():

    # Command line arguments. Use a port > 1024 by default so that we can run
    # without sudo, for use as a real server you need to use port 80.
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', default=2080, type=int,
                        help='Port to use')
    args = parser.parse_args()

    # Create the server socket (to handle tcp requests using ipv4), make sure
    # it is always closed by using with statement.
    #with Socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # The socket stays connected even after this script ends. So in order
    # to allow the immediate reuse of the socket (so that we can kill and
    # re-run the server while debugging) we set the following option. This
    # is potentially dangerous in real code: in rare cases you may get junk
    # data arriving at the socket.
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # COMPLETE (2)
    endpoint = ('', args.port)

    # COMPLETE (3)
    ss.bind(endpoint)
    ss.listen(1)
    print("server ready")

    while True:
         cs = ss.accept()[0] 
         request = cs.recv(1024).decode('ascii')
         reply = http_handle(request)
         cs.send(reply)


         print("\n\nReceived request")
         print("======================")
         print(request.rstrip())
         print("======================")


         print("\n\nReplied with")
         print("======================")
         print(reply.rstrip())
         print("======================")
         break

    return 0

def http_handle(request_string):
    file_name = request_string.split('\n')[0].split(' ')[1].replace('/','')
    if os.path.exists(file_name):
        if file_name.endswith(".html"):
            mimetype='text/html'
            sendReply = True
        if file_name.endswith(".jpg"):
            mimetype='image/jpg'
            sendReply = True
        if file_name.endswith(".gif"):
            mimetype='image/gif'
            sendReply = True
        if file_name.endswith(".js"):
            mimetype='application/javascript'
            sendReply = True
        if file_name.endswith(".css"):
            mimetype='text/css'
            sendReply = True
        headers = 'HTTP/1.1 200 OK'+'\n' + 'Content-Type:'+mimetype+'\n' + 'Connection: close'+'\n' + '\n'
        with open(file_name, 'rb') as myfile:
            data = myfile.read()
        answers= "%s%s\n"%(headers, data)
        return answers
    else:
        headers = 'HTTP/1.1 404 Not Found'+'\n' + 'Content-Type:text/html'+'\n' + 'Connection: close'+'\n' + '\n'
        with open('error.html', 'rb') as myfile:
            data = myfile.read()
        answers= "%s%s\n"%(headers, data)
        return answers
    """Given a http requst return a response

    Both request and response are unicode strings with platform standard
    line endings.
    """
    assert not isinstance(request_string, bytes)
    # Fill in the code to handle the http request here. You will probably want
    # to write additional functions to parse the http request into a nicer data
    # structure (eg a dict), and to easily create http responses.
if __name__ == "__main__":
    sys.exit(main())
