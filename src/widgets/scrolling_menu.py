from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.properties import BooleanProperty, StringProperty, NumericProperty,ObjectProperty
from database import myDataBase
from kivy.app import App
from widgets.button_with_2_states import CustomButtonWith2States
from utils.helpers import get_resource_path
from kivy.clock import Clock
from kivy.uix.recyclegridlayout import RecycleGridLayout

class CustomRatingImage(Image):
    pass

class StatefulLabel(RecycleDataViewBehavior, BoxLayout):
    name = StringProperty()
    genre = StringProperty()
    status = StringProperty()
    rating = NumericProperty()
    active = BooleanProperty()
    index = 0
    normal_redact_res = StringProperty("")
    down_redact_res = StringProperty("")
    normal_del_res = StringProperty("")
    down_del_res = StringProperty("")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.normal_redact_res = get_resource_path('resources/images/buttons/Redact_btn.png')
        self.down_redact_res = get_resource_path('resources/images/buttons/Redact_btn_down.png')
        self.normal_del_res = get_resource_path('resources/images/buttons/Delete_btn.png')
        self.down_del_res = get_resource_path('resources/images/buttons/Delete_btn_down.png')


    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.name = data.get('name', '')
        self.genre = data.get('genre', '')
        self.status = data.get('status', '')
        self.rating = data.get('rating', 0)
        self.film_id = data.get('film_id', '')
        super(StatefulLabel, self).refresh_view_attrs(rv, index, data)
        self.update_rating_images()

    def del_btn_realise(self, btn):
        db = myDataBase()
        db.del_film(self.film_id)
        if hasattr(self.parent.parent, 'update_data'):
            new_data = db.get_all_films()
            self.parent.parent.update_data(new_data)

    def update_rating_images(self):
        
        Clock.schedule_once(self._update_rating_images)

    def _update_rating_images(self, dt):
        """Обновление изображений рейтинга"""
        if not hasattr(self, 'ids'):
            return
            
        # Обновляем все 5 изображений рейтинга
        for i in range(1, 6):
            image_id = f'rating_btn_{i}'
            if image_id in self.ids:
                if i <= self.rating:
                    # Активная звезда
                    self.ids[image_id].source = get_resource_path('resources/images/buttons/rating_btn_down600.png')
                else:
                    # Неактивная звезда
                    self.ids[image_id].source = get_resource_path('resources/images/buttons/rating_btn_up600.png')

    def go_to_update_film(self):
        app = App.get_running_app()
        app.film_to_redact = self.film_id
        app.root.current = "redactFilmMenuScreen"

class MyRecycleGridLayout(RecycleGridLayout):
        pass
            
class RV(RecycleView):
    grid_layout = ObjectProperty(None)
    def __init__(self, data_list=None, **kwargs):
        super(RV, self).__init__(**kwargs)
        
        if data_list is None:
            # Данные по умолчанию, если список не передан
            data_list = [
                {'name': 'Фильм 1', 'genre': 'Драма', 'status': 'Новый', 'rating': 4, 'film_id': 1, 'active': False}
            ]
        self.data = data_list

    def set_grid_layout_height(self, new_height):
        
        if self.grid_layout:
            self.grid_layout.height = new_height
            return True
        else:
            
            if self.children:
                for child in self.children:
                    if isinstance(child, MyRecycleGridLayout):
                        self.grid_layout = child
                        self.grid_layout.height = new_height
                        return True
        return False
    
    def update_data(self, new_data_list):
        self.data = new_data_list
        k = len(new_data_list)
        new_height = k*75 + (k-1)*10
        # print(new_height)
        # После обновления данных нужно обновить высоту
        if self.grid_layout:
            Clock.schedule_once(lambda dt: self.set_grid_layout_height(new_height), 0.1)
