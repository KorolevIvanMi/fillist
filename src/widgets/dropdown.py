from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.properties import ListProperty

class CustomDropdownButton(Button):
    button_color = ListProperty([136/255,136/255,136/255, 1]) 

class StatusDropdown(DropDown):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auto_width =200
        statuses = ["Просмотрен", "В планах", "В процессе"]
        for status in statuses:
            btn = CustomDropdownButton(text = status)
            btn.bind(on_release = lambda btn: self.select(btn.text))
            self.add_widget(btn)

