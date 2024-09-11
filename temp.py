import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QToolBar, QColorDialog, QFontDialog
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont, QAction


class EditableTextEdit(QTextEdit):
    editingChanged = Signal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("border: none;")
        self.setReadOnly(True)
        self.is_locked = True

    def mouseDoubleClickEvent(self, event):
        self.setReadOnly(False)
        self.is_locked = False
        self.editingChanged.emit(self.is_locked)
        print("Editing mode enabled.")
        super().mouseDoubleClickEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
            self.setReadOnly(True)  # Ctrl+S 锁定文本框
            self.is_locked = True
            self.editingChanged.emit(self.is_locked)  # 发出编辑模式锁定的信号
            print("Editing mode locked.")
        else:
            super().keyPressEvent(event)  # 继续处理其他按键事件


class TextEditorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.base_window_title = "Text Editor with Style Options"  # 基础窗口标题
        self.setWindowTitle(self.base_window_title)
        self.resize(800, 600)

        self.title_edit = EditableTextEdit()
        self.title_edit.setPlaceholderText("Enter Title Here")
        self.title_edit.setStyleSheet("font-size: 24px; font-weight: bold; border: none;")  # 固定样式
        self.title_edit.editingChanged.connect(self.update_window_title)  # 连接信号到槽

        self.text_edit = EditableTextEdit()
        self.text_edit.editingChanged.connect(self.update_window_title)  # 连接信号到槽

        self.toolbar = self.addToolBar("Text Formatting")

        font_action = QAction("Font", self)
        font_action.triggered.connect(self.change_font)
        self.toolbar.addAction(font_action)

        font_size_action = QAction("Font Size", self)
        font_size_action.triggered.connect(self.change_font_size)
        self.toolbar.addAction(font_size_action)

        font_color_action = QAction("Font Color", self)
        font_color_action.triggered.connect(self.change_font_color)
        self.toolbar.addAction(font_color_action)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.title_edit)
        layout.addWidget(self.text_edit)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_window_title(self, is_locked):
        """更新窗口标题，未锁定时显示 *，锁定后移除 *"""
        print("is_locked:", is_locked)
        if is_locked:
            self.setWindowTitle(self.base_window_title)
        else:
            self.setWindowTitle(self.base_window_title + " *")  # 标题加上 * 表示未锁定

    def change_font(self):
        flag, font = QFontDialog.getFont(self)
        if flag:
            self.text_edit.set_font(font)

    def change_font_size(self):
        flag, font = QFontDialog.getFont(self)
        if flag:
            size = font.pointSize()
            self.text_edit.set_font_size(size)

    def change_font_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_edit.set_font_color(color)

    def get_text_content(self):
        """获取正文内容"""
        return self.text_edit.toPlainText()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextEditorApp()
    window.show()
    sys.exit(app.exec())
