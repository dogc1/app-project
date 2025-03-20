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

class GridTemperature(GridLayout):
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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
        
temperatureY = [25.49, 25.46, 25.42, 25.39, 25.30, 25.23, 25.04, 24.93, 24.83, 24.77, 24.64, 24.42, 24.40, 24.39, 24.37, 24.36, 24.36, 24.33, 24.33, 24.32]
start_time = datetime.now().replace(hour=23, minute=0, second=0, microsecond=0)
timestamps = [start_time + timedelta(minutes=30 * i) for i in range(20)]

class DialogOne(Screen):
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
        ax.plot(timestamps, temperatureY, label="Temperatur")
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
        ax2.plot(timestamps, temperatureY, label="Luftfeuchtigkeit")
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
        ax3.plot(timestamps, temperatureY, label="Luftdruck")
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


humidity = 67.54
temperature = 24.93
presser = 980.4
elements = ["Gerät 1", "Gerät 2", "Gerät 3"]

class DialogTwo(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Erstes GridTemperature
        grid1 = GridTemperature(cols=1)
        grid1.add_widget(Label(text="Temperatur"))
        grid1.add_widget(Label(text=str(temperature) + "°C" ))

        # Zweites GridHumidity
        grid2 = GridHumidity(cols=1)
        grid2.add_widget(Label(text="Luftfeuchtigkeit"))
        grid2.add_widget(Label(text= str(humidity) + "%"))

        # Drittes GridPressure
        grid3 = GridPressure(cols=1)
        grid3.add_widget(Label(text="Luftdruck"))
        grid3.add_widget(Label(text=str(humidity) + "hPa"))

        # GridLayouts zum BoxLayout hinzufügen
        layout.add_widget(grid1)
        layout.add_widget(grid2)
        layout.add_widget(grid3)
        self.add_widget(layout)

class DialogThree(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        # Dynamisch Widgets hinzufügen
        for item in elements:
            layout.add_widget(Label(text=item))

        self.add_widget(layout)
        
        # Beispiel: Hinzufügen einer Schaltfläche, um weitere Elemente zu generieren

    def add_bluetooth_device(self):
        layout = BoxLayout(orientation='vertical')        
        # layout.add_widget(Label(text=listeofConnections))
        self.add_widget(layout)

# Definition des Hauptlayouts
class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Menü oben
        menu_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        btn_dialog_one = Button(text="Wertentwicklung")
        btn_dialog_two = Button(text="Aktuelle Werte")
        btn_dialog_three = Button(text="Einstellungen")
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
    def build(self):
        self.title = 'Total mess'
        return MainLayout()
    