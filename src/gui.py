from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.matplotlib import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from kivy.uix.scrollview import ScrollView

from MockDaten import MockupDaten

from kivy.clock import Clock
from device import DeviceCommunication

plt.set_loglevel("ERROR")

temperature = tuple()
humidity = tuple()
pressure = tuple()

elements = ["Gerät 1"]
connected = False
name = ""
address = ""

device = DeviceCommunication("08:F9:E0:F4:7B:3A", "GSOG_SENSOR1")
def connect_device(dt):
    """
    __author__ = Dario Gloc
    Starten des nebenläufigen Threads der Bluetoothverbindung zum Gerät

    Parameters:
        dt: delta-time für scheduling events
    """
    device.run_thread()

def get_new_data(dt):
    """
    __author__ = Dario Gloc, Tahir Bulut
    Scheduled function zum Erhalt der aktualisierten Daten der Bluetoothverbindung 
    Beschreiben der globalen Variablen zur Anzeige auf der GUI

    Parameters:
        dt: delta-time für scheduling events
    """
    global humidity, temperature, pressure, connected, address, name
    data = device.get_thread_output()
   
    if data is not None:
        temperature = data["Temperature"]
        humidity = data["Humidity"]
        pressure = data["Pressure"]
        connected = data["Connected"]
        address = data["Address"]
        name = data["Name"]

class GridTemperature(GridLayout):
    """
    __author__ = Jonas Jäger
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0, 197/255, 145/255, 0.8)  # RGBA: Grün
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

class GridHumidity(GridLayout):
    """
    __author__ = Jonas Jäger
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(227/255, 47/255, 50/255, 0.8)  # RGBA: Rot
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

class GridPressure(GridLayout):
    """
    __author__ = Jonas Jäger
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(22/255, 46/255, 255/255, 0.8)  # RGBA: Blau
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

class GridDiagramm(GridLayout):
    """
    __author__ = Jonas Jäger
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
        
mockup = MockupDaten()
geraet, geratedDatas = mockup.greateDatas()

# Listen für die extrahierten Werte
timestamps = [messung.datum for messung in geratedDatas]
timestamps = [datetime.strptime(ts, "%d.%m.%Y %H:%M") for ts in timestamps]
temperaturen = [messung.temperatur for messung in geratedDatas]
luftfeuchtigkeiten = [messung.luftfeuchtigkeit for messung in geratedDatas]
luftdruecke = [messung.luftdruck for messung in geratedDatas]

temperatureY = [25.49, 25.46, 25.42, 25.39, 25.30, 25.23, 25.04, 24.93, 24.83, 24.77, 24.64, 24.42, 24.40, 24.39, 24.37, 24.36, 24.36, 24.33, 24.33, 24.32]
start_time = datetime.now().replace(hour=23, minute=0, second=0, microsecond=0)

