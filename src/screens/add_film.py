from kivy.uix.behaviors.touchripple import Color

from kivy.lang import Builder
from utils.helpers import *

from widgets.dropdown import StatusDropdownAdd
from kivy.uix.widget import Widget
from widgets.warning import WarningForAdd
from kivy.properties import ObjectProperty, ListProperty
from kivy.app import App

from kivy.clock import Clock
from database import myDataBase
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout




class AddFilmMenu(FloatLayout):


    
    db = myDataBase()
    status_button = ObjectProperty(None)
    status_dropdown = None
    film_name_txt = ObjectProperty(None)
    film_genre_txt = ObjectProperty(None)
    film_description_txt =  ObjectProperty(None)
    rating_layout = ObjectProperty(None)
    
    


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        
        self.normal_apl_res = get_resource_path('resources/images/buttons/Apply_btn.png')
        self.down_apl_res = get_resource_path('resources/images/buttons/Apply_btn_down.png')
        self.normal_get_back_res = get_resource_path('resources/images/buttons/Get_back_btn.png')
        self.down_get_back_res = get_resource_path('resources/images/buttons/Get_back_btn_down.png')

        self.setup_status_dropdown()



    
        
    def acceptOnRelease(self):
        film_name = self.film_name_txt.text
        film_genre = self.film_genre_txt.text
        film_status = self.status_button.text
        film_rating = self.rating_layout.selected_rating
        film_discription = self.film_description_txt.text

        

        isfilmin = self.db.add_film_to_bd(film_name, film_genre, film_status, film_rating, film_discription)
        if (isfilmin == 1):
            app = App.get_running_app()

            app.data_updated = True
            app.root.current = "mainScreen"
        else:

            self.my_warning = WarningForAdd()
            self.my_warning.pos_hint = {"x":0.4, "y": -0.1}
            self.my_warning.size_hint = 0.2, 0.03
            if isfilmin == 0:
                self.my_warning.label_text = "Фильм уже существует!" 
            elif isfilmin == 2:
                self.my_warning.label_text = "Нужно выбрать статус!"    
            elif isfilmin == 3:
                self.my_warning.label_text = "Нужно ввести название!"
            elif isfilmin == 4:
                self.my_warning.label_text = "Нужно ввести жанр!"
            self.add_widget(self.my_warning)        
        
            self.my_warning.appearing(callback= self.remove_warning)
            
    def remove_warning(self, *args):
            # Проверяем, что виджет еще существует
            if self.my_warning and self.my_warning in self.children:
                self.remove_widget(self.my_warning)

    def getBackOnRelease(self):
        app = App.get_running_app()
        app.root.current = "mainScreen"

    def setup_status_dropdown(self):
        #Настройка dropdown для статуса
        self.status_dropdown = StatusDropdownAdd()
        self.status_dropdown.bind(on_select=self.on_status_select)

    def open_status_dropdown(self):
        
        #Открывает dropdown статуса
        if self.status_dropdown and self.status_button:
            self.status_dropdown.open(self.status_button)
    def on_status_select(self, instance, value):
        if value == self.status_button.text:
            self.status_button.text = "Все"
        else:
        # Обновляем текст кнопки на выбранный статус
            if self.status_button:
                self.status_button.text = value
    def on_rating_selected(self, value):
        print(f"Выбран рейтинг: {value}")