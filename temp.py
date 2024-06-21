import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QDockWidget, QVBoxLayout, QWidget, QSplitter
from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtCore import Qt

from mvc.notem import NoteModule
from archi import ProfileNote

class CodeEditorExample(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Code Editor Example")
        self.setGeometry(100, 100, 800, 600)

        # 中央窗口区域
        # central_widget = QWidget()
        # self.setCentralWidget(central_widget)

        # # 使用 QSplitter 创建可调整大小的面板
        # splitter = QSplitter()

        # # 左侧面板
        # left_panel = QTextEdit()
        # left_panel.setPlaceholderText("Explorer")
        # splitter.addWidget(left_panel)

        # # 中间面板
        # center_panel = QTextEdit()
        # center_panel.setPlaceholderText("Editor")
        # splitter.addWidget(center_panel)

        # # 右侧面板
        # right_panel = QTextEdit()
        # right_panel.setPlaceholderText("Properties")
        # splitter.addWidget(right_panel)

        # layout = QVBoxLayout()
        # layout.addWidget(splitter)
        # central_widget.setLayout(layout)

        # 创建一个顶部停靠窗口
        top_dock = QDockWidget("top", self)
        top_dock.setWidget(QTextEdit())
        self.addDockWidget(Qt.TopDockWidgetArea, top_dock)
        top_dock.setAllowedAreas(Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea | Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        # 创建一个底部停靠窗口
        bottom_dock = QDockWidget("Console", self)
        bottom_dock.setWidget(QTextEdit())
        self.addDockWidget(Qt.BottomDockWidgetArea, bottom_dock)
    
        # 创建一个左侧停靠窗口
        left_dock = QDockWidget("Project Explorer", self)
        left_dock.setWidget(QTextEdit())
        self.addDockWidget(Qt.LeftDockWidgetArea, left_dock)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CodeEditorExample()
    ex.show()
    sys.exit(app.exec_())