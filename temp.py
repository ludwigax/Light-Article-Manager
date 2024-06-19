from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QToolBar, QTextBrowser, QAction
from PyQt5.QtCore import Qt, QRect

from widget.search import SearchWidget

if __name__ == '__main__':
    app = QApplication([])
    
    window = QMainWindow()
    window.setWindowTitle('Main Window')
    # window.setGeometry(QRect(100, 100, 800, 600))
    search = SearchWidget()
    window.setCentralWidget(search)
    window.show()
    
    app.exec_()
