import shutil
import os
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QFileDialog,
)
from PyQt5.QtCore import Qt
from editor import Editor

button_texts = [
    "Original",
    "Left",
    "Right",
    "Mirror",
    "Sharpen",
    "Gray",
    "Saturation",
    "Contrast",
    "Blur",
]


class ImageEditor:
    def __init__(self):
        self.col_left = QVBoxLayout()
        self.col_right = QVBoxLayout()
        self.file_list = QListWidget()

        self.picture_box = QLabel("Image will appear here!")
        self.picture_box.setObjectName("pictureBox")
        self.picture_box.setAlignment(Qt.AlignCenter)

        self.root_path = os.path.join(
            os.path.expanduser("~"), "Pictures", "ImagesEditor"
        )

        self.editor = Editor(self.picture_box)

        self.init_ui()
        self.list_images()

    def init_ui(self):
        btn_upload = QPushButton("Upload")
        btn_upload.setObjectName("upload")
        btn_upload.clicked.connect(self.save_files)

        self.col_left.addWidget(btn_upload)
        self.col_left.addWidget(self.file_list)

        for text in button_texts:

            button = QPushButton(text)
            button.setObjectName("button")
            button.clicked.connect(lambda _, t=text: self.editor_load_image(t))
            self.col_left.addWidget(button)

        self.col_right.addWidget(self.picture_box)

        self.master_layout = QHBoxLayout()
        self.master_layout.addLayout(self.col_left, 20)
        self.master_layout.addLayout(self.col_right, 80)

        self.file_list.currentRowChanged.connect(self.display_image)

    def save_files(self):
        origin_path, _ = QFileDialog.getOpenFileName(
            None, "Select Image", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp)"
        )

        if origin_path:
            os.makedirs(self.root_path, exist_ok=True)

            filename = os.path.basename(origin_path)
            destination_path = os.path.join(self.root_path, filename)

            if not os.path.exists(destination_path):
                shutil.copy(origin_path, destination_path)
                self.file_list.addItem(filename)
            else:
                print("File already exists!")

    def list_images(self):
        if os.path.exists(self.root_path):
            for file in os.listdir(self.root_path):
                if file.endswith((".png", ".xpm", ".jpg", ".jpeg", ".bmp")):
                    self.file_list.addItem(file)

    def display_image(self):
        if self.file_list.currentRow() >= 0:
            filename = self.file_list.currentItem().text()
            image_path = os.path.join(self.root_path, filename)

            self.editor.load_image(image_path)

    def editor_load_image(self, text: str):
        self.editor.apply_filter(text)
