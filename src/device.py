from bluetooth import BluetoothConnection
from queue import Queue
import threading
import asyncio

class Device:
    def __init__(self, mac_address, device_name):
        self._device_name = device_name
        self._mac_address = mac_address

    async def device_connection(self):
        device_client = await BluetoothConnection(self._mac_address, self._device_name)

        async def producer(w_queue):
            while True:
                data = await device_client.request_data()
                print("write")
                w_queue.put(data)
                await asyncio.sleep(4)

        async def consumer(r_queue):
            while True:
                print("read:", r_queue.get())
                await asyncio.sleep(4)

        queue = Queue()
        t_consumer = threading.Thread(target = consumer, args =(queue, )) 
        t_producer = threading.Thread(target = producer, args =(queue, ))
        t_consumer.start()
        t_producer.start()

                    
'''
class BluetoothDeviceManager:
    def __init__(self):
        self.devices = self.load_devices(self._mac_address, self._device_name)

    def load_devices(self):
        try:
            with open('devices.json', 'r') as f:
                devices = json.load(f)
                print(f"Geräte geladen: {devices}")
        except FileNotFoundError:
            devices = []
            print("Keine Geräte-Datei gefunden, es wird eine neue erstellt.")
        return devices

    def save_devices(self):
        with open('devices.json', 'w') as f:s
            json.dump(self.devices, f, indent=4)
            print(f"Geräte gespeichert: {self.devices}")

    def add_device(self, device):
        if not any(d["mac_address"] == device.mac_address for d in self.devices):
            self.devices.append(device.to_dict())
            self.save_devices()
            print(f"Gerät hinzugefügt: {device.device_name}")
        else:
            print(f"Gerät mit der MAC-Adresse {device.mac_address} existiert bereits.")

    def remove_device(self, mac_address):
        print(f"Versuche, Gerät mit MAC-Adresse {mac_address} zu löschen...")
        for device in self.devices:
            if device["mac_address"] == mac_address:
                self.devices.remove(device)
                print(f"Gerät mit MAC-Adresse {mac_address} entfernt.")
                self.save_devices()
                return
        print(f"Kein Gerät mit MAC-Adresse {mac_address} gefunden.")
'''

if __name__ == '__main__':
    dev = Device("08:F9:E0:F4:7B:3A", "GSOG_SENSOR1")
    asyncio.run(dev.device_connection())
