from bleak import BleakScanner, BleakClient
from bleak.exc import BleakDeviceNotFoundError
import asyncio
import struct
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

_TEMPERATURE_UUID = "2A6E"
_HUMIDITY_UUID    = "2A6F"
_PRESSURE_UUID    = "2A6D"

class BluetoothDiscover:

    _timeout = 5

    async def discover(self):
        logging.info("Searching for devices...")
        found_devices = await BleakScanner.discover(timeout = BluetoothDiscover._timeout, return_adv = True)
        device_data = dict()
        for key, device in found_devices.items():
            if device[0].name:
                logging.info("Found device address: %s with name: %s", key, device[0].name)
                device_data[key] = device[0].name
            else:
                logging.info("Found device address: %s", key)
                device_data[key] = None
        
        return device_data

class BluetoothConnection:

    # TODO Should be for all devices via grafic interface
    refresh_timer = 5

    def __init__(self, device_address: str, name = None):
        self._device_address: str = device_address
        self._client: BleakClient = None
        self._connected: bool = False
        self._data = dict()
        self._data["Address"] = device_address
        self._data["Name"] = name

    
    async def connect(self, queue):
        async with BleakClient(self._device_address) as client:
            logging.info("Connecting device with address: '%s'", self._device_address)
            
            if client.is_connected:
                logging.info("Connected to device with address: '%s'", self._device_address)
                self._connected = True
                self._client = client
                await self._request_data(queue)

            else:
                logging.error("Connection to device with address: '%s' failed!", self._device_address)

    async def _request_data(self, queue):

        logging.info("Refreshing data for device: '%s' every %s seconds...", 
            self._device_address, BluetoothConnection.refresh_timer)
        
        while self._connected:
            try:

                temp = await self._client.read_gatt_char(_TEMPERATURE_UUID)
                pressure = await self._client.read_gatt_char(_PRESSURE_UUID)
                humidity = await self._client.read_gatt_char(_HUMIDITY_UUID)

                self._data["Temperature"] = self._encode_temperature(temp)
                self._data["Humidity"] = self._encode_humidity(humidity)
                self._data["Pressure"] = self._encode_pressure(pressure)

                queue.put(self._data)

                await asyncio.sleep(BluetoothConnection.refresh_timer)

            except BleakDeviceNotFoundError:
                logging.error("Device with address: '%s' not found!", self._device_address)
            except Exception as e:
                logging.error("Error while connecting device '%s': %s", self._device_address, e)

    def get_sensor_data(self):
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
