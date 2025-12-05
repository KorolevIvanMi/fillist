from kivy.config import Config

Config.set('graphics', 'fullscreen', '0')  
Config.set('graphics', 'resizable', '1')



from kivy.app import App
from kivy.lang import Builder
import os

from kivy.uix.screenmanager import ScreenManager, Screen
from FillistMainMenu import FillistMainMenu
from addFilmMenu import AddFilmMenu
from redactFilmMenu import RedactFilmMenu
from utils import load_kv_file
from utils import get_resource_path
from kivy.core.text import LabelBase
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty

class mainScreen(Screen):
    pass

class AddFilmMenuScreen(Screen):
    pass

class RedactFilmMenuScreen(Screen):
    def on_enter(self, *args):
        # Этот метод вызывается автоматически при входе на экран
        if self.ids.redact_film_menu:  # Проверяем, что виджет существует
            self.ids.redact_film_menu.setup_all_data()

class FillistApp(App):
        data_updated = BooleanProperty(False)
        film_to_redact = NumericProperty(-1)
        
        def build(self):
            
        # загрузка шрифтов
            font_path1 = get_resource_path('fonts/FreeCheese-Regular.otf')
            font_path2 = get_resource_path('fonts/Guidy.ttf')

            LabelBase.register(name='FreeCheese', fn_regular=font_path1)
            LabelBase.register(name='Guidy', fn_regular=font_path2)

        # загрузка файлов kv
            load_kv_file('design/fillist.kv')
            load_kv_file('design/myScrolingMenu.kv') 
            load_kv_file('design/myRating.kv')
            load_kv_file('design/myDropDown.kv')
            load_kv_file('design/myLayout.kv')
            load_kv_file('design/addFilmMenu.kv')
            load_kv_file('design/redactFilmMenu.kv')
            load_kv_file('design/myDropDownAddAndRedact.kv')

        
            sm = ScreenManager()
            sm.add_widget(mainScreen())
            sm.add_widget(AddFilmMenuScreen())
            sm.add_widget(RedactFilmMenuScreen())
            return sm

if __name__ == '__main__':
    
    FillistApp().run()