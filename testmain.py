import json
from PySide6.QtWidgets import QApplication, QListWidgetItem, QVBoxLayout, QWidget, QListWidget
from PySide6.QtCore import QMimeData, Qt, QPoint
from PySide6.QtGui import QDrag


class MetaItem(QListWidgetItem):
    def __init__(self, metadata):
        super().__init__(metadata.get("title"))
        self._metadata = metadata

    def setMetaData(self, metadata):
        self._metadata = metadata
        return super().setText(self._metadata.get("title"))

    def metadata(self):
        return self._metadata


class DragListWidget(QListWidget):
    def __init__(self, drop_in=True, drag_out=True):
        super().__init__()
        self.dragging = True
        self.start_point = QPoint()
        self.drag_out = drag_out
        self.setAcceptDrops(drop_in)
        self.setDropIndicatorShown(True)

    def dragEnterEvent(self, event):
        if self.drag_out and event.mimeData().hasFormat("application/octet-stream"):
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if self.drag_out and event.mimeData().hasFormat("application/octet-stream"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/octet-stream"):
            item_data = event.mimeData().data("application/octet-stream")
            meta_data = json.loads(item_data.data().decode())
            drop_index = self.indexAt(QPoint(event.position().x(), event.position().y()))
            if drop_index.isValid():
                self.insertItem(drop_index.row(), MetaItem(meta_data))
            else:
                self.addItem(MetaItem(meta_data))
            event.acceptProposedAction()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_point = event.position().toPoint()
            item: MetaItem = self.itemAt(self.start_point)
            if item:
                self.dragging = True
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not self.dragging:
            super().mouseMoveEvent(event)
        distance = (event.position().toPoint() - self.start_point).manhattanLength()
        if distance >= QApplication.startDragDistance():
            item: MetaItem = self.itemAt(self.start_point)
            mime_data = QMimeData()
            mime_data.setData("application/octet-stream", json.dumps(item.metadata()).encode())
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            if drag.exec(Qt.MoveAction) == Qt.MoveAction:
                self.takeItem(self.row(item))
            self.dragging = False

    def mouseReleaseEvent(self, event):
        self.dragging = False
        super().mouseReleaseEvent(event)
        


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # 创建两个 DragListWidget 实例
        self.list_widget_1 = DragListWidget(True, True)
        self.list_widget_2 = DragListWidget(True, True)

        # 添加项目到第一个列表
        meta_data_1 = {"title": "Item 1"}
        meta_data_2 = {"title": "Item 2"}
        self.list_widget_1.addItem(MetaItem(meta_data_1))
        self.list_widget_1.addItem(MetaItem(meta_data_2))

        # 添加项目到第二个列表
        meta_data_3 = {"title": "Item 3"}
        meta_data_4 = {"title": "Item 4"}
        self.list_widget_2.addItem(MetaItem(meta_data_3))
        self.list_widget_2.addItem(MetaItem(meta_data_4))

        layout.addWidget(self.list_widget_1)
        layout.addWidget(self.list_widget_2)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
