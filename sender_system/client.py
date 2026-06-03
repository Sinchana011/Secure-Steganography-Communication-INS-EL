import socket

from aes_utils import encrypt_message
from stegano_utils import embed_data


SERVER_IP = "127.0.0.1"
PORT = 5050

KEY = b'1234567890abcdef'


message = input("Enter Secret Message: ")


encrypted_data = encrypt_message(
    message,
    KEY
)


embed_data(
    "../images/weeknd.png",
    encrypted_data,
    "stego_image.png"
)

print("Stego image generated.")


client = socket.socket()

client.connect((SERVER_IP, PORT))

print("Connected to receiver.")


with open("stego_image.png", "rb") as file:

    while True:

        data = file.read(4096)

        if not data:
            break

        client.sendall(data)

print("Image sent successfully.")

client.close()