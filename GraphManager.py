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
        if x is not None and y is not None:
            sc.axes.plot(x, y)
        sc.axes.set_xlabel('Time')
        sc.axes.set_ylabel('Balance')
        # hide the tick lines
        sc.axes.get_xaxis().set_ticks([])
        sc.axes.get_yaxis().set_ticks([])
        # hide the values
        sc.axes.get_xaxis().set_ticklabels([])
        sc.axes.get_yaxis().set_ticklabels([])
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(sc)
        self.show()
    