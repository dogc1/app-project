import asyncio
from Bluetooth import BluetoothDiscover

class TestFile():
    dict = asyncio.run(BluetoothDiscover().discover())
    print(dict)
