import asyncio
import struct
import time
from pathlib import Path

async def send_image(host, port, image_path):
    reader, writer = await asyncio.open_connection(host, port)

    with open(image_path, "rb") as img_file:
        image_data = img_file.read()

    # Send the image size
    image_size = len(image_data)
    writer.write(struct.pack("!I", image_size))

    # Send the image data
    writer.write(image_data)
    await writer.drain()

    # Receive an acknowledgment from the server
    ack = await reader.read(3)
    print("Acknowledgment received:", ack.decode())

    writer.close()
    await writer.wait_closed()

async def main():
    host = "10.29.69.81"
    port = 21201
    image_path = "penguin.png"

    while True:
        await send_image(host, port, image_path)
        time.sleep(1)  # Adjust the delay between sending images as needed

if __name__ == "__main__":
    asyncio.run(main())
