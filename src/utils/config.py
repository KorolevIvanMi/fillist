
from kivy.config import Config
from kivy.core.window import Window
from kivy.app import App

def screen_confirguration():
    Config.set('graphics', 'fullscreen', '0')  
    Config.set('graphics', 'resizable', '1')
    Config.set('graphics', 'width', '1920')
    Config.set('graphics', 'height', '1080')

def bind_keyboard_to_app(app_class):
    original_build = app_class.build
    

    def new_build(self):
        # Вызываем оригинальный build
        root = original_build(self)
        # Привязываем обработчик клавиатуры
        Window.bind(on_keyboard=self._handle_keyboard)
        return root
    
    def _handle_keyboard(self, window, key, scancode, codepoint, modifier):
        """Обработчик клавиатуры"""
        print(f"Key: {key}, Modifiers: {modifier}")
        
        # F11 для переключения полноэкранного режима
        if key == 292: 
            if Window.fullscreen:
                # Переход в оконный режим
                Window.fullscreen = False
                Window.size = (1200, 750)
            else:
                # Переход в полноэкранный режим
                Window.fullscreen = 'auto'
            return True
        
        if key == 110 and 'ctrl' in modifier:
            app = App.get_running_app()
            if app and hasattr(app, 'root'):
                current_screen = app.root.current_screen
                if current_screen and current_screen.name == "mainScreen":
                    if hasattr(current_screen, 'ids') and 'fillist_main_menu' in current_screen.ids:
                        fillist_menu = current_screen.ids.fillist_main_menu
                        
                        # Проверяем, что у него есть нужный метод
                        if hasattr(fillist_menu, 'go_to_addScreen'):
                            fillist_menu.go_to_addScreen()
                            return True
        
    
        if key == 115 and  'ctrl' in modifier:
            app = App.get_running_app()
            if app and hasattr(app, 'root'):
                current_screen = app.root.current_screen
                if current_screen and current_screen.name == "AddFilmMenuScreen":
                    # Теперь получаем FillistMainMenu через его id
                    if hasattr(current_screen, 'ids') and 'add_film_menu' in current_screen.ids:
                        fillist_menu = current_screen.ids.add_film_menu
                        
                        # Проверяем, что у него есть нужный метод
                        if hasattr(fillist_menu, 'acceptOnRelease'):
                            fillist_menu.acceptOnRelease()
                            return True
                elif current_screen and current_screen.name == "redactFilmMenuScreen":
                    
                    if hasattr(current_screen, 'ids') and 'redact_film_menu' in current_screen.ids:
                        fillist_menu = current_screen.ids.redact_film_menu
                        
                        # Проверяем, что у него есть нужный метод
                        if hasattr(fillist_menu, 'save_changes'):
                            fillist_menu.save_changes()
                            return True
        if key == 98 and  'ctrl' in modifier:
            app = App.get_running_app()
            if app and hasattr(app, 'root'):
                current_screen = app.root.current_screen
                if current_screen and current_screen.name == "AddFilmMenuScreen":
                    # Теперь получаем FillistMainMenu через его id
                    if hasattr(current_screen, 'ids') and 'add_film_menu' in current_screen.ids:
                        fillist_menu = current_screen.ids.add_film_menu
                        
                        # Проверяем, что у него есть нужный метод
                        if hasattr(fillist_menu, 'getBackOnRelease'):
                            fillist_menu.getBackOnRelease()
                            return True
                elif current_screen and current_screen.name == "redactFilmMenuScreen":
                    
                    if hasattr(current_screen, 'ids') and 'redact_film_menu' in current_screen.ids:
                        fillist_menu = current_screen.ids.redact_film_menu
                        
                        # Проверяем, что у него есть нужный метод
                        if hasattr(fillist_menu, 'getBackOnRelease'):
                            fillist_menu.getBackOnRelease()
                            return True
                elif current_screen and current_screen.name == "mainScreen":
                    
                    if hasattr(current_screen, 'ids') and 'fillist_main_menu' in current_screen.ids:
                        fillist_menu = current_screen.ids.fillist_main_menu
                        
                        # Проверяем, что у него есть нужный метод
                        if hasattr(fillist_menu, 'go_to_home'):
                            fillist_menu.go_to_home()
                            return True
                elif current_screen and current_screen.name == "settingsScreen":
                    if hasattr(current_screen, 'ids') and 'setting_menu' in current_screen.ids:
                        fillist_menu = current_screen.ids.setting_menu
                        # Проверяем, что у него есть нужный метод
                        if hasattr(fillist_menu, 'go_to_home'):
                            fillist_menu.go_to_home()
                            return True
                elif current_screen and current_screen.name == "exportImportScreen":
                    if hasattr(current_screen, 'ids') and 'export_import_menu' in current_screen.ids:
                        fillist_menu = current_screen.ids.export_import_menu
                        # Проверяем, что у него есть нужный метод
                        if hasattr(fillist_menu, 'go_to_home'):
                            fillist_menu.go_to_home()
                            return True
                elif current_screen and current_screen.name == "ProfileScreen":
                    if hasattr(current_screen, 'ids') and 'profile_menu' in current_screen.ids:
                        fillist_menu = current_screen.ids.profile_menu
                        # Проверяем, что у него есть нужный метод
                        if hasattr(fillist_menu, 'go_to_home'):
                            fillist_menu.go_to_home()
                            return True
        return False
    # Заменяем методы
    app_class.build = new_build
    app_class._handle_keyboard = _handle_keyboard
    
    return app_class


    
