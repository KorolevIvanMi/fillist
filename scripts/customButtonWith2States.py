
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.properties import StringProperty

class CustomButtonWith2States(ButtonBehavior, Image):
    normal_source = StringProperty("")
    down_source = StringProperty("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_active = False
        

    def on_normal_source(self, instance, value):
        if self.state == 'normal':
            self.source = value

    def on_down_source(self, instance, value):
        if self.state == 'down':
            self.source = value

    def on_state(self, instance, value):
        if value == 'down' and self.down_source:
            self.source = self.down_source
        else:
            self.source = self.normal_source