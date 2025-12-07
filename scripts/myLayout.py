from kivy.uix.settings import text_type
from kivy.app import App
from kivy.lang import Builder
import os
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.clock import Clock
from myDropDown import StatusDropdown
from myRating import CustomLayotForRating
from myDataBase import myDataBase
from myScrolingMenu import RV, StatefulLabel, MyRecycleGridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from customButtonWith2States import CustomButtonWith2States
from utils import *


class myLayout(FloatLayout):
    
    db = myDataBase()
    rating_layout = ObjectProperty(None)
    
    search_text = ObjectProperty(None)
    status_dropdown = None
    status_button = ObjectProperty(None)
    scroll_menu = ObjectProperty(None) 
    


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.normal_apl_res = get_resource_path('images/buttons/Apply_btn.png')
        self.down_apl_res = get_resource_path('images/buttons/Apply_btn_down.png')
        self.normal_del_res = get_resource_path('images/buttons/Delete_btn.png')
        self.down_del_res = get_resource_path('images/buttons/Delete_btn_down.png')
        self.normal_search_res = get_resource_path('images/buttons/Search_btn.png')
        self.down_search_res = get_resource_path('images/buttons/Search_btn_down.png')
        self.normal_decrease_res = get_resource_path('images/buttons/Decrease_btn.png')
        self.down_decrease_res = get_resource_path('images/buttons/Decrease_btn_down.png')
        self.normal_increase_res = get_resource_path('images/buttons/increase_btn.png')
        self.down_increase_res = get_resource_path('images/buttons/increase_btn_down.png')

        self.setup_status_dropdown()
        Clock.schedule_once(self.setup_scroling_menu, 0.1)

        app = App.get_running_app()
        app.bind(data_updated=self.on_data_updated)

    def on_data_updated(self, instance, value):
        
        if value:  # Если флаг стал True
            print("Обнаружено обновление данных, обновляю список...")
            self.refresh_data()
            # Сбрасываем флаг обратно
            app = App.get_running_app()
            app.data_updated = False

    def refresh_data(self):
        """Обновление данных из базы"""
        data_from_db = self.db.get_all_films()
        if self.scroll_menu:
            self.scroll_menu.update_data(data_from_db)
            print("Данные успешно обновлены")
        
# Поиск по названию
    def searchOnPress(self):
        text_to_find = self.search_text.text
        self.search_text.text = ""
        print("Search in progress...")
        s = self.db.find_film_by_name(text_to_find)
        if(text_to_find == "" or text_to_find == "all"):
            data_from_db = self.db.get_all_films()
            self.scroll_menu.update_data(data_from_db)
        else:
            self.scroll_menu.update_data(s)

# обработка dropdown меню
    def setup_status_dropdown(self):
        #Настройка dropdown для статуса
        self.status_dropdown = StatusDropdown()
        self.status_dropdown.bind(on_select=self.on_status_select)

    def open_status_dropdown(self):
        #Открывает dropdown статуса
        if self.status_dropdown and self.status_button:
            self.status_dropdown.open(self.status_button)

    def on_status_select(self, instance, value):

        if value == "В процессе" or value == "В планах":
            self.rating_layout.recetChoice()
        # Обновляем текст кнопки на выбранный статус
        if self.status_button:
            self.status_button.text = value


# Обработка выбора рейтинга
    def on_rating_selected(self, value):
        pass
        
# обработка списка фильмов  
    def setup_scroling_menu(self, dt = None):
        data_from_db = self.db.get_all_films()

        # print(data_from_db)
        if self.scroll_menu:
            self.scroll_menu.update_data(data_from_db)

# обработка фильтров
    def apply_filters(self):
        film_status = self.status_button.text
        film_rating = self.rating_layout.selected_rating
        # print(film_status,"  ", film_rating)
        films_by_filtrs = self.db.find_films_with_filters(film_status, film_rating)
        self.scroll_menu.update_data(films_by_filtrs)
# сброс параметров фильмов
    def recet_filters(self):
        self.status_button.text = "Все"
        self.rating_layout.recetChoice()
        data_from_db = self.db.get_all_films()
        self.scroll_menu.update_data(data_from_db)

# обработка сортиовки рейтинга по возрастанию и убыванию
    def decrease_on_realise(self):
        data_from_db = self.db.get_all_films()
        self.scroll_menu.update_data(data_from_db)

    def increase_on_realise(self):
        data_from_db = self.db.get_all_films()[::-1]
        self.scroll_menu.update_data(data_from_db)