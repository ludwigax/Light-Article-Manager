from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, \
    QPushButton, QFrame
from PySide6.QtGui import QColor

from widget.search import SearchWidget

import math
import utils.combo as cb

class SemanticSearchZone(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        
        self._metadata = None

        layout = QVBoxLayout()

        self.search_widget = SearchWidget(self)

        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(['Text', 'Score', 'ID'])
        self.table_widget.setFrameShape(QFrame.Panel)
        self.table_widget.setFrameShadow(QFrame.Sunken)
        self.table_widget.setLineWidth(2)

        layout.addWidget(self.search_widget)
        layout.addWidget(self.table_widget)
        self.setLayout(layout)

        self.set_slots()

    def set_slots(self):
        self.search_widget.search_signal.connect(self.search)

    def init_data(self, metadata):
        if self._metadata:
            self.clear_data()
        if not metadata:
            return
        self._metadata = metadata
        scores = self._metadata[0]
        
        for i, text in enumerate(self._metadata[2]):
            self.table_widget.insertRow(i)

            label = QLabel(text)
            label.setWordWrap(True)
            label.setFixedWidth(400)

            self.table_widget.setCellWidget(i, 0, label)
            self.table_widget.setRowHeight(i, label.sizeHint().height())
            self.table_widget.setItem(i, 1, QTableWidgetItem(f"{scores[i]:.3f}"))
            self.table_widget.setItem(i, 2, QTableWidgetItem(str(self._metadata[1][i])))

            color = self.calculate_color(scores[i])
            self.table_widget.item(i, 1).setBackground(color)
        self.table_widget.resizeColumnsToContents()

    def clear_data(self):
        self._metadata = None
        self.table_widget.clear()
        self.table_widget.setRowCount(0)

    def search(self, text):
        if not text:
            return
        scores, article_ids, texts = cb.search_vector_base(text)
        self.init_data((scores, article_ids, texts))

    def calculate_color(self, score):
        if score is None or (isinstance(score, float) and math.isnan(score)):
            return QColor(0, 191, 255)

        if score < 0.5:
            red = 255
            green = int(255 * (score * 2))
        else:
            red = int(255 * (1 - score) * 2)
            green = 255

        blue = 0
        return QColor(red, green, blue)




    