from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ListProperty, StringProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.graphics import Color

class WarningForAdd(BoxLayout):
    
    bg_color = ListProperty([1, 0, 0, 0])
    ft_color = ListProperty([1, 1, 1, 1])
    label_text = StringProperty("Вы заполнили не все поля!")


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        
        self.pos_hint = {'y': -0.05} 
        self.label_text = "Test"
        

    def appearing(self, callback = None):
        anim_ap = Animation(pos_hint = {'y':0.15}, duration= 1)
        anim_ap &= Animation(ft_color=[1, 1, 1, 1], duration=1)
        anim_ap &= Animation(bg_color=[1, 0, 0, 1], duration=1)
        anim_dis = Animation(bg_color=[1, 0, 0, 0], duration=1)
        anim_dis &= Animation(ft_color=[1, 1, 1, 0], duration=1)
        
        dis_ap = anim_ap + anim_dis

        if callback:
            dis_ap.bind(on_complete=callback)
        
        dis_ap.start(self)

        return dis_ap