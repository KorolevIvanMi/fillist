from kivy.uix.settings import text_type
from myDropDownAddAndRedact import StatusDropdownAdd, CustomDropdownButtonAdd
from kivy.uix.widget import Widget
from  kivy.properties import ObjectProperty
from kivy.app import App
from myDataBase import myDataBase
from utils import *

class RedactFilmMenu(Widget):

    
    db = myDataBase()
    film_name_txt = ObjectProperty(None)
    film_genre_txt = ObjectProperty(None)
    status_button = ObjectProperty(None)
    rating_layout = ObjectProperty(None)
    film_description_txt = ObjectProperty(None)
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.normal_apl_res = get_resource_path('images/buttons/Apply_btn.png')
        self.down_apl_res = get_resource_path('images/buttons/Apply_btn_down.png')
        self.normal_get_back_res = get_resource_path('images/buttons/Get_back_btn.png')
        self.down_get_back_res = get_resource_path('images/buttons/Get_back_btn_down.png')
        self.setup_status_dropdown()

    def on_enter(self):
        self.setup_all_data()

    def getBackOnRelease(self):
        app = App.get_running_app()
        app.root.current = "mainScreen"
    
    def setup_all_data(self):

        app = App.get_running_app()
        
        s = self.db.find_film_by_id(app.film_to_redact)
        self.film_name_txt.text = s["name"]  
        self.film_genre_txt.text = s['genre']
        self.status_button.text = s['status']
        self.film_description_txt.text = s['description']
        self.rating_layout.set_rating(str(s["rating"]))

    def on_rating_selected(self, value):
        pass

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

    def save_changes(self):
        app = App.get_running_app()
        
        film_id = app.film_to_redact
        film_name = self.film_name_txt.text
        film_genre = self.film_genre_txt.text
        film_status = self.status_button.text
        film_rating = self.rating_layout.selected_rating
        film_discription = self.film_description_txt.text

        isfilmin = self.db.update_data(film_id, film_name, film_genre, film_status, film_rating, film_discription )
        if (isfilmin == 1):
            

            app.data_updated = True
            app.root.current = "mainScreen"
