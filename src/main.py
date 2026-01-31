from utils.config import *
screen_confirguration()

from kivy.app import App
from kivy.lang import Builder
import os
from kivy.uix.screenmanager import ScreenManager, Screen
from screens.main_menu import FillistMainMenu
from screens.add_film import AddFilmMenu
from screens.edit_film import RedactFilmMenu
from screens.welcome_menu import WelcomeMenu
from screens.settings_menu import SettingsMenu
from screens.export_import import ExportImportMenu
from screens.profile import ProfileMenu
from utils.helpers import *
from kivy.core.text import LabelBase
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty

class profileScreen(Screen):
    pass

class exportImportScreen(Screen):
    pass

class settingsScreen(Screen):
    pass 

class welcomeScreen(Screen):
    pass

class mainScreen(Screen):
    pass

class AddFilmMenuScreen(Screen):
    pass

class RedactFilmMenuScreen(Screen):
    def on_enter(self, *args):
        # Этот метод вызывается автоматически при входе на экран
        if self.ids.redact_film_menu:  # Проверяем, что виджет существует
            self.ids.redact_film_menu.setup_all_data()

@bind_keyboard_to_app
class FillistApp(App):
    data_updated = BooleanProperty(False)
    film_to_redact = NumericProperty(-1)
    
    def build(self):
        # загрузка шрифтов
        font_path1 = get_resource_path('resources/fonts/FreeCheese-Regular.otf')
        font_path2 = get_resource_path('resources/fonts/Guidy.ttf')

        LabelBase.register(name='FreeCheese', fn_regular=font_path1)
        LabelBase.register(name='Guidy', fn_regular=font_path2)

        # загрузка файлов kv
        load_kv_file('resources/kv/screens/add_film.kv')
        load_kv_file('resources/kv/screens/edit_film.kv')
        load_kv_file('resources/kv/screens/main_menu.kv')
        load_kv_file('resources/kv/screens/welcome_menu.kv')
        load_kv_file('resources/kv/screens/settings_menu.kv')
        load_kv_file('resources/kv/screens/export_import.kv')
        load_kv_file('resources/kv/screens/profile.kv')
        load_kv_file('resources/kv/widgets/scrolling_menu.kv') 
        load_kv_file('resources/kv/widgets/rating.kv')
        load_kv_file('resources/kv/widgets/dropdown.kv')
        load_kv_file('resources/kv/widgets/layout.kv')
        load_kv_file('resources/kv/widgets/warning.kv')
        load_kv_file('resources/kv/widgets/profile_image.kv')

        sm = ScreenManager()
        sm.add_widget(welcomeScreen())
        sm.add_widget(mainScreen())
        sm.add_widget(AddFilmMenuScreen())
        sm.add_widget(RedactFilmMenuScreen())
        sm.add_widget(settingsScreen())
        sm.add_widget(exportImportScreen())
        sm.add_widget( profileScreen())
        return sm



if __name__ == '__main__':
    print("Версия 1.1.1 запущена!!")
    FillistApp().run()