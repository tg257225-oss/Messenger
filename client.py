import socket
import threading
host = '127.0.0.1'
port = 2345
def listen_for_msg_from_serv(client):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            parts = message.split(": ", 1)
            username = parts[0]
            content = parts[1] if len(parts) > 1 else ""


            print(f"[{username}] {content}")
        else:
            print("The message received from the client is empty.")



def send_msg_to_serv(client):
    while 1:
        message = input("Message: ")
        if message != '':
            client.sendall(message.encode())
        else:
            print("The message is currently empty.")




def comms_to_server(client):

    username = input("Enter your username: ")
    if username != '':
        client.sendall(username.encode())
    else:
        print("The username field cannot be empty.")
        exit(0)

    threading.Thread(target=listen_for_msg_from_serv, args=(client, )).start()
    send_msg_to_serv(client)


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server
    try:
        client.connect((host, port))
        print(f"The client is now connected to the server.")
    except:
        print(f"Unable to connect to server {host} {port}.")
        exit(0)


    comms_to_server(client)

if __name__ == '__main__':
    main()