from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.app import App
from utils.helpers import * 
from utils.export_import import export
from utils.user_service import is_log_in
from widgets.warning import WarningForAdd

class WelcomeMenu(FloatLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.normal_prof_res = get_resource_path('resources/images/buttons/Profile_btn.png')
        self.down_prof_res = get_resource_path('resources/images/buttons/Profile_btn_down.png')
        
    @is_log_in
    def go_to_main_menu(self):
        app = App.get_running_app()
        app.root.current = "mainScreen"
    
    def go_to_settings_menu(self):
        app = App.get_running_app()
        app.root.current = "settingsScreen"
    @is_log_in
    def go_to_export_import_menu(self):
        app = App.get_running_app()
        app.root.current = "exportImportScreen"

    def go_to_profile_menu(self):
        app = App.get_running_app()
        app.root.current = "ProfileScreen"
    
    def spawn_warning(self):
        self.my_warning = WarningForAdd()
        self.my_warning.pos_hint = {"x":0.4, "y": -0.1}
        self.my_warning.size_hint = 0.2, 0.03
        self.my_warning.label_text = "Необходимо авторизоваться"
        self.add_widget(self.my_warning)        
        
        self.my_warning.appearing(callback= self.remove_warning)
            
    def remove_warning(self, *args):
            # Проверяем, что виджет еще существует
            if self.my_warning and self.my_warning in self.children:
                self.remove_widget(self.my_warning)