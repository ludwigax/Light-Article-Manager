import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QFrame, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt

class KeyValueWidget(QWidget):
    def __init__(self, key, value, status_color):
        super().__init__()

        layout = QHBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

        # 创建key标签
        self.key_label = QLabel(key)
        self.key_label.setFrameShape(QFrame.Panel)
        self.key_label.setFrameShadow(QFrame.Sunken)
        self.key_label.setLineWidth(2)
        self.key_label.setAlignment(Qt.AlignCenter)
        # 使用更严肃的样式，取消背景色和圆角，保持系统风格
        self.key_label.setStyleSheet("""
            font-weight: bold;
            font-size: 12px;
            color: #013e5d;
            background-color: none;
        """)

        # 创建value标签
        self.value_label = QLabel(value)
        self.value_label.setFrameShape(QFrame.Panel)
        self.value_label.setFrameShadow(QFrame.Sunken)
        self.value_label.setLineWidth(2)
        self.value_label.setAlignment(Qt.AlignCenter)

        # 设置value的颜色根据状态
        self.value_label.setStyleSheet(f"color: {status_color}; font-weight: bold;")

        # 将key和value添加到布局
        layout.addWidget(self.key_label)
        layout.addWidget(self.value_label)

        # 设置这个widget的布局
        self.setLayout(layout)


class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout()

        # 设置间距为5，使布局更紧凑
        layout.setSpacing(15)
        # layout.setContentsMargins(3, 3, 3, 3)

        # 创建四个 KeyValueWidget 作为key和value对
        google_widget = KeyValueWidget("GOOGLE", "OK", "green")
        crossref_widget = KeyValueWidget("CROSSREF", "NO", "red")
        wos_widget = KeyValueWidget("WOS", "OK", "green")
        arxiv_widget = KeyValueWidget("ARXIV", "NO", "red")

        # 在布局中添加这四个控件
        layout.addWidget(google_widget, 0, 0)
        layout.addWidget(crossref_widget, 0, 1)
        layout.addWidget(wos_widget, 0, 2)
        layout.addWidget(arxiv_widget, 0, 3)

        # 第二行：Google账号, 账号名称, WOS凭据, 凭据名称
        google_account_widget = KeyValueWidget("GOOGLE ACCOUNT", "my_google_account", "black")
        wos_credentials_widget = KeyValueWidget("WOS TOKEN", "my_wos_credentials", "black")

        # 在布局中添加第二行的控件
        layout.addWidget(google_account_widget, 1, 0, 1, 2)
        layout.addWidget(wos_credentials_widget, 1, 2, 1, 2)

        # 设置控件的网格布局
        self.setLayout(layout)


# 创建应用程序实例
app = QApplication(sys.argv)

# 创建 DashboardWidget 的实例
dashboard = DashboardWidget()
dashboard.setWindowTitle("仪表盘示例")
dashboard.resize(800, 200)  # 设置窗口大小
dashboard.show()

# 启动应用程序事件循环
sys.exit(app.exec())
