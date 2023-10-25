from PyQt6.QtWidgets import QApplication
from GUI import FinanceTracker
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinanceTracker()
    window.show()
    sys.exit(app.exec())