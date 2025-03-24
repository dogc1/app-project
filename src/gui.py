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
    Eine Klasse, die ein GridLayout für die Darstellung von Temperaturwerten definiert.
    Hintergrundfarbe: Grün.

    __author__ = Jonas Jäger
    """
    def __init__(self, **kwargs):
        """
        Initialisiert das GridLayout für Temperatur mit einem grünen Hintergrund.

        Args:
            kwargs: Zusätzliche Argumente, die an den Initialisierer der Superklasse 
            weitergegeben werden.
        """
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0, 197/255, 145/255, 0.8)  # RGBA: Grün
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        """
        Aktualisiert die Größe und Position des Rechtecks bei Änderungen im Layout.

        Args:
            instance: Die aktuelle Instanz des Layouts.
            value: Der aktualisierte Wert (z. B. Größe oder Position).
        """
        self.rect.size = instance.size
        self.rect.pos = instance.pos

class GridHumidity(GridLayout):
    """
    Eine Klasse, die ein GridLayout für die Darstellung von Luftfeuchtigkeitswerten definiert.
    Hintergrundfarbe: Rot.

    __author__ = Jonas Jäger
    """
    def __init__(self, **kwargs):
        """
        Initialisiert das GridLayout für Luftfeuchtigkeit mit einem roten Hintergrund.

        Args:
            kwargs: Zusätzliche Argumente, die an den Initialisierer der Superklasse 
            weitergegeben werden.
        """
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(227/255, 47/255, 50/255, 0.8)  # RGBA: Rot
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        """
        Aktualisiert die Größe und Position des Rechtecks bei Änderungen im Layout.

        Args:
            instance: Die aktuelle Instanz des Layouts.
            value: Der aktualisierte Wert (z. B. Größe oder Position).
        """
        self.rect.size = instance.size
        self.rect.pos = instance.pos

class GridPressure(GridLayout):
    """
    Eine Klasse, die ein GridLayout für die Darstellung von Luftdruckwerten definiert.
    Hintergrundfarbe: Blau.

    __author__ = Jonas Jäger
    """
    def __init__(self, **kwargs):
        """
        Initialisiert das GridLayout für Luftdruck mit einem blauen Hintergrund.

        Args:
            kwargs: Zusätzliche Argumente, die an den Initialisierer der Superklasse 
            weitergegeben werden.
        """
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(22/255, 46/255, 255/255, 0.8)  # RGBA: Blau
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        """
        Aktualisiert die Größe und Position des Rechtecks bei Änderungen im Layout.

        Args:
            instance: Die aktuelle Instanz des Layouts.
            value: Der aktualisierte Wert (z. B. Größe oder Position).
        """
        self.rect.size = instance.size
        self.rect.pos = instance.pos

class GridDiagramm(GridLayout):
    """
    Eine Klasse, die ein allgemeines GridLayout für Diagramme definiert.
    Die Hintergrundfarbe wird dynamisch erstellt.

    __author__ = Jonas Jäger
    """
    def __init__(self, **kwargs):
        """
        Initialisiert das GridLayout für Diagramme mit einem dynamischen Hintergrund.

        Args:
            kwargs: Zusätzliche Argumente, die an den Initialisierer der Superklasse 
            weitergegeben werden.
        """
        super().__init__(**kwargs)
        with self.canvas.before:
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        """
        Aktualisiert die Größe und Position des Rechtecks bei Änderungen im Layout.

        Args:
            instance: Die aktuelle Instanz des Layouts.
            value: Der aktualisierte Wert (z. B. Größe oder Position).
        """
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


class DialogOne(Screen):
    """
    Ein Bildschirm, der verschiedene Diagramme (Temperatur, Luftfeuchtigkeit und Luftdruck)
    in einem scrollbaren Layout anzeigt. Jedes Diagramm zeigt Daten im Zeitverlauf mit 
    Markierungen für Tageswechsel.

    __author__ = Jonas Jäger
    """
    def __init__(self, **kwargs):
        """
        Initialisiert den DialogOne-Bildschirm mit einer scrollbaren Ansicht und 
        dynamisch generierten Diagrammen für Temperatur, Luftfeuchtigkeit und Luftdruck.

        Args:
            kwargs: Zusätzliche Argumente, die an den Initialisierer der Superklasse 
            weitergegeben werden.
        """
        super().__init__(**kwargs)
        scroll_view = ScrollView(size_hint=(1, 1))
        grid = GridDiagramm(cols=1, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        def add_fixed_height_plot(fig, grid, height=400):
            """
            Fügt ein Diagramm mit einer festen Höhe dem Raster hinzu.

            Args:
                fig: Die matplotlib-Figur, die dem Layout hinzugefügt werden soll.
                grid: Das Rasterlayout, zu dem die Figur hinzugefügt wird.
                height (int): Die Höhe der Figur in Pixeln.
            """
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
    Ein Bildschirm, der aktuelle Werte für Temperatur, Luftfeuchtigkeit und Luftdruck 
    in drei separaten Rasterlayouts anzeigt. Die Werte werden periodisch aktualisiert.

    __author__ = Jonas Jäger, Dario Gloc
    """
    def __init__(self, **kwargs):
        """
        Initialisiert den DialogTwo-Bildschirm mit einem vertikalen Layout, 
        das drei Raster enthält. Jedes Raster zeigt ein Label und einen dynamisch 
        aktualisierten Wert für Temperatur, Luftfeuchtigkeit und Luftdruck an.

        Args:
            kwargs: Zusätzliche Argumente, die an den Initialisierer der Superklasse 
            weitergegeben werden.
        """
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Erstes GridTemperature
        self.grid1 = GridTemperature(cols=1)
        self.grid1.add_widget(Label(text="Temperatur"))
        self.temperature = Label(text=" ".join(str(22,5)))
        self.grid1.add_widget(self.temperature)

        # Zweites GridHumidity
        self.grid2 = GridHumidity(cols=1)
        self.grid2.add_widget(Label(text="Luftfeuchtigkeit"))
        self.humidity = Label(text=" ".join(str(65,4)))
        self.grid2.add_widget(self.humidity)

        # Drittes GridPressure
        self.grid3 = GridPressure(cols=1)
        self.grid3.add_widget(Label(text="Luftdruck"))
        self.pressure = Label(text=" ".join(str(960,3)))
        self.grid3.add_widget(self.pressure)

        # GridLayouts zum BoxLayout hinzufügen
        layout.add_widget(self.grid1)
        layout.add_widget(self.grid2)
        layout.add_widget(self.grid3)
        self.add_widget(layout)
        
        Clock.schedule_interval(self._update, 5)

    def _update(self, dt):
        """
        Aktualisiert periodisch die angezeigten Werte für Temperatur, Luftfeuchtigkeit 
        und Luftdruck.

        Args:
            dt: Zeitintervall zwischen den Aktualisierungen.
        """
        global temperature, humidity, pressure
        self.temperature.text = " ".join(22,5)
        self.humidity.text = " ".join(65,4)
        self.pressure.text = " ".join(960,3)
        
