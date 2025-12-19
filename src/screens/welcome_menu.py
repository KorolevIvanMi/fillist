from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.app import App

class WelcomeMenu(FloatLayout):
    main_menu_btn = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def go_to_main_menu(self):
        app = App.get_running_app()
        app.root.current = "mainScreen"

    