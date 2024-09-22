from PySide6.QtWidgets import QPlainTextEdit, QTextBrowser, QTextEdit, QLabel, QWidget, QLineEdit
from PySide6.QtGui import QKeyEvent, QMouseEvent, QTextCursor, QTextCharFormat, QColor, QTextDocument, QFontMetrics
from PySide6.QtCore import Qt

class Modifier:
    def setHook(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


# slot functions --------------------------------------------------------------
def setTextEditFit(widget: QPlainTextEdit): # slot function
    # font_metrics = QFontMetrics(widget.font())
    line_count = widget.document().lineCount()
    # print(line_count, font_metrics.lineSpacing())
    widget.setFixedHeight(line_count * 16 + 12) # 16 is the line spacing, 12 is the padding


# modified widgets -----------------------------------------------------------
class LPlainTextEdit(QPlainTextEdit, Modifier):
    def __init__(self, parent=None):
        super().__init__(parent)

    def setTextChangedSlot(self, slot="edit_fit"):
        self.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        if slot == "edit_fit":
            self.textChanged.connect(lambda: setTextEditFit(self))

    def keyPressEvent(self, ev: QKeyEvent) -> None:
        if hook := getattr(self, "keyPress_hook", None):
            ret = hook(self, params=(ev,))
            if state := getattr(self, "keyPress_state", None) is False or (ret==0):
                return super().keyPressEvent(ev)
        else:
            return super().keyPressEvent(ev)
        # if e.key() == Qt.Key_Return and e.modifiers() == Qt.ControlModifier:
        #     self.parent().parent()._onSearchClicked()
        # else:
        #     return super().keyPressEvent(e)

class LTextBrowser(QTextBrowser, Modifier):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        # parent() -> LItem -> QListWidget -> LMainWindow
        if hook := getattr(self, "mousePress_hook", None):
            ret = hook(self, params=(ev,))
            if state := getattr(self, "mousePress_state", None) is False or (ret==0):
                return super().mousePressEvent(ev)
        else:
            return super().mousePressEvent(ev)
    
    def mouseDoubleClickEvent(self, ev: QMouseEvent) -> None:
        # parent() -> LMainWindow
        if hook := getattr(self, "mouseDoubleClick_hook", None):
            ret = hook(self, params=(ev,))
            if state := getattr(self, "mouseDoubleClick_state", None) is False or (ret==0):
                return super().mouseDoubleClickEvent(ev)
        else:
            return super().mouseDoubleClickEvent(ev)
        
class LLabel(QLabel, Modifier):
    def __init__(self, parent=None, enabled=True):
        super().__init__(parent)
        self.full_text = None
        self.setWordWrap(False)
        self.enabled = enabled
        if self.enabled:
            self.updateElidedText()

    def setFullText(self, text: str):
        self.full_text = text
        self.updateElidedText()

    def updateElidedText(self):
        if not self.full_text:
            text = self.text()
        else:
            text = self.full_text
        metrics = QFontMetrics(self.font())
        elided_text = metrics.elidedText(text, Qt.ElideRight, self.width())
        self.setText(elided_text)
        if text != elided_text:
            self.setToolTip(text)
        else:
            self.setToolTip(None)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.enabled:
            self.updateElidedText()

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        # parent() -> LItem -> QTreeWidget -> LMainWindow
        if hook := getattr(self, "mousePress_hook", None):
            ret = hook(self, params=(ev,))
            if state := getattr(self, "mousePress_state", None) is False or (ret==0):
                return super().mousePressEvent(ev)
        else:
            return super().mousePressEvent(ev)
        
    def mouseDoubleClickEvent(self, ev: QMouseEvent) -> None:
        if hook := getattr(self, "mouseDoubleClick_hook", None):
            ret = hook(self, params=(ev,))
            if state := getattr(self, "mouseDoubleClick_state", None) is False or (ret==0):
                return super().mouseDoubleClickEvent(ev)
        else:
            return super().mouseDoubleClickEvent(ev)
        
class LLineEdit(QLineEdit, Modifier):
    def __init__(self, parent=None):
        super().__init__(parent)

    def focusOutEvent(self, event):
        if hook := getattr(self, "focusOut_hook", None):
            ret = hook(self, params=(event,))
            if state := getattr(self, "focusOut_state", None) is False or (ret==0):
                return super().focusOutEvent(event)
        else:
            return super().focusOutEvent(event)
        
class LTextEdit(QTextEdit, Modifier): # TODO
    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, ev: QKeyEvent) -> None:
        if hook := getattr(self, "keyPress_hook", None):
            ret = hook(self, params=(ev,))
            if state := getattr(self, "keyPress_state", None) is False or (ret==0):
                return super().keyPressEvent(ev)
        else:
            return super().keyPressEvent(ev)
        
class SearchTextEdit(LTextEdit, Modifier):
    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() == Qt.Key_Tab:
            self.handleTab()
        else:
            super().keyPressEvent(e)
            cursor = self.textCursor()
            cursor = self.moveOutSpecialText(e.key(), cursor)
            self.setTextCursor(cursor)
    
    def mousePressEvent(self, e: QMouseEvent) -> None:
        super().mousePressEvent(e)
        cursor = self.textCursor()
        if self.isSpecialText(cursor):
            cursor = self.moveOutSpecialText(Qt.Key_Left, cursor)
            self.setTextCursor(cursor)
        
    def handleTab(self):
        cursor = self.textCursor()
        
        cursor_s, flag_s = self.findSpliter(backward=True)
        cursor_e, flag_e = self.findSpliter()
        print(cursor_s.position(), cursor_e.position())

        cursor_s.setPosition(cursor_e.position(), QTextCursor.KeepAnchor)
        text = cursor_s.selectedText()
        print(text)

        charFormat = QTextCharFormat()
        charFormat.setForeground(QColor('blue'))
        charFormat.setBackground(QColor('lightgray'))
        
        if text.strip():
            # if not flag_s:
            #     text = "||" + text
            # if not flag_e:
            #     text = text + "||"
            text = "||" + text.strip() + "||"
            cursor_s.insertText(" ", QTextCharFormat())
            cursor_s.insertText(text, charFormat)
            cursor_s.insertText(" ", QTextCharFormat())
            if not flag_e:
                cursor_s.insertText(" ", QTextCharFormat())

        self.viewport().update()

    def findSpliter(self, text: str = "||", backward: bool = False):
        cursor = self.textCursor()
        flag = True
        if backward:
            cursor_a = self.document().find(text, cursor, QTextDocument.FindBackward)
            if cursor_a.isNull():
                cursor_a = QTextCursor(self.document())
                cursor_a.movePosition(QTextCursor.Start)
                flag = False
            else:
                cursor_a.setPosition(cursor_a.position() + 1)
        else:
            cursor_a = self.document().find(text, cursor)
            if cursor_a.isNull():
                cursor_a = QTextCursor(self.document())
                cursor_a.movePosition(QTextCursor.End)
                flag = False
            else:
                cursor_a.setPosition(cursor_a.position() - 3)
        return cursor_a, flag
    
    def isSpecialText(self, cursor):
        format = cursor.charFormat()
        return format.background().color() == QColor('lightgray')
    
    def moveOutSpecialText(self, key, cursor):
        if key == Qt.Key_Left:
            while self.isSpecialText(cursor) and not cursor.atBlockStart():
                cursor.movePosition(QTextCursor.Left)
            cursor.movePosition(QTextCursor.Left) # add one offset
        elif key == Qt.Key_Right:
            while self.isSpecialText(cursor) and not cursor.atBlockEnd():
                cursor.movePosition(QTextCursor.Right)
        return cursor