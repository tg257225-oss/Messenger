import socket
import threading
import tkinter as tk
import sys
from tkinter import scrolledtext
from tkinter import messagebox

host = '127.0.0.1'
port = 2345

DARK_BROWN = "#453D3C"
LIGHT_BROWN = "#9C8989"
OFF_WHITE = "#EBDFDF"
NORMAL_FONT = ("Lucida Sans", 16)
SMALL_FONT = ("Lucida Sans", 11)
FONT_COLOR = "#2B2A2A"
WHITE = "white"
BG = "#EDEBEB"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def msg_update(message):
    msg_box.config(state=tk.NORMAL)
    msg_box.insert(tk.END, message + '\n')
    msg_box.config(state=tk.DISABLED)

def connect():
    username_button.config(state=tk.NORMAL)
    username_textbox.config(state=tk.NORMAL)
    # connect to server
    try:
        client.connect((host, port))
        msg_update("[SERVER] Successfully connected to the server.")
        username_button.config(state=tk.DISABLED)
        username_textbox.config(state=tk.DISABLED)
    except:
        messagebox.showerror("Error", f"Unable to connect to server {host} {port}.")
        #exit(0)

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Error", "The username field cannot be empty.")
        #exit(0)

    threading.Thread(target=listen_for_msg_from_serv, args=(client, ), daemon=True).start()


def send_message(event=None):
    message = message_txtbox.get()
    if message != '':
        client.sendall(message.encode())
        message_txtbox.delete(0, tk.END)
    else:
        sys.stdout.write(" ")
        sys.stdout.flush()




root = tk.Tk()
root.geometry("600x600")
root.title("Messenger")
root.resizable(False, False)


root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=6)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

top_frame = tk.Frame(root, width=600, height=55, bg=LIGHT_BROWN)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)
top_frame.pack_propagate(False)

middle_frame = tk.Frame(root, width=600, height=470, bg=OFF_WHITE )
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=55, bg=DARK_BROWN)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)
bottom_frame.pack_propagate(False)

username_label = tk.Label(top_frame, text="Enter your username:", font=NORMAL_FONT, fg=FONT_COLOR, bg=LIGHT_BROWN)
username_label.pack(side=tk.LEFT, padx=(10,0) )

username_textbox = tk.Entry(top_frame, font=NORMAL_FONT, bg=BG, fg=FONT_COLOR, width=20)
username_textbox.pack(side=tk.LEFT, padx=(10,10), pady=(2, 0))

username_button = tk.Button(top_frame, text="Join", font=SMALL_FONT, fg=FONT_COLOR, bg=OFF_WHITE, command=connect, height=1, width=4)
username_button.pack(side=tk.LEFT, padx=(10,10), pady=(2,0))


message_txtbox = tk.Entry(bottom_frame, font=NORMAL_FONT, bg=BG, width=38)
message_txtbox.pack(side=tk.LEFT, padx=12)

msg_button = tk.Button(bottom_frame, text="Send", font=SMALL_FONT, fg=FONT_COLOR, bg=OFF_WHITE, command=send_message)
msg_button.pack(side=tk.LEFT, padx=10)

msg_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=OFF_WHITE, fg=FONT_COLOR, width=67, height=29)
msg_box.config(state=tk.DISABLED)
msg_box.pack(side=tk.TOP)




root.bind("<Return>", send_message)


def listen_for_msg_from_serv(client):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            parts = message.split(": ", 1)
            username = parts[0]
            content = parts[1] if len(parts) > 1 else ""



            sys.stdout.write("\r\033[K")
            msg_update(f"[{username}] {content}")

            sys.stdout.write(" ")
            sys.stdout.flush()

        else:
            messagebox.showerror("Error","The message received from the client is empty.")


def main():
    root.mainloop()



if __name__ == '__main__':
    main()