from bleak import BleakScanner, BleakClient
from bleak.exc import BleakDeviceNotFoundError
from time import sleep
import struct
import logging
from culsans import Queue

logger = logging.getLogger("Bluetooth")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

_TEMPERATURE_UUID = "2A6E"
_HUMIDITY_UUID    = "2A6F"
_PRESSURE_UUID    = "2A6D"
class BluetoothDiscover:
    """
    __author__ = Tahir Bulut

    Scannerklasse für Bluetooth
    """
    _timeout = 5

    async def discover(self):
        """
        Methode zum Scannen der verfübaren Bluetoothgeräte

        Returns:
            dict: Dictionary mit Adressen und Gerätenamen, falls Gerätenamen verfügbar
        """
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
    """
    __author__ = Dario Gloc, Tahir Bulut

    Klasse zur Verbindung und Datenübertragung über Bluetooth

    Attributes:
        _device_address (str): Adresse des zu verbindenen Gerätes
        _client (BleakClient): Interface zur BLE GATT-Kommunikation
        _data (dict): Dictionary zum Speichern der Geräte- sowie Kommunikationsinformationen
        _queue (Queue): Schreibende Seite der Queue zur Übermittlung des Dictionaries
    """
    refresh_timer = 5

    def __init__(self, queue: Queue, device_address: str, name = None):
        """
        Initialisator der Klasse

        Parameters:
            _queue (Queue): Für die Kommunikation verwendete Queue
            _device_address (str): Geräteadresse zur Verbindung
            name (default=None): Gerätenamen, falls vorhanden
        """
        self._device_address: str = device_address
        self._client: BleakClient = None
        self._data = dict()
        self._data["Address"] = device_address
        self._data["Name"] = name
        self._queue = queue
    
    async def connect(self):
        """
        Methode zur Erzeugung der Bluetooth-Verbindung über das Bleak-Interface
        """
        async with BleakClient(self._device_address) as client:
            logger.info("Connecting device with address: '%s'", self._device_address)
            
            try:
                logger.info("Connected to device with address: '%s'", self._device_address)
                self._client = client
                await self._request_data()

            except Exception:
                logger.error("Connection to device with address: '%s' failed!", self._device_address)

    async def _request_data(self):
        """
        Methode zum Lesen der Sensorwerte über das GATT-Protokoll anhand von UUID-Schnittstellen,
        Aufrechterhaltung der Verbindung, Beschreiben des Dictionaries als auch Ablegen der Daten in die Queue
        """
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

    def _encode_temperature(self, raw_temp):
        """
        Hilfsmethode zur Korrektur des Temperaturwertes

        Parameters:
            raw_temp: Zu korrigierender Temperaturwert
        """
        float_temp = float(struct.unpack('<h', raw_temp)[0] / 100)
        return ("{:.2f}".format(float_temp), "°C")

    def _encode_humidity(self, raw_humidity):
        """
        Hilfsmethode zur Korrektur des Luftfeutigkeitswertes

        Parameters:
            raw_temp: Zu korrigierender Luftfeutigkeitswert
        """
        float_humidity = float(struct.unpack('<h', raw_humidity)[0] / 100)
        return ("{:.2f}".format(float_humidity), "%")

    def _encode_pressure(self, raw_pressure):
        """
        Hilfsmethode zur Korrektur des Druckwertes

        Parameters:
            raw_temp: Zu korrigierender Druckwert
        """
        float_pressure = float(struct.unpack('<i', raw_pressure)[0] / 10)
        return ("{:.1f}".format(float_pressure), "hPa")
