import socket

from aes_utils import decrypt_message
from stegano_utils import extract_data


HOST = "127.0.0.1"
PORT = 5050

KEY = b'1234567890abcdef'


server = socket.socket()

server.bind((HOST, PORT))

server.listen(1)

print(f"Server listening on port {PORT}...")


conn, addr = server.accept()

print(f"Connected by {addr}")


with open("received_stego.png", "wb") as file:

    while True:

        data = conn.recv(4096)

        if not data:
            break

        file.write(data)

print("Image received successfully.")


conn.close()

server.close()


hidden_data = extract_data(
    "received_stego.png"
)

message = decrypt_message(
    hidden_data,
    KEY
)

print("\nRecovered Message:")
print(message)