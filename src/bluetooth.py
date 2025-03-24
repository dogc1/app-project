from bleak import BleakScanner, BleakClient
from bleak.exc import BleakDeviceNotFoundError
from time import sleep
import struct
import logging
from culsans import Queue
import asyncio

logger = logging.getLogger("Bluetooth")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

_TEMPERATURE_UUID = "2A6E"
_HUMIDITY_UUID    = "2A6F"
_PRESSURE_UUID    = "2A6D"

class BluetoothDiscover:

    _timeout = 5

    async def discover(self):
        logger.info("Searching for devices...")
        found_devices = await BleakScanner.discover(timeout = BluetoothDiscover._timeout, return_adv = True)
        device_data = dict()
        for key, device in found_devices.items():
            if device[0].name:
                logger.info("Found device address: %s with name: %s", key, device[0].name)
                device_data[key] = device[0].name
            else:
                logger.info("Found device address: %s", key)
                device_data[key] = None
        
        return device_data

class BluetoothConnection:

    refresh_timer = 5

    def __init__(self, queue: Queue, device_address: str, name = None):
        self._device_address: str = device_address
        self._client: BleakClient = None
        self._data = dict()
        self._data["Address"] = device_address
        self._data["Name"] = name
        self._queue = queue
    
    async def connect(self):
        async with BleakClient(self._device_address) as client:
            logger.info("Connecting device with address: '%s'", self._device_address)
            
            try:
                logger.info("Connected to device with address: '%s'", self._device_address)
                self._client = client
                await self._request_data()

            except Exception:
                logger.error("Connection to device with address: '%s' failed!", self._device_address)

    async def _request_data(self):

        logger.info("Fetching data for device: '%s' every %s seconds", 
            self._device_address, BluetoothConnection.refresh_timer)

        while True:
            
            try:
                sleep(BluetoothConnection.refresh_timer)

                temp = await self._client.read_gatt_char(_TEMPERATURE_UUID)
                pressure = await self._client.read_gatt_char(_PRESSURE_UUID)
                humidity = await self._client.read_gatt_char(_HUMIDITY_UUID)

                self._data["Temperature"] = self._encode_temperature(temp)
                self._data["Humidity"] = self._encode_humidity(humidity)
                self._data["Pressure"] = self._encode_pressure(pressure)
                self._data["Connected"] = self._client.is_connected

                if not self._queue.full():
                    self._queue.sync_q.put_nowait(self._data)

            except BleakDeviceNotFoundError:
                logger.error("Device with address: '%s' not found!", self._device_address)
            except Exception as e:
                logger.error("Error while connecting device '%s': %s", self._device_address, e)

    def get_sensor_data(self):
        print(self._data)
        return self._data

    def _encode_temperature(self, raw_temp):
        float_temp = float(struct.unpack('<h', raw_temp)[0] / 100)
        return ("{:.2f}".format(float_temp), "°C")

    def _encode_humidity(self, raw_humidity):
        float_humidity = float(struct.unpack('<h', raw_humidity)[0] / 100)
        return ("{:.2f}".format(float_humidity), "%")

    def _encode_pressure(self, raw_pressure):
        float_pressure = float(struct.unpack('<i', raw_pressure)[0] / 10)
        return ("{:.1f}".format(float_pressure), "hPa")
