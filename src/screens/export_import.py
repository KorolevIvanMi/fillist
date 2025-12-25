from kivy.uix.settings import text_type
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import ObjectProperty

from utils.helpers import get_resource_path
from utils.export_import import *

class ExportImportMenu(FloatLayout):

    container_dyn = ObjectProperty(None)
    file_path_txt = ObjectProperty(None)
    file_name_txt = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.normal_home_res = get_resource_path('resources/images/buttons/Home_btn.png')
        self.down_home_res = get_resource_path('resources/images/buttons/Home_btn_down.png')
        
    def go_to_home(self):
        app = App.get_running_app()
        app.root.current = "welcomeScreen"

    def export_data(self):
        file_path = self.file_path_txt.text
        file_name = self.file_name_txt.text

        export(file_path, file_name)
    
    def import_data(self):
        file_path = self.file_path_txt.text
        file_name = self.file_name_txt.text
        
        import_films(file_path, file_name)
        