class DialogOne(Screen):
    """
    __author__ = Jonas Jäger
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        scroll_view = ScrollView(size_hint=(1, 1))
        grid = GridDiagramm(cols=1, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        def add_fixed_height_plot(fig, grid, height=400):
            canvas = FigureCanvasKivyAgg(fig)
            canvas.size_hint_y = None  # Deaktiviert automatische Höhenanpassung
            canvas.height = height  # Setzt fixe Höhe
            grid.add_widget(canvas)

        # Temperatur
        fig, ax = plt.subplots()
        ax.plot(timestamps, temperaturen, label="Temperatur")
        ax.set_title("Temperatur")
        ax.set_xlabel("Zeit")
        ax.set_ylabel("Temperatur °C")
        for i, ts in enumerate(timestamps):
            if ts.date() != timestamps[0].date():  # Wenn das Datum sich ändert
                ax.axvline(ts, color='red', linestyle='--', label='Tageswechsel')
                break  # Nur eine Linie einfügen (kannst du anpassen)
        ax.legend()
        add_fixed_height_plot(fig, grid, height=400)
        grid.add_widget(FigureCanvasKivyAgg(fig))

        # Luftfeuchtigkeit
        fig2, ax2 = plt.subplots()
        ax2.plot(timestamps, luftfeuchtigkeiten, label="Luftfeuchtigkeit")
        ax2.set_title("Luftfeuchtigkeit")
        ax2.set_xlabel("Zeit")
        ax2.set_ylabel("Luftfeuchtigkeit %")
        for i, ts in enumerate(timestamps):
            if ts.date() != timestamps[0].date():  # Wenn das Datum sich ändert
                ax2.axvline(ts, color='red', linestyle='--', label='Tageswechsel')
                break  # Nur eine Linie einfügen (kannst du anpassen)
        ax2.legend()
        add_fixed_height_plot(fig2, grid, height=400)
        grid.add_widget(FigureCanvasKivyAgg(fig2))

        # Luftdruck
        fig3, ax3 = plt.subplots()
        ax3.plot(timestamps, luftdruecke, label="Luftdruck")
        ax3.set_title("Luftdruck")
        ax3.set_xlabel("Zeit")
        ax3.set_ylabel("Luftdruck hPa")
        for i, ts in enumerate(timestamps):
            if ts.date() != timestamps[0].date():  # Wenn das Datum sich ändert
                ax3.axvline(ts, color='red', linestyle='--', label='Tageswechsel')
                break  # Nur eine Linie einfügen (kannst du anpassen)
        ax3.legend()
        add_fixed_height_plot(fig3, grid, height=400)
        grid.add_widget(FigureCanvasKivyAgg(fig3))

        scroll_view.add_widget(grid)
        self.add_widget(scroll_view)

class DialogTwo(Screen):
    """
    __author__ = Jonas Jäger, Dario Gloc
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Erstes GridTemperature
        self.grid1 = GridTemperature(cols=1)
        self.grid1.add_widget(Label(text="Temperatur"))
        self.temperature = Label(text=" ".join(temperature))
        self.grid1.add_widget(self.temperature)

        # Zweites GridHumidity
        self.grid2 = GridHumidity(cols=1)
        self.grid2.add_widget(Label(text="Luftfeuchtigkeit"))
        self.humidity = Label(text=" ".join(humidity))
        self.grid2.add_widget(self.humidity)

        # Drittes GridPressure
        self.grid3 = GridPressure(cols=1)
        self.grid3.add_widget(Label(text="Luftdruck"))
        self.pressure = Label(text=" ".join(pressure))
        self.grid3.add_widget(self.pressure)

        # GridLayouts zum BoxLayout hinzufügen
        layout.add_widget(self.grid1)
        layout.add_widget(self.grid2)
        layout.add_widget(self.grid3)
        self.add_widget(layout)
        
        Clock.schedule_interval(self._update, 5)

    def _update(self, dt):
        global temperature, humidity, pressure
        self.temperature.text = " ".join(temperature)
        self.humidity.text = " ".join(humidity)
        self.pressure.text = " ".join(pressure)
        
class DialogThree(Screen):
    """
    __author__ = Jonas Jäger, Tahir Bulut
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.label_device_info = Label(
            text="[color=ff0000]Nicht verbunden[/color]",
            halign="left",
            valign="top",
            markup=True
        )
        self.layout.add_widget(self.label_device_info)
        self.add_widget(self.layout)

        self._no_data_counter = 0
        self._last_data = None

        Clock.schedule_interval(self.update_device_info, 5)

    def update_device_info(self, dt):
        global connected, address, name

        print("XXXXXXXXXX", connected)
        print("XXXXXXXXXX", name)
        print("XXXXXXXXXX", address)

        # Wenn kein neues Data kommt, zeige letzten bekannten Status
        if connected and address is not None and name is not None:
            # Verbindung als aktiv ansehen, wenn in den letzten 2 Intervallen Daten kamen
            status = "[color=00ff00]Verbunden[/color]"
            
            info_text = (
                f"[b]Verbundene Gerätedaten:[/b]\n"
                f"Name: {name}\n"
                f"MAC-Adresse: {address}\n"
                f"Status: {status}\n"
            )
            self.label_device_info.text = info_text

class MainLayout(BoxLayout):
    """
    __author__ = Jonas Jäger
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        Clock.schedule_interval(get_new_data, 5)

        # Menü oben
        menu_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        btn_dialog_one = Button(text="Wertentwicklung")
        btn_dialog_two = Button(text="Aktuelle Werte")
        btn_dialog_three = Button(text="Geräte Status")
        btn_dialog_one.bind(on_press=self.show_dialog_one)
        btn_dialog_two.bind(on_press=self.show_dialog_two)
        btn_dialog_three.bind(on_press=self.show_dialog_three)
        menu_layout.add_widget(btn_dialog_one)
        menu_layout.add_widget(btn_dialog_two)
        menu_layout.add_widget(btn_dialog_three)
        self.add_widget(menu_layout)

        # ScreenManager für dynamische Inhalte
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(DialogOne(name="dialog_one"))
        self.screen_manager.add_widget(DialogTwo(name="dialog_two"))
        self.screen_manager.add_widget(DialogThree(name="dialog_three"))
        self.add_widget(self.screen_manager)

    def show_dialog_one(self, instance):
        self.screen_manager.current = "dialog_one"

    def show_dialog_two(self, instance):
        self.screen_manager.current = "dialog_two"

    def show_dialog_three(self, instance):
        self.screen_manager.current = "dialog_three"

class AppMain(App):
    """
    __author__ = Jonas Jäger
    """
    def build(self):
        self.title = 'Total mess'
        Clock.schedule_once(connect_device, 0)
        return MainLayout()
