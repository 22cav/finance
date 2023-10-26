import sys
import os
import datetime
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QWidget, QGridLayout, QStyle, QComboBox, QListWidget
from PyQt6.QtCore import Qt, pyqtSignal
from FinanceManager import FinanceManager
from GraphManager import Graph_Widget


class FinanceTracker(QMainWindow):

    def __init__(self):
        super().__init__()
        # Set window title and dimensions
        self.setWindowTitle("Finance Tracker")
        self.load_window = None
        self.manager = None  # Define the manager attribute as None initially
        self.setup_intro_ui()
        self.loaded_file = None
        self.budget_division_list = []
    
    def save_transaction(self, transactions):
        with open(f"Saved Balances/{self.loaded_file}.txt", "w") as f:
            # In the first line of the file, write the amount of money available
            f.write(f"amount{self.manager.get_balance()}\n")
            # In the second line, write the transaction history
            f.write("transactions:")
            for transaction in transactions:
                f.write(f"{transaction},")
            f.write("\n")
            # In the third line, write the budget division
            f.write("budgets:" + ",".join(self.budget_division_list) + "\n")
                 
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
        self.file_name = QLineEdit(self.frame)
        self.file_name.setStyleSheet("padding: 10px; font-size: 16px; border-radius: 5px; border: 1px solid #ccc;")
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
        grid.addWidget(self.file_name, 3, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.submit_button, 4, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.label3, 5, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.load_button, 6, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        # Set the layout for the main widget
        self.frame.setLayout(grid)

    def show_load_window(self):
        self.load_window = Load_Window()
        self.load_window.submitClicked.connect(self.on_load_window_confirm)
        self.load_window.show()
    
    def on_load_window_confirm(self, file):
        if file == 'None':
            self.load_window.close()
            self.load_window = None
        else:
            self.load_window.close()
            self.manager = FinanceManager(filepath=file)
            self.manager.Load_file()
            self.load_window = None
            self.loaded_file = file
            self.setup_menu_ui()

    def submit_money(self):
        finances = self.finances_available.text()
        self.manager = FinanceManager(finances)
        self.manager.Initialize_empty_file(name, finances)
        name = self.file_name.text()
        self.manager.Initialize_empty_file(name, finances)
        self.setup_menu_ui(name+".txt")

    def setup_menu_ui(self):
        self.setGeometry(100, 100, 800, 600)
        self.frame = QWidget(self)
        self.setCentralWidget(self.frame)
        # Central Panel: Current balance, last 5 transactions log + "see more"
        self.frame1 = QWidget(self.frame)
        self.current_balance_label = QLabel("Current Balance: ", self.frame1)
        self.current_balance_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.current_balance_value = QLabel("€"+str(self.manager.get_balance()), self.frame1)
        self.current_balance_value.setStyleSheet("font-size: 24px; margin-bottom: 20px;")
        self.transactions_label = QLabel("Last 5 Transactions:", self.frame1)
        self.transactions_label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
        self.transactions_list = QListWidget(self.frame1, )
        self.transactions_list.setFixedHeight(120)
        self.transactions_list.setStyleSheet("padding: 10px; font-size: 16px; border-radius: 5px; border: 1px solid #ccc;")
        #Show the last 5 transactions with mooney spent
        for transaction in self.manager.return_n_transactions(5).iterrows():
            self.transactions_list.addItem(transaction[1]['description'] + ": " + str(transaction[1]['amount']) + "€")
        self.see_more_button = QPushButton("See all the transactions", self.frame1)
        self.see_more_button.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #2196F3; color: #fff; font-size: 16px;")
        self.see_more_button.clicked.connect(self.show_transactions_window)
        self.add_transaction_label = QPushButton("Add Transaction", self.frame1)
        self.add_transaction_label.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #2196F3; color: #fff; font-size: 16px;")
        self.add_transaction_label.clicked.connect(self.setup_add_transaction_ui)


        # Set the layout for the first subframe
        grid1 = QGridLayout()
        grid1.setSpacing(20)
        grid1.addWidget(self.current_balance_label, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid1.addWidget(self.current_balance_value, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid1.addWidget(self.transactions_label, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid1.addWidget(self.transactions_list, 3, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid1.addWidget(self.see_more_button, 4, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid1.addWidget(self.add_transaction_label, 5, 0, alignment=Qt.AlignmentFlag.AlignCenter)
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
        self.data_visualization_label = QLabel("Balance graph:", self.frame2)
        self.data_visualization_graph = Graph_Widget(self.manager.return_n_transactions(10)['date'].tolist(), self.manager.return_n_balances(10), self.frame2)

        # Set the layout for the second subframe
        grid2 = QGridLayout()
        grid2.setSpacing(20)
        grid2.addWidget(self.budget_label, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid2.addWidget(self.budget_list, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid2.addWidget(self.add_budget_button, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid2.addWidget(self.data_visualization_label, 5, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid2.addWidget(self.data_visualization_graph, 6, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        self.frame2.setLayout(grid2)


        # Create a grid layout and add the widgets to it
        grid = QGridLayout()
        grid.setSpacing(20)
        grid.addWidget(self.frame1, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.frame2, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Set the layout for the main widget
        self.frame.setLayout(grid)

    def setup_add_transaction_ui(self):
        self.frame = QWidget(self)
        self.setCentralWidget(self.frame)
        self.setGeometry(100, 100, 800, 600)

        self.label1 = QLabel("Add Transaction", self.frame)
        self.label1.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.label2 = QLabel("Amount:", self.frame)
        self.label2.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
        self.amount = QLineEdit(self.frame)
        self.amount.setStyleSheet("padding: 10px; font-size: 16px; border-radius: 5px; border: 1px solid #ccc;")
        self.label3 = QLabel("Description:", self.frame)
        self.label3.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
        self.description = QLineEdit(self.frame)
        self.description.setStyleSheet("padding: 10px; font-size: 16px; border-radius: 5px; border: 1px solid #ccc;")
        self.submit_button = QPushButton("Submit", self.frame)
        self.submit_button.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #4CAF50; color: #fff; font-size: 16px;")
        self.submit_button.clicked.connect(self.submit_transaction)

        # Create a grid layout and add the widgets to it
        grid = QGridLayout()
        grid.setSpacing(20)
        grid.addWidget(self.label1, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.label2, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.amount, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.label3, 3, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.description, 4, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.submit_button, 5, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        # Set the layout for the main widget   
        self.frame.setLayout(grid)

    def submit_transaction(self):
        amount = self.amount.text()
        description = self.description.text()
        self.manager.add_transaction(amount, datetime.datetime.now(), description)
        self.setup_menu_ui(self.loaded_file)

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