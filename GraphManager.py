import sys
import matplotlib
matplotlib.use('QtAgg')

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(5, 4), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class Graph_Widget(QWidget):
    def __init__(self, x, y, parent=None, *args, **kwargs):
        super(Graph_Widget, self).__init__(*args, **kwargs)

        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot([1,2,3,4,5], y)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(sc)
        self.show()