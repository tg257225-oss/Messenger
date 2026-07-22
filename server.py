import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

host = '127.0.0.1'
port = 2345
listener_limit = 4
active_clients = [] # ls of all active users

DARK_BROWN = "#453D3C"
LIGHT_BROWN = "#9C8989"
OFF_WHITE = "#EBDFDF"
NORMAL_FONT = ("Lucida Sans", 16)
SMALL_FONT = ("Lucida Sans", 11)
FONT_COLOR = "#2B2A2A"
WHITE = "white"
BG = "#EDEBEB"

def msg_update(message):
    msg_box.config(state=tk.NORMAL)
    msg_box.insert(tk.END, message + '\n')
    msg_box.config(state=tk.DISABLED)


root = tk.Tk()
root.geometry("600x200")
root.title("Messenger Server")
root.resizable(False, False)

top_frame = tk.Frame(root, width=600, height=50, bg=LIGHT_BROWN)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)
top_frame.pack_propagate(False)

bottom_frame = tk.Frame(root, width=600, height=150, bg=OFF_WHITE )
bottom_frame.grid(row=1, column=0, sticky=tk.NSEW)
bottom_frame.pack_propagate(False)

server_label = tk.Label(top_frame, text="Server", font=NORMAL_FONT, fg=FONT_COLOR, bg=LIGHT_BROWN)
server_label.pack(side=tk.LEFT, padx=(10,0) )

msg_box = scrolledtext.ScrolledText(bottom_frame, font=SMALL_FONT, bg=OFF_WHITE, fg=FONT_COLOR, width=67, height=29)
msg_box.config(state=tk.DISABLED)
msg_box.pack(side=tk.TOP)

# listens for msgs from clients
def listen_for_msg(client, username):

    while 1:
        try:
            message = client.recv(2048).decode('utf-8')
            if message != '':
                final_msg = username + ': ' + message
                send_msg_to_all(final_msg)
            else:
                remove_client(client, username)
                break
        except:
            remove_client(client, username)

            break



def remove_client(client, username):
    for user in active_clients:
        if user[1] == client:
            active_clients.remove(user)
            msg_update(f"Client {username} has disconnected.")
            client.close()
            break

    usernames = ", ".join([user[0] for user in active_clients])
    send_msg_to_all(f"SERVER: Client {username} has disconnected.")
    send_msg_to_all(f"Current active users: {usernames}")




# sends new msg to single client
def send_msg_to_client(client, message):

    client.sendall(message.encode())

# sends new msg to all clients on the server
def send_msg_to_all(message):

    usernames = ", ".join([user[0] for user in active_clients])
    msg_update(f"Current active users: {usernames}")


    for user in active_clients:
        send_msg_to_client(user[1], message)



def client_handler(client):

    # server listens for client registering their username
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            usernames = ", ".join([user[0] for user in active_clients])
            send_msg_to_all(f"Current active users: {usernames}")
            break
        else:
            msg_update("There is no username.")

    threading.Thread(target=listen_for_msg, args=(client, username, )).start()


def server_loop():


    # af_init = ipv4 address
    # sock streem = tcp packs for communication
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # give server address in the form of host ip and port
        server.bind((host, port))
        msg_update(f"The server is now running on {host} {port}.")
    except:
        msg_update(f"Unable to bind to the host {host} and port {port}.")
        return



    # max number of client connections the server can make
    server.listen(listener_limit)

    # listens for client connections
    while 1:
        client, address = server.accept()
        msg_update(f"Successfully connected to the client {address[0]} {address[1]}.")

        threading.Thread(target=client_handler, args=(client, )).start()



def main():
    threading.Thread(target=server_loop, daemon=True).start()
    root.mainloop()

if __name__ == '__main__':
    main()