from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QPushButton, QMessageBox

class CalcApp(QWidget):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Calculator App")
    self.resize(250,300)

    # Main Widgets
    self.text_box = QLineEdit()
    self.grid = QGridLayout()

    # Button labels and control buttons 
    self.buttons_text = [
      "7", "8", "9", "/",
      "4", "5", "6", "*",
      "1", "2", "3", "-",
      "0", ".", "=", "+"
    ]
    self.btn_clear = QPushButton("Clear")
    self.btn_delete = QPushButton("<")

    # UI setup
    self.init_ui()
    self.apply_styles()


  def init_ui(self):
    """Initialize and organize the Calculator's layouts and widgets."""
    main_layout = QVBoxLayout()

    # Input line for text
    main_layout.addWidget(self.text_box)

    # Layout for numeric and operational buttons
    self.create_buttons()
    main_layout.addLayout(self.grid)

    # Layout for control buttons
    control_buttons = QHBoxLayout()
    control_buttons.addWidget(self.btn_clear) 
    control_buttons.addWidget(self.btn_delete) 
    main_layout.addLayout(control_buttons)

    # Connect control buttons to their respective functions
    self.btn_clear.clicked.connect(self.clear_text)
    self.btn_delete.clicked.connect(self.delete_last_character)
    
    # Set the main layout
    self.setLayout(main_layout)

  def create_buttons(self):
    """Creates the calculator buttons and adds them to the grid layout."""
    row, col = 0, 0
    for text in self.buttons_text:
      button = QPushButton(text)
      
      # Assign classes based ont button type
      if text in "0123456789.":
        button.setObjectName("number")
      elif text in "/*-+=":
        button.setObjectName("operator")

      # Connect the button click event 
      button.clicked.connect(lambda _, t=text: self.on_button_click(t))
      self.grid.addWidget(button, row, col)

      col += 1
      if col > 3:
        row += 1
        col = 0

    # Assign object names to control buttons for unique styling
    self.btn_clear.setObjectName("special")
    self.btn_delete.setObjectName("special")

  def apply_styles(self):
    """Applies CSS styles to the calculator."""
    self.setStyleSheet("""
      QWidget {
        background-color: #f5f5f5;
        font-family: Arial, sans-serif;                                
      }
                       
      QLineEdit {
        font-size: 24px;
        padding: 10px;
        border: 2px solid #d3d3d3;
        border-radius: 10px;
        background-color: #ffffff;
        color: #333333;
        margin-bottom: 10px;
      }
                       
      QPushButton {
        font-size: 18px;
        padding: 10px;
        border-radius: 10px;
      }
                       
      QPushButton#number {
        background-color: #e0e0e0;
        color: #333333;
      }
                       
      QPushButton#number:hover { background-color: #d3d3d3; }
                       
      QPushButton#operator {
        background-color: #81d4d3;
        color: #ffffff;                 
      }
                       
      QPushButton#operator:hover { background-color: #4fc3f7; }
                                                    
      QPushButton:pressed {
        background-color: #c8c8c8;
      }
                       
      QPushButton#special {
        background-color: #fbbc04;
        color: #ffffff;
      }
      QPushButton#special:hover { background-color: #fbbc04; }
                
    """)

  def on_button_click(self, text:str):
    """Handles logic for operation and number buttons."""
    if text == "=":
      self.calculate_results()
    else:
      self.text_box.setText(self.text_box.text() + text)

    
  def calculate_results(self):
    """Performs calculation based on the current expression."""
    expression = self.text_box.text()
    try:
      result = eval(expression)
      self.text_box.setText(str(result))
    except ZeroDivisionError:
      self.show_error("Error: Division by zero")
    except SyntaxError:
      self.show_error("Error: Invalid syntax")
    except Exception:
      self.show_error("Error: An error occurred")
  
  def clear_text(self):
    self.text_box.clear()
  
  def delete_last_character(self):
    text = self.text_box.text()
    if text:
      self.text_box.setText(text[:-1])
  
  def show_error(self, message):
    """Display an error message in a dialog box."""
    error_dialog = QMessageBox()
    error_dialog.setIcon(QMessageBox.Critical)
    error_dialog.setWindowTitle("Error!")
    error_dialog.setText(message)
    error_dialog.exec_()
   

if __name__ == "__main__":
  app = QApplication([])
  window = CalcApp()
  window.show()
  app.exec_()