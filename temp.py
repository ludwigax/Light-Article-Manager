from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QToolBar, QTextBrowser, QAction
from PyQt5.QtCore import Qt, QRect

class SubWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        
        # 创建工具栏
        toolbar = QToolBar("Toolbar", self)
        
        # 添加一个动作到工具栏
        test_action = QAction("Test", self)
        test_action.triggered.connect(self.test_temp)
        toolbar.addAction(test_action)
        
        # 创建 QTextBrowser
        text_browser = QTextBrowser(self)
        text_browser.setHtml('<h1>HTML Content</h1><p>This is a QTextBrowser displaying HTML content.</p>')
        
        layout.addWidget(toolbar)
        layout.addWidget(text_browser)
        
        self.setLayout(layout)
    
    def test_temp(self):
        print("Test action triggered!")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Main Window')
        
        # 创建子窗口
        self.sub_window = SubWindow(self)
        self.sub_window.setWindowTitle('Sub Window')
        
        # 设置子窗口无边框
        # self.sub_window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        # 初始对齐子窗口位置和大小
        self.align_sub_window()
        
        self.show()
        self.sub_window.show()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.align_sub_window()
    
    def moveEvent(self, event):
        super().moveEvent(event)
        self.align_sub_window()
    
    def align_sub_window(self):
        main_geom = self.geometry()
        x = main_geom.right()
        y = main_geom.top()
        width = main_geom.width() // 2
        height = main_geom.height()
        
        self.sub_window.setGeometry(QRect(x, y, width, height))

if __name__ == '__main__':
    app = QApplication([])
    
    main_window = MainWindow()
    
    app.exec_()
