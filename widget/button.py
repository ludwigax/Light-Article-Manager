from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDragEnterEvent, QDropEvent

import utils.opn as opn
import utils.format as fmt

import shutil
from widget.emitter import emitter

BUTTON_STYLES = {
    "default": "",
    "GREEN": """
    QPushButton {
        border: 2px solid #5cb85c;
        background-color: #dff0d8;
        color: #3c763d;
    }
    QPushButton:pressed {
        background-color: #c1e2b3;
        border: 2px solid #4cae4c;
    }
    """,
    "PURPLE": """
    QPushButton {
        border: 2px solid #6f42c1;
        background-color: #e2d3f1;
        color: #563d7c;
    }
    QPushButton:pressed {
        background-color: #cbb2e4;
        border: 2px solid #5a36a6;
    }
    """,
    "RED": """
    QPushButton {
        border: 2px solid #d9534f;
        background-color: #f2dede;
        color: #a94442;
    }
    QPushButton:pressed {
        background-color: #e6b9b8;
        border: 2px solid #c9302c;
    }
    """,
    "BLUE": """
    QPushButton {
        border: 2px solid #337ab7;
        background-color: #d9edf7;
        color: #2e6da4;
    }
    QPushButton:pressed {
        background-color: #bcdff1;
        border: 2px solid #286090;
    }
    """,
    "GREY_DASHED": """
    QPushButton {
        border: 2px dashed #aaa;
        background-color: #f0f0f0;
    }
    """
}

def StyleButton(clf, style):
    button = QPushButton(clf)
    button.setStyleSheet(BUTTON_STYLES[style])
    return button

class PDFDropButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("")
        self.setAcceptDrops(True)
        self.pdf_path = None
        self.article_id = None

    def init_data(self, pdf_path, article_id):
        print("ARTICLE ID:", article_id)

        if article_id is None:
            self.setEnabled(False)
        else:
            self.setEnabled(True)

        self.pdf_path = pdf_path
        self.article_id = article_id
        if not self.pdf_path:
            self.setText("Drop PDF File")
            self.setStyleSheet(False)
        else:
            self.setText("Open PDF File")
            self.setStyleSheet(True)

    def clear_data(self):
        self.pdf_path = None
        self.article_id = None
        self.setText("Drop PDF File")
        self.setStyleSheet(False)

    def setStyleSheet(self, is_pdf):
        if is_pdf:
            super().setStyleSheet(BUTTON_STYLES["GREEN"])
        else:
            super().setStyleSheet(BUTTON_STYLES["GREY_DASHED"])

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if self.article_id and len(urls) == 1 and urls[0].toLocalFile().endswith(".pdf"):
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        file_path = urls[0].toLocalFile()
        if file_path.endswith(".pdf"):
            self.setText("Open PDF File")
            self.setStyleSheet(True)
            article = opn.get_article(self.article_id)
            local_path = opn.get_related_path(file_path)
            article.local_path = local_path # TODO fatal error
            import func
            func.global_session().commit()
            shutil.copyfile(file_path, opn.get_absolute_path(local_path))
            self.pdf_path = opn.get_absolute_path(local_path)
            emitter.render_main_browser.emit(self.article_id)

    def mousePressEvent(self, event):
        if not self.pdf_path:
            return
        opn.open_file(self.pdf_path)
        return super().mousePressEvent(event)