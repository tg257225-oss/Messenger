import socket
import threading

host = '127.0.0.1'
port = 2345
listener_limit = 4

def main():

    # af_init = ipv4 address
    # sock streem = tcp packs for communcaiton
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # give server address in the form of host ip and port
        server.bind((host, port))
        print("The server is now running.")
    except:
        print(f"Unable to bind to the host {host} and port {port}.")


    # max number of client connections the server can make
    server.listen(listener_limit)

    # listens for client connections
    while 1:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}.")

if __name__ == '__main__':
    main()