import threading
from Bluetooth import *
import time
'''
    Testscript for parallelization
'''
if __name__ == '__main__':

    print("Searching for devices...")
    search = asyncio.run(BluetoothDiscover().discover())
    for device in search.items():
        print("Found:", device)
    print("Done.")

    connection_list = list()
    device_dict = dict()

    connection_list.append("08:F9:E0:F4:7B:3A")

    print("Connect gsog_sensor...")
    for address in connection_list:
        connection = BluetoothConnection(address)
        thread = threading.Thread(target=asyncio.run, args=(connection.connect(),))
        device_dict[address] = connection
        thread.start()

    print("Reading and printing data for gsog_sensor...")
    while True:
        gsog_sensor = device_dict[address]
        print("Received Data:", gsog_sensor.get_sensor_data())
        time.sleep(3)