class DialogThree(Screen):
    """
    Ein Bildschirm, der Verbindungsinformationen für das Bloothousegerät anzeigt. 
    Wenn das Bloothousegerät nicht verbunden ist, wird eine entsprechende Meldung angezeigt. 
    Aktualisiert die Verbindungsinformationen in regelmäßigen Abständen.

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
        """
        Aktualisiert die Verbindungsinformationen des Geräts und gibt 
        Debug-Informationen in der Konsole aus.

        Args:
            dt: Zeitintervall zwischen den Aktualisierungen.
        """
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
    Das Hauptlayout der Anwendung, das ein Menü und einen ScreenManager enthält.
    Über das Menü kann der Nutzer zwischen verschiedenen Dialogen navigieren.

    __author__ = Jonas Jäger
    """
    def __init__(self, **kwargs):
        """
        Initialisiert das Hauptlayout mit einem vertikalen Layout, einem Menü oben 
        und einem ScreenManager, der die dynamischen Inhalte verwaltet.

        Args:
            kwargs: Zusätzliche Argumente, die an den Initialisierer der Superklasse 
            weitergegeben werden.
        """
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Aktualisiert Daten in regelmäßigen Abständen
        Clock.schedule_interval(get_new_data, 5)

        # Menü oben
        menu_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        btn_dialog_one = Button(text="Wertentwicklung")
        btn_dialog_two = Button(text="Aktuelle Werte")
        btn_dialog_three = Button(text="Geräte Status")

        # Verknüpft die Buttons mit den entsprechenden Dialoganzeigen
        btn_dialog_one.bind(on_press=self.show_dialog_one)
        btn_dialog_two.bind(on_press=self.show_dialog_two)
        btn_dialog_three.bind(on_press=self.show_dialog_three)

        # Buttons zum Menü-Layout hinzufügen
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
        """
        Zeigt den Dialog "Wertentwicklung" im ScreenManager an.

        Args:
            instance: Die Instanz des gedrückten Buttons.
        """
        self.screen_manager.current = "dialog_one"

    def show_dialog_two(self, instance):
        """
        Zeigt den Dialog "Aktuelle Werte" im ScreenManager an.

        Args:
            instance: Die Instanz des gedrückten Buttons.
        """
        self.screen_manager.current = "dialog_two"

    def show_dialog_three(self, instance):
        """
        Zeigt den Dialog "Geräte Status" im ScreenManager an.

        Args:
            instance: Die Instanz des gedrückten Buttons.
        """
        self.screen_manager.current = "dialog_three"

class AppMain(App):
    """
    Die Hauptanwendung, die das Hauptlayout erstellt und die Geräteverbindung initiiert.

    __author__ = Jonas Jäger
    """
    def build(self):
        """
        Baut das Hauptlayout der Anwendung auf und startet die Verbindung zum Gerät.

        Returns:
            MainLayout: Das Hauptlayout der Anwendung.
        """
        self.title = 'Total mess'
        Clock.schedule_once(connect_device, 0)
        return MainLayout()
