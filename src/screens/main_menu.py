from kivy.uix.widget import Widget
from widgets.layout import myLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.app import App
from utils.helpers import get_resource_path 
from utils.user_service import is_log_in

class CustomButtonToGoToOtherScreen(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.normal_source = get_resource_path("resources/images/buttons/Add_btn.png")  
        self.down_source = get_resource_path("resources/images/buttons/Add_btn_down.png")

        self.source = self.normal_source
        self.is_active = False
        
        app = App.get_running_app()
        if app:
            app.main_menu = self
    def on_state(self, instance, value):
        if value == 'down':
            # Кнопка нажата, но еще не отпущена
            self.source = self.down_source
        else:
            self.source = self.normal_source
    
class FillistMainMenu(FloatLayout):
    # переход на экран добавления фильма
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.normal_home_res = get_resource_path('resources/images/buttons/Home_btn.png')
        self.down_home_res = get_resource_path('resources/images/buttons/Home_btn_down.png')
    
    def go_to_addScreen(self):
        app = App.get_running_app()
        app.root.current = "AddFilmMenuScreen"
    def go_to_home(self):
        app = App.get_running_app()
        app.root.current = "welcomeScreen"