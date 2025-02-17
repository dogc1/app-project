from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel


class Gui(MDApp):

    def build(self):
        # Todo: Dark/Teal-Theme
        #self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Dark"
        return (
            MDScreen(
                MDLabel(
                    text="MDLabel",
                    halign="center",
                    text_color= "white",
                ),
                md_bg_color=self.theme_cls.backgroundColor,
            )
        )

if __name__ == "__main__":
    Gui().run()                                                                                                                                                                         