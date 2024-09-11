from PySide6.QtWidgets import QTextEdit
from PySide6.QtCore import Qt, Signal

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
            self.setReadOnly(True)
            if not self.is_locked:
                self.is_locked = True
                self.editingChanged.emit(self.is_locked) 
                print("Editing mode locked.")
        else:
            super().keyPressEvent(event)