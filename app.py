import os
import socket
import tempfile

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from receiver_listener import (
    start_receiver,
    get_latest_message
)

from sender_system.aes_utils import encrypt_message
from sender_system.stegano_utils import embed_data

# ---------------------------------
# Constants
# ---------------------------------

HOST = "127.0.0.1"
PORT = 5050

KEY = b'1234567890abcdef'

# ---------------------------------
# Page Config
# ---------------------------------

st.set_page_config(
    page_title="Secure Steganography Communication System",
    layout="wide"
)

# ---------------------------------
# Auto Refresh
# ---------------------------------

st_autorefresh(
    interval=1000,
    key="receiver_refresh"
)

# ---------------------------------
# Session State
# ---------------------------------

if "sender_message" not in st.session_state:
    st.session_state.sender_message = ""

if "receiver_message" not in st.session_state:
    st.session_state.receiver_message = ""

if "received_message" not in st.session_state:
    st.session_state.received_message = ""

# ---------------------------------
# Start Receiver
# ---------------------------------

if "receiver_started" not in st.session_state:

    start_receiver()

    st.session_state.receiver_started = True

# ---------------------------------
# Check Incoming Messages
# ---------------------------------

incoming = get_latest_message()

if incoming:

    st.session_state.receiver_message = (
        "Image received successfully."
    )

    st.session_state.received_message = incoming

# ---------------------------------
# UI
# ---------------------------------

st.title(
    "Secure Steganography Communication System"
)

st.caption(
    "AES Encryption • SHA-256 Integrity Verification • LSB Steganography • Socket Communication"
)

left_col, right_col = st.columns(2)

# =================================
# Sender
# =================================

with left_col:

    st.subheader("Sender")

    message = st.text_area(
        "Enter Secret Message"
    )

    uploaded_image = st.file_uploader(
        "Choose PNG Image",
        type=["png"]
    )

    if st.button("Encrypt and Send"):

        try:

            if not message:

                st.warning(
                    "Please enter a message."
                )

            elif uploaded_image is None:

                st.warning(
                    "Please upload a PNG image."
                )

            else:

                st.session_state.receiver_message = ""
                st.session_state.received_message = ""

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".png"
                ) as temp_image:

                    temp_image.write(
                        uploaded_image.getbuffer()
                    )

                    cover_image_path = temp_image.name

                encrypted_data = encrypt_message(
                    message,
                    KEY
                )

                stego_image_path = "stego_image.png"

                embed_data(
                    cover_image_path,
                    encrypted_data,
                    stego_image_path
                )

                client = socket.socket()

                client.connect(
                    (HOST, PORT)
                )

                with open(
                    stego_image_path,
                    "rb"
                ) as file:

                    while True:

                        data = file.read(4096)

                        if not data:
                            break

                        client.sendall(data)

                client.close()

                if os.path.exists(
                    cover_image_path
                ):
                    os.remove(
                        cover_image_path
                    )

                st.session_state.sender_message = (
                    "Image sent successfully."
                )

        except Exception as e:

            st.session_state.sender_message = (
                f"Error: {e}"
            )

    if st.session_state.sender_message:

        st.success(
            st.session_state.sender_message
        )

# =================================
# Receiver
# =================================

with right_col:

    st.subheader("Receiver")

    if st.session_state.receiver_message:

        st.success(
            st.session_state.receiver_message
        )

    st.text_area(
        "Recovered Message",
        value=st.session_state.received_message,
        height=250,
        disabled=True
    )