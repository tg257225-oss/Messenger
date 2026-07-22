# Messenger
Messenger is a Python progam (strictly Windows) that acts as your typical messaging platform.
### ![Messenger in action](Assets/messengerclients+server.png)
## How does it work?
Messenger follows the typical flow of any messaging system. Simply, if you enter a text into any messaging platform, your computer (client) will take the text and turn it in to small, digestable packets that are sent over a socket connnection to the server. These packets are labeled accordingly so the server knows who to ship them to. These packets are then shipped to the recipient client (computer) where they are reassembled and turned into text that appears on the screen.
## Features
* End-to-End Encryption - Only the people actively communicating in the chat can see the content of the messages. 
