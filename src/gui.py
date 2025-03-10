from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle

# Definition der Bildschirme

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

class DialogOne(Screen):
    # def __init__(self, **kwargs):
    #     layout = BoxLayout()
    #     # Matplotlib-Diagramm erstellen
    #     fig, ax = plt.subplots()
    #     ax.plot([1, 2, 3], [4, 5, 6], label="Beispielkurve")
    #     ax.set_title("Einfaches Diagramm")
    #     ax.legend()

    #     # Diagramm als Widget hinzufügen
    #     layout.add_widget(FigureCanvasKivyAgg(fig))
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text="Dies ist Dialog 1"))
        self.add_widget(layout)

class DialogTwo(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Erstes GridTemperature
        grid1 = GridTemperature(cols=1)
        grid1.add_widget(Label(text="Temperatur"))
        grid1.add_widget(Label(text="Temperatur Wert"))

        # Zweites GridHumidity
        grid2 = GridHumidity(cols=1)
        grid2.add_widget(Label(text="Luftfeuchtigkeit"))
        grid2.add_widget(Label(text="Feuchtigkeits Wert"))

        # Drittes GridPressure
        grid3 = GridPressure(cols=1)
        grid3.add_widget(Label(text="Luftdruck"))
        grid3.add_widget(Label(text="Luftdruck Wert"))

        # GridLayouts zum BoxLayout hinzufügen
        layout.add_widget(grid1)
        layout.add_widget(grid2)
        layout.add_widget(grid3)
        self.add_widget(layout)

class DialogThree(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text="Dies ist Dialog 3"))
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

class MyApp(App):
    def build(self):
        return MainLayout()


if __name__ == "__main__":
    # Gui().run()
    MyApp().run()