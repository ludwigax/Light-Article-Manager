from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QLabel


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        # 主布局
        main_layout = QVBoxLayout()

        # 按钮容器布局
        button_layout = QHBoxLayout()

        # 按钮列表
        self.buttons = []
        for i in range(4):
            button = QPushButton(f"按钮 {i+1}")
            button.clicked.connect(self.create_button_handler(i))
            self.buttons.append(button)
            button_layout.addWidget(button)

        # StackedWidget 用来存放多个页面
        self.stacked_widget = QStackedWidget()

        # 添加页面到 QStackedWidget
        for i in range(4):
            page = self.create_page(i)
            self.stacked_widget.addWidget(page)

        # 将按钮布局和 StackedWidget 添加到主布局
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.stacked_widget)

        # 设置窗口布局
        self.setLayout(main_layout)

    def create_button_handler(self, index):
        # 这个函数返回一个槽函数，用于切换到指定的页面
        def button_handler():
            self.stacked_widget.setCurrentIndex(index)

        return button_handler

    def create_page(self, index):
        # 创建不同的页面，页面上只是显示一个标签
        page = QWidget()
        layout = QVBoxLayout()
        label = QLabel(f"页面 {index + 1}")
        layout.addWidget(label)
        page.setLayout(layout)
        return page


if __name__ == "__main__":
    app = QApplication([])

    # 创建并展示主窗口
    window = MainWindow()
    window.setWindowTitle("QStackedWidget 页面切换")
    window.resize(400, 300)
    window.show()

    app.exec()
