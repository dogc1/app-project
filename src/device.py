from bluetooth import BluetoothConnection
from threading import Thread
from culsans import Queue
import asyncio
import logging

logger = logging.getLogger("Device")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class DeviceCommunication:
    def __init__(self, mac_address, device_name = ""):
        self._mac_address = mac_address
        self._device_name = device_name
        self._device_connection: BluetoothConnection
        self._data = dict()
        self._queue = Queue()
        self._thread = None
        
    def run_thread(self):
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
        if self._queue.qsize() > 1:
            data = self._queue.sync_q.get(block=False, timeout=0)
            logger.info("Data from device with address '%s': %s", self._mac_address, data)
            return data
