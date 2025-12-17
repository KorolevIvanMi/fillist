from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.properties import StringProperty
from utils.helpers import get_resource_path

class CustomButtonForRating(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.normal_source = get_resource_path('resources/images/buttons/rating_btn_up600.png')
        self.active_source = get_resource_path('resources/images/buttons/rating_btn_down600.png')
        self.pressed_source = get_resource_path('resources/images/buttons/rating_btn_cur600.png')

        self.source = self.normal_source
        self.is_active = False
        self.rating_value = ""  

    def on_state(self, instance, value):

        if value == 'down':
            # Кнопка нажата, но еще не отпущена
            self.source = self.pressed_source
        else:
            
            if self.is_active:
                self.source = self.active_source
            else:
                self.source = self.normal_source

class CustomLayotForRating(BoxLayout):
    selected_rating = StringProperty('')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.buttons = []
        self.orientation = 'horizontal'
        self.spacing = 5
        
        for i in range(5):
            btn = CustomButtonForRating()
            btn.rating_value = str(i+1)  # Сохраняем значение рейтинга
            btn.bind(on_release=self.buttonIsDown)
            self.buttons.append(btn)
            self.add_widget(btn)

    def buttonIsDown(self, btn_instance):    
        rating = int(btn_instance.rating_value)
        if str(rating) == self.selected_rating:
            self.recetChoice()
        else:
            self.selected_rating = str(rating)
            for i, button in enumerate(self.buttons):
                if i < rating:
                    button.source = button.active_source
                    button.is_active = True
                else:
                    button.source = button.normal_source
                    button.is_active = False

    def recetChoice(self):
        self.selected_rating = ''
        for button in self.buttons:
            button.source = button.normal_source
            button.is_active = False

    def set_rating(self, rating_value):
        
        """Установить рейтинг программно (без нажатия кнопки)"""
        if self.selected_rating == rating_value:
            self.recetChoice()
        else:
            if rating_value:
                rating = int(rating_value)
                self.selected_rating = str(rating)
                for i, button in enumerate(self.buttons):
                    if i < rating:
                        button.source = button.active_source
                        button.is_active = True
                    else:
                        button.source = button.normal_source
                        button.is_active = False
            else:
                self.resetChoice()