import sys, os
import asyncio
from bleak import BleakClient, BleakScanner


MAGIC_CMD = b'\n\x17\x15\xec\xdaD\xf2"\t\x08\x06\x12\x03\xf8\x05\n\x18\x015\xa9\xd9BDH\x03'
TORADIO_UUID = "f75c76d2-129e-4dad-a1dd-7866124401e7"

async def send_reboot(addr):
    print("connecting")
    async with BleakClient(addr) as client:
        print("sending command")
        await client.write_gatt_char(TORADIO_UUID, MAGIC_CMD)
        await asyncio.sleep(3)
        print("done")

try:
    addr = sys.argv[1]
    asyncio.run(send_reboot(addr))
except IndexError:
    print("Usage: blereboot-ota.py bleaddr")
    asyncio.run(scan())



