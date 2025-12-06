from kivy.lang import Builder
from utils import *

from myDropDownAddAndRedact import StatusDropdownAdd, CustomDropdownButtonAdd
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.app import App

from kivy.clock import Clock
from myDataBase import myDataBase
from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.uix.dropdown import DropDown




class AddFilmMenu(Widget):
    
    db = myDataBase()
    status_button = ObjectProperty(None)
    status_dropdown = None
    film_name_txt = ObjectProperty(None)
    film_genre_txt = ObjectProperty(None)
    film_description_txt =  ObjectProperty(None)
    rating_layout = ObjectProperty(None)
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.normal_apl_res = get_resource_path('images/buttons/Apply_btn.png')
        self.down_apl_res = get_resource_path('images/buttons/Apply_btn_down.png')
        self.normal_get_back_res = get_resource_path('images/buttons/Get_back_btn.png')
        self.down_get_back_res = get_resource_path('images/buttons/Get_back_btn_down.png')

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
            

    def getBackOnRelease(self):
        app = App.get_running_app()
        app.root.current = "mainScreen"

    def setup_status_dropdown(self):
        #Настройка dropdown для статуса
        self.status_dropdown = StatusDropdownAdd()
        self.status_dropdown.bind(on_select=self.on_status_select)

    def open_status_dropdown(self):
        print("Open dropDown")
        #Открывает dropdown статуса
        if self.status_dropdown and self.status_button:
            self.status_dropdown.open(self.status_button)
    def on_status_select(self, instance, value):

        # Обновляем текст кнопки на выбранный статус
        if self.status_button:
            self.status_button.text = value
    def on_rating_selected(self, value):
       
        print(f"Выбран рейтинг: {value}")