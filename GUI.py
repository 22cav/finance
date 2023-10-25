import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QWidget, QGridLayout, QStyle, QComboBox, QListWidget
from PyQt6.QtCore import Qt, pyqtSignal
from FinanceManager import FinanceManager
import matplotlib.pyplot as plt


class FinanceTracker(QMainWindow):

    def __init__(self):
        super().__init__()
        # Set window title and dimensions
        self.setWindowTitle("Finance Tracker")
        self.load_window = None
        self.setup_intro_ui()

    def setup_intro_ui(self):
        self.setGeometry(100, 100, 400, 300)
        self.frame = QWidget(self)
        self.setCentralWidget(self.frame)

        # Create labels and buttons
        self.label1 = QLabel("Welcome to Finance Tracker", self.frame)
        self.label1.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.label2 = QLabel("Please load a saved file or enter your available finances:", self.frame)
        self.label2.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
        self.finances_available = QLineEdit(self.frame)
        self.finances_available.setStyleSheet("padding: 10px; font-size: 16px; border-radius: 5px; border: 1px solid #ccc;")
        self.submit_button = QPushButton("Submit", self.frame)
        self.submit_button.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #4CAF50; color: #fff; font-size: 16px;")
        self.submit_button.clicked.connect(self.submit_money)
        self.label3 = QLabel("Or", self.frame)
        self.load_button = QPushButton("Load Saving", self.frame)
        self.load_button.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #2196F3; color: #fff; font-size: 16px;")
        self.load_button.clicked.connect(self.show_load_window)

        # Create a grid layout and add the widgets to it
        grid = QGridLayout()
        grid.setSpacing(20)
        grid.addWidget(self.label1, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.label2, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.finances_available, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.submit_button, 3, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.label3, 4, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.load_button, 5, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        # Set the layout for the main widget
        self.frame.setLayout(grid)

    def show_load_window(self):
        self.load_window = Load_Window()
        self.load_window.submitClicked.connect(self.on_load_window_confirm)
        self.load_window.show()
    
    def on_load_window_confirm(self, file):
        if file == 'None':
            self.load_window = None
        else:
            self.setup_main_ui(file)
            self.load_window = None

    def submit_money(self):
        finances = self.finances_available.text()
        self.manager = FinanceManager(finances)
        self.setup_menu_ui()

    def setup_menu_ui(self, selected_file=None):
        self.setGeometry(100, 100, 800, 600)
        self.frame = QWidget(self)
        self.setCentralWidget(self.frame)

        # Central Panel: Current balance, last 5 transactions log + "see more"
        self.frame1 = QWidget(self.frame)
        self.current_balance_label = QLabel("Current Balance: ", self.frame1)
        self.current_balance_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.current_balance_value = QLabel("€"+self.manager.balance(), self.frame1)
        self.current_balance_value.setStyleSheet("font-size: 24px; margin-bottom: 20px;")
        self.transactions_label = QLabel("Last 5 Transactions:", self.frame1)
        self.transactions_label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
        self.transactions_list = QListWidget(self.frame1)
        self.transactions_list.setStyleSheet("padding: 10px; font-size: 16px; border-radius: 5px; border: 1px solid #ccc;")
        self.see_more_button = QPushButton("See More", self.frame1)
        self.see_more_button.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #2196F3; color: #fff; font-size: 16px;")
        self.see_more_button.clicked.connect(self.show_transactions_window)

        # Set the layout for the first subframe
        grid1 = QGridLayout()
        grid1.setSpacing(20)
        grid1.addWidget(self.current_balance_label, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid1.addWidget(self.current_balance_value, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid1.addWidget(self.transactions_label, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid1.addWidget(self.transactions_list, 3, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid1.addWidget(self.see_more_button, 4, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        self.frame1.setLayout(grid1)

        # Right panel: Budget division
        self.frame2 = QWidget(self.frame)
        self.budget_label = QLabel("Budget Division:", self.frame2)
        self.budget_label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
        self.budget_list = QListWidget(self.frame2)
        self.budget_list.setStyleSheet("padding: 10px; font-size: 16px; border-radius: 5px; border: 1px solid #ccc;")
        self.add_budget_button = QPushButton("Add Budget", self.frame2)
        self.add_budget_button.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #4CAF50; color: #fff; font-size: 16px;")
        self.add_budget_button.clicked.connect(self.show_add_budget_window)

        # Set the layout for the second subframe
        grid2 = QGridLayout()
        grid2.setSpacing(20)
        grid2.addWidget(self.budget_label, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid2.addWidget(self.budget_list, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid2.addWidget(self.add_budget_button, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        self.frame2.setLayout(grid2)

        # Left panel: Add transaction
        self.frame3 = QWidget(self.frame)
        self.add_transaction_label = QLabel("Add Transaction:", self.frame3)
        self.add_transaction_label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")

        # Set the layout for the third subframe
        grid3 = QGridLayout()
        grid3.setSpacing(20)
        grid3.addWidget(self.add_transaction_label, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        self.frame3.setLayout(grid3)

        # Create a grid layout and add the widgets to it
        grid = QGridLayout()
        grid.setSpacing(20)
        grid.addWidget(self.frame3, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.frame1, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.frame2, 0, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Set the layout for the main widget
        self.frame.setLayout(grid)

    def show_transactions_window(self):
        pass
        """self.transactions_window = Transactions_Window()
        self.transactions_window.show()"""

    def show_add_budget_window(self):
        pass
        """self.add_budget_window = Add_Budget_Window()
        self.add_budget_window.submitClicked.connect(self.on_add_budget_window_confirm)
        self.add_budget_window.show()"""

    def on_add_budget_window_confirm(self, budget):
        self.budget_list.addItem(budget)
        self.add_budget_window = None

    def submit_transaction(self):
        name = self.transaction_name_input.text()
        amount = self.transaction_amount_input.text()
        transaction_type = self.transaction_type_dropdown.currentText()
        self.manager.add_transaction(name, amount, transaction_type)
        self.current_balance_value.setText(f"${self.manager.current_balance:.2f}")
        self.transactions_list.clear()
        for transaction in self.manager.transactions[-5:]:
            self.transactions_list.addItem(f"{transaction['name']}: ${transaction['amount']:.2f} ({transaction['type']})")

class Load_Window(QMainWindow):
    submitClicked = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Load a Saved File")
        self.folder_path = "./Saved Balances"
        self.saved_files = [f for f in os.listdir(self.folder_path) if f.endswith('.txt')]
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(100, 100, 400, 300)
        self.frame = QWidget(self)
        self.setCentralWidget(self.frame)

        # Create labels and dropdown menu
        self.label1 = QLabel("Select a saved file:", self.frame)
        self.label1.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
        self.file_dropdown = QComboBox(self.frame)
        self.file_dropdown.setStyleSheet("padding: 10px; font-size: 16px; border-radius: 5px; border: 1px solid #ccc;")
        self.file_dropdown.addItems(['None'] + self.saved_files)
        self.submit_button = QPushButton("Submit", self.frame)
        self.submit_button.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #4CAF50; color: #fff; font-size: 16px;")
        self.submit_button.clicked.connect(self.submit)
        
        # Create a grid layout and add the widgets to it
        grid = QGridLayout()
        grid.setSpacing(20)
        grid.addWidget(self.label1, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.file_dropdown, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.submit_button, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        # Set the layout for the main widget
        self.frame.setLayout(grid)

    def submit(self):
        self.submitClicked.emit(self.file_dropdown.currentText())
        self.close