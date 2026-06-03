from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib
import zlib


def generate_key():
    return get_random_bytes(16)


def encrypt_message(message, key):

    cipher = AES.new(key, AES.MODE_EAX)

    ciphertext, tag = cipher.encrypt_and_digest(
        message.encode()
    )

    hash_value = hashlib.sha256(ciphertext).hexdigest()

    combined_data = (
        cipher.nonce +
        tag +
        ciphertext +
        hash_value.encode()
    )

    compressed_data = zlib.compress(combined_data)

    return compressed_data


def decrypt_message(data, key):

    decompressed = zlib.decompress(data)

    nonce = decompressed[:16]

    tag = decompressed[16:32]

    extracted_hash = decompressed[-64:].decode()

    ciphertext = decompressed[32:-64]

    new_hash = hashlib.sha256(ciphertext).hexdigest()

    if new_hash != extracted_hash:
        return "Integrity Verification Failed!"

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

    plaintext = cipher.decrypt(ciphertext)

    return plaintext.decode()