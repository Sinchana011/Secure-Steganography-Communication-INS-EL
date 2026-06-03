from PIL import Image


def to_binary(data):

    return ''.join(
        format(byte, '08b')
        for byte in data
    )


def embed_data(image_path, data, output_path):

    img = Image.open(image_path)

    binary_data = to_binary(data)

    payload_length = format(
        len(binary_data),
        '032b'
    )

    final_data = payload_length + binary_data

    pixels = img.load()

    width, height = img.size

    data_index = 0

    for y in range(height):

        for x in range(width):

            pixel = list(pixels[x, y])

            for i in range(3):

                if data_index < len(final_data):

                    pixel[i] = (
                        pixel[i] & ~1 |
                        int(final_data[data_index])
                    )

                    data_index += 1

            pixels[x, y] = tuple(pixel)

            if data_index >= len(final_data):

                img.save(output_path)

                return

    print("Image too small!")


def extract_data(image_path):

    img = Image.open(image_path)

    pixels = img.load()

    width, height = img.size

    binary_data = ""

    for y in range(height):

        for x in range(width):

            pixel = pixels[x, y]

            for i in range(3):

                binary_data += str(pixel[i] & 1)

    payload_length = int(
        binary_data[:32],
        2
    )

    hidden_data = binary_data[
        32:32 + payload_length
    ]

    byte_data = bytes(

        int(hidden_data[i:i+8], 2)

        for i in range(0, len(hidden_data), 8)

    )

    return byte_data