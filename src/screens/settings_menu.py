from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from utils.helpers import get_resource_path


class SettingsMenu(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.normal_home_res = get_resource_path('resources/images/buttons/Home_btn.png')
        self.down_home_res = get_resource_path('resources/images/buttons/Home_btn_down.png')
        
    def go_to_home(self):
        app = App.get_running_app()
        app.root.current = "welcomeScreen"