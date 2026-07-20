import socket
import threading

host = '127.0.0.1'
port = 2345
listener_limit = 4
active_clients = [] # ls of all active users

# sends new msg to all clients on the server
def send_msg_to_all(from_username, message):
    pass


def client_handler(client):

    # server listens for client registering their username
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
        else:
            print("There is no username.")


def main():

    # af_init = ipv4 address
    # sock streem = tcp packs for communcaiton
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # give server address in the form of host ip and port
        server.bind((host, port))
        print(f"The server is now running on {host} {port}.")
    except:
        print(f"Unable to bind to the host {host} and port {port}.")


    # max number of client connections the server can make
    server.listen(listener_limit)

    # listens for client connections
    while 1:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}.")

        threading.Thread(target=client_handler, args=(client, )).start()

if __name__ == '__main__':
    main()