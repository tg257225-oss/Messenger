import socket
import threading

host = '127.0.0.1'
port = 2345
listener_limit = 4
active_clients = [] # ls of all active users


# listens for msgs from clients
def listen_for_msg(client, username):

    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + ': ' + message
            send_msg_to_all(final_msg)
        else:
            print(f"The message sent from the client {username} is empty.")

# sends new msg to single client
def send_msg_to_client(client, message):
    client.sendall(message.encode())

# sends new msg to all clients on the server
def send_msg_to_all(message):

    for user in active_clients:
        send_msg_to_client(user[1], message)



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