import socket
import threading

from receiver_system.aes_utils import decrypt_message
from receiver_system.stegano_utils import extract_data

HOST = "127.0.0.1"
PORT = 5050

KEY = b'1234567890abcdef'

latest_message = None
server_running = False


def get_latest_message():

    global latest_message

    msg = latest_message

    latest_message = None

    return msg


def start_receiver():

    global server_running

    if server_running:
        return

    server_running = True

    def receiver():

        global latest_message

        try:

            server = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            server.setsockopt(
                socket.SOL_SOCKET,
                socket.SO_REUSEADDR,
                1
            )

            server.bind((HOST, PORT))

            server.listen(5)

            print(
                f"Receiver listening on {HOST}:{PORT}"
            )

            while True:

                conn, addr = server.accept()

                print(
                    f"Connected by {addr}"
                )

                with open(
                    "received_stego.png",
                    "wb"
                ) as file:

                    while True:

                        data = conn.recv(4096)

                        if not data:
                            break

                        file.write(data)

                conn.close()

                print(
                    "Image received successfully."
                )

                hidden_data = extract_data(
                    "received_stego.png"
                )

                message = decrypt_message(
                    hidden_data,
                    KEY
                )

                latest_message = message

                print(
                    f"Recovered Message: {message}"
                )

        except Exception as e:

            print(
                f"Receiver Error: {e}"
            )

    threading.Thread(
        target=receiver,
        daemon=True
    ).start()