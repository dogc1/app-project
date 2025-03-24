from bluetooth import BluetoothConnection
from threading import Thread
from culsans import Queue
import asyncio
import logging

logger = logging.getLogger("Device")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class DeviceCommunication:
    """
    __author__ = Dario Gloc

    Klasse zur Realisierung der Nebenläufigkeiten zwischen dem Mainthread und der Bluetooth-Kommunikation

    Attributes:
        _mac_address: MAC-Adresse zur Geräteverbindung
        _device_name: Name des Gerätes
        _queue: Queue zur Interkommunikation zwischen Main- und Bluetooththread
    """
    def __init__(self, mac_address, device_name = ""):
        """
        Initialisator der Klasse DeviceCommunication
        

        Args:
            mac_address: MAC-Adresse des zu verbindenden Gerätes
            device_name (default=""): Name des zu verbindenden Gerätes
        """
        self._mac_address = mac_address
        self._device_name = device_name
        self._device_connection: BluetoothConnection
        self._queue = Queue()
        
    def run_thread(self):
        """
        Erzeugung der Thread-Nebenläufigkeit
        
        Hintergrundausführung der asynchronen Methode connect(), Übergabe des Queue-Objektes
        """
        try:
            logger.info(
                "Starting thread to device with address '%s' and name '%s'",
                self._mac_address, self._device_name)
            device = BluetoothConnection(self._queue, self._mac_address, self._device_name)
            Thread(target=asyncio.run, args=(device.connect(),), daemon=True).start()
        except Exception as e:
            logger.error(
                "Thread connection to device with address '%s' and name '%s' failed! Error: %s",
                self._mac_address, self._device_name, e)

    def get_thread_output(self):
        """
        Lesen der vom Thread abgelegten Daten aus der Queue
        
        Returns:
            dict: Dictionary der Daten aus der Bluetooth-Klasse
        """
        if self._queue.qsize() > 1:
            data = self._queue.sync_q.get(block=False, timeout=0)
            logger.info("Data from device with address '%s': %s", self._mac_address, data)
            return data
