from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from utils.helpers import get_resource_path
from database import myDataBase
from kivy.properties import ObjectProperty
from widgets.warning import WarningForAdd


class ProfileMenu(FloatLayout):

    db = myDataBase()
    login_txt = ObjectProperty(None)
    password_txt = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.normal_home_res = get_resource_path('resources/images/buttons/Home_btn.png')
        self.down_home_res = get_resource_path('resources/images/buttons/Home_btn_down.png')
        
    def go_to_home(self):
        app = App.get_running_app()
        app.root.current = "welcomeScreen"

    def on_enter_btn(self):
        password = self.password_txt.text
        login = self.login_txt.text
        res = self.db.log_in(password, login)
        print(res)
        if res == 0:
            self.spawn_warning("Такого пользователя нет")


    def spawn_warning(self, warning_text):
        self.my_warning = WarningForAdd()
        self.my_warning.pos_hint = {"x":0.4, "y": -0.1}
        self.my_warning.size_hint = 0.2, 0.03
        self.my_warning.label_text = warning_text
        self.add_widget(self.my_warning)        
        
        self.my_warning.appearing(callback= self.remove_warning)
            
    def remove_warning(self, *args):
            # Проверяем, что виджет еще существует
            if self.my_warning and self.my_warning in self.children:
                self.remove_widget(self.my_warning)

    def on_exit_release(self):
        self.login_txt.text = ""
        self.password_txt.text = ""
        self.db.log_out()

    def on_register_release(self):
        password = self.password_txt.text
        login = self.login_txt.text   
        self.db.register(login, password)