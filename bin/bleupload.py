import sys, os
import asyncio
from bleak import BleakClient, BleakScanner


SERVICE_UUID                 = "4FAFC201-1FB5-459E-8FCC-C5C9C331914B"
CHARACTERISTIC_TX_UUID       = "62ec0272-3ec5-11eb-b378-0242ac130003"
CHARACTERISTIC_OTA_UUID      = "62ec0272-3ec5-11eb-b378-0242ac130005"

async def scan():
    print(await BleakScanner.discover())

async def flash(filename, addr):
    fwsize = os.path.getsize(filename)
    fwfile = open(filename, "rb")

    print("connecting")
    async with BleakClient(addr, services=[SERVICE_UUID]) as client:
        done = asyncio.Event()
        async def cb(sender, data):
            buf = fwfile.read(512)

            if not buf:
                print("done.")
                done.set()
                return

            print("wrote {}/{} bytes".format(fwfile.tell(), fwsize))
            await client.write_gatt_char(CHARACTERISTIC_OTA_UUID, buf)

        await client.start_notify(CHARACTERISTIC_TX_UUID, cb)
        print("start update")
        await client.write_gatt_char(CHARACTERISTIC_OTA_UUID, bytes())
        await done.wait()
        print("exit")

try:
    filename = sys.argv[1]
    addr = sys.argv[2]
    asyncio.run(flash(filename, addr))
except IndexError:
    print("Usage: bleflash.py filename bleaddr")
    print("restart node before: meshtastic --reboot-ota")
    asyncio.run(scan())
    


