from kivy.uix.widget import Widget
from myLayout import myLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.app import App
from utils import get_resource_path 

class CustomButtonToGoToOtherScreen(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.normal_source = get_resource_path("images/buttons/Add_btn.png")  
        self.down_source = get_resource_path("images/buttons/Add_btn_down.png")

        self.source = self.normal_source
        self.is_active = False

    def on_state(self, instance, value):
        if value == 'down':
            # Кнопка нажата, но еще не отпущена
            self.source = self.down_source
        else:
            self.source = self.normal_source
    
class FillistMainMenu(Widget):
    # переход на экран добавления фильма
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.normal_export_res = get_resource_path('images/buttons/Export_btn.png')
        self.down_export_res = get_resource_path('images/buttons/Export_btn_down.png')
    def go_to_addScreen(self):
        app = App.get_running_app()
        app.root.current = "AddFilmMenuScreen"