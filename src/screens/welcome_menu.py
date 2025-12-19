from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.app import App
from utils.helpers import * 
class WelcomeMenu(FloatLayout):
    main_menu_btn = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.normal_prof_res = get_resource_path('resources/images/buttons/Profile_btn.png')
        self.down_prof_res = get_resource_path('resources/images/buttons/Profile_btn_down.png')

    def go_to_main_menu(self):
        app = App.get_running_app()
        app.root.current = "mainScreen"

    