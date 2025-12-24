from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty

from utils.helpers import get_resource_path


class ExportImportMenu(FloatLayout):

    container_dyn = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.normal_home_res = get_resource_path('resources/images/buttons/Home_btn.png')
        self.down_home_res = get_resource_path('resources/images/buttons/Home_btn_down.png')
        
    def go_to_home(self):
        app = App.get_running_app()
        app.root.current = "welcomeScreen"

    def spawn_export_widgets(self):
        self.container_dyn.clear_widgets()

        box = BoxLayout( 
        pos_hint= {'x': 1.665/10, 'y': 6/10},
        size_hint=(6.67/10, 3/10),
        orientation= 'vertical',
        ) 
        
        label = Label(
            text='Путь куда экспортировать данные:',
            color=(0, 0, 0, 1),
            font_size='40sp'
        )

        box.add_widget(label)
        
        self.container_dyn.add_widget(box)
        
