from PyQt5.QtWidgets import QApplication, QWidget
from image_editor import ImageEditor
import os


class Application(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Editor")
        self.resize(900, 700)

        self.image_editor = ImageEditor()
        self.setLayout(self.image_editor.master_layout)

        self.load_styles()

    def load_styles(self):
        current_dir = os.path.dirname(__file__)
        style_path = os.path.join(current_dir, "styles.qss")

        # Tenta carregar o arquivo de estilo
        try:
            with open(style_path, "r") as file:
                style = file.read()
                self.setStyleSheet(style)
        except FileNotFoundError:
            print(f"Arquivo de estilo 'styles.qss' não encontrado em {style_path}")


if __name__ == "__main__":
    app = QApplication([])
    window = Application()
    window.show()
    app.exec_()
