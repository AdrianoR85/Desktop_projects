import tempfile
from PIL import ImageEnhance, Image, ImageFilter
from PyQt5.QtGui import QPixmap
import os


class Editor:
    def __init__(self, label):
        self.label = label
        self.image_path = None
        self.image = None
        self.filename = None

    def load_image(self, image_path):
        self.image = QPixmap(image_path)
        self.image_path = image_path
        self.update_display()

    def update_display(self):
        if self.image:
            self.label.setPixmap(self.image)

    def apply_filter(self, filter_name):
        if not self.image_path:
            return

        # Abrir a imagem com PIL para manipulação
        with Image.open(self.image_path) as img:

            if img.mode != "RGB":
                img = img.convert("RGB")

            if filter_name == "Left":
                img = img.rotate(90, expand=True)
            elif filter_name == "Right":
                img = img.rotate(-90, expand=True)
            elif filter_name == "Mirror":
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif filter_name == "Sharpen":
                img = img.filter(ImageFilter.SHARPEN)
            elif filter_name == "Gray":
                img = img.convert("L").convert("RGBA")
            elif filter_name == "Saturation":
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(1.5)
            elif filter_name == "Contrast":
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.5)
            elif filter_name == "Blur":
                img = img.filter(ImageFilter.BLUR)

            # Obter o diretório temporário e garantir que ele exista
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, "temp_image.png")
            img.save(temp_path)  # Salva a imagem no diretório temporário

            # Atualizar o QPixmap com a imagem filtrada
            self.image = QPixmap(temp_path)
            self.update_display()
