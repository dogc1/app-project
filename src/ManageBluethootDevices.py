import json
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup


class Device:
    def __init__(self, device_name, mac_address):
        self.device_name = device_name
        self.mac_address = mac_address

    def to_dict(self):
        return {
            "device_name": self.device_name,
            "mac_address": self.mac_address
        }


class BluetoothDeviceManager:
    def __init__(self):
        self.devices = self.load_devices()

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
        with open('devices.json', 'w') as f:
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


class DeviceManagerApp(App):
    def build(self):
        self.manager = BluetoothDeviceManager()
        self.layout = BoxLayout(orientation='vertical')

        self.scrollview = ScrollView()
        self.grid_layout = GridLayout(cols=1, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        self.load_devices_list()

        self.scrollview.add_widget(self.grid_layout)
        self.layout.add_widget(self.scrollview)

        return self.layout

    def load_devices_list(self):
        """Lädt alle Geräte und zeigt sie in der Kivy-Oberfläche an."""
        self.grid_layout.clear_widgets()  # Clear previous widgets
        for device in self.manager.devices:
            device_name = device['device_name']
            mac_address = device['mac_address']
            
            device_label = Label(text=f"{device_name} ({mac_address})")
            connect_button = Button(text="Verbinden", size_hint_y=None, height=40)
            remove_button = Button(text="Löschen", size_hint_y=None, height=40)

            connect_button.bind(on_press=lambda instance, mac=mac_address: self.connect_device(mac))
            remove_button.bind(on_press=lambda instance, mac=mac_address: self.remove_device(mac))

            self.grid_layout.add_widget(device_label)
            self.grid_layout.add_widget(connect_button)
            self.grid_layout.add_widget(remove_button)

    def connect_device(self, mac_address):
        """Verbindet sich mit dem Gerät anhand der MAC-Adresse."""
        print(f"Verbinde mit Gerät: {mac_address}")
        # Hier können Sie das Verbindungslogik implementieren, z.B. mit `Bleak` oder ähnlichem

    def remove_device(self, mac_address):
        """Löscht das Gerät aus der Liste und der Datei."""
        self.manager.remove_device(mac_address)
        self.load_devices_list()  # Aktualisiere die Anzeige nach dem Löschen


if __name__ == '__main__':
    DeviceManagerApp().run()
