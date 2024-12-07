import os
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QDateEdit,
    QLineEdit,
    QComboBox,
    QPushButton,
    QTableWidget,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QTableWidgetItem,
    QHeaderView,
)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import QDate, Qt


class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(550, 500)
        self.setWindowTitle("Expense Tracker 2.0")

        self.date_box = QDateEdit()
        self.dropdown = QComboBox()
        self.description = QLineEdit()
        self.amount = QLineEdit()

        self.add_btn = QPushButton("Add Expense")
        self.add_btn.clicked.connect(self.add_expense)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.delete_expense)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Id", "Date", "Category", "Amount", "Description"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.sortByColumn(1, Qt.DescendingOrder)

        self.dropdown.addItems(
            ["Food", "Transport", "Rent", "Shopping", "Entertainment", "Bills", "Other"]
        )

        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()

        self.row1.setContentsMargins(5, 5, 5, 5)
        self.row2.setContentsMargins(5, 5, 5, 5)
        self.row3.setContentsMargins(5, 5, 5, 5)

        self.row1.addWidget(QLabel("Date:"))
        self.row1.addWidget(self.date_box)
        self.row1.addWidget(QLabel("Category:"))
        self.row1.addWidget(self.dropdown)

        self.row2.addWidget(QLabel("Amount:"))
        self.row2.addWidget(self.amount)
        self.row2.addWidget(QLabel("Description:"))
        self.row2.addWidget(self.description)

        self.row3.addWidget(self.add_btn)
        self.row3.addWidget(self.delete_btn)

        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)
        self.master_layout.addLayout(self.row3)

        self.master_layout.addWidget(self.table)

        self.setLayout(self.master_layout)

        self.load_table()
        self.load_styles()

    def load_table(self):
        self.table.setRowCount(0)

        query = QSqlQuery("SELECT * FROM expenses")

        row = 0
        while query.next():
            expensive_id = query.value(0)
            date = query.value(1)
            category = query.value(2)
            amount = query.value(3)
            description = query.value(4)

            # Add Values to Table
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(expensive_id)))
            self.table.setItem(row, 1, QTableWidgetItem(date))
            self.table.setItem(row, 2, QTableWidgetItem(category))
            self.table.setItem(row, 3, QTableWidgetItem(str(amount)))
            self.table.setItem(row, 4, QTableWidgetItem(description))

            row += 1

    def add_expense(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        category = self.dropdown.currentText()
        amount = self.amount.text()
        description = self.description.text()

        query = QSqlQuery()
        query.prepare(
            "INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)"
        )
        query.addBindValue(date)
        query.addBindValue(category)
        query.addBindValue(amount)
        query.addBindValue(description)
        query.exec_()

        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()

        self.load_table()

    def delete_expense(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Warning", "Please select an expense to delete!.")
            return

        expensive_id = self.table.item(selected_row, 0).text()

        confirm_delete = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this expense?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm_delete == QMessageBox.Yes:
            query = QSqlQuery()
            query.prepare("DELETE FROM expenses WHERE id = ?")
            query.addBindValue(expensive_id)
            query.exec_()

            self.load_table()

    def load_styles(self):
        current_dir = os.path.dirname(__file__)
        style_path = os.path.join(current_dir, "styles.qss")
        try:
            with open(style_path, "r") as file:
                style = file.read()
                self.setStyleSheet(style)
        except FileNotFoundError:
            print(f"Arquivo de estilo 'styles.qss' não encontrado em {style_path}")

# Create Database
database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName("expenses.db")

if not database.open():
    QMessageBox.critical(
        None,
        "Database Error",
        "Could not open your database.",
        QMessageBox.Cancel,
    )
    sys.exit(1)

query = QSqlQuery()
query.exec_(
    """
      CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        date TEXT, 
        category TEXT, 
        amount REAL,
        description TEXT)
    """
)


if __name__ == "__main__":
    app = QApplication([])
    window = ExpenseApp()
    window.show()
    app.exec_()
