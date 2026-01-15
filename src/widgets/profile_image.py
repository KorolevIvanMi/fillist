from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from io import BytesIO
from utils.helpers import get_resource_path


class ProfileImage(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_image = get_resource_path("resources/images/buttons/Profile_btn.png")
        self.source = self.default_image  # Устанавливаем дефолтное изображение
        
    def update_image(self, resource):
        """
        Обновляет изображение из BLOB данных
        """
        if isinstance(resource, bytes) and resource:
            try:
                # Конвертируем BLOB в текстуру
                data = BytesIO(resource)
                img = CoreImage(data, ext='png')
                self.texture = img.texture
                return True
            except:
                # При ошибке - дефолтное изображение
                self.source = self.default_image
                return False
        else:
            # Если не BLOB - дефолтное изображение
            self.source = self.default_image
            return False