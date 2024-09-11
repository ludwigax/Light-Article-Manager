from PySide6.QtWidgets import QMenu, QWidget
from PySide6.QtCore import Qt, QPoint, QEvent
from PySide6.QtGui import QMouseEvent, QAction

def folder_right_click_menu(widget: QWidget, pos: QPoint):
    menu = QMenu(widget)

    act_add_folder = QAction("Add Folder", widget)
    act_add_folder.triggered.connect(widget.window().onFolderAddClicked)
    menu.addAction(act_add_folder)

    act_add_article = QAction("Add Article", widget)
    handle = lambda : widget.window().onFolderArticleAddClicked(widget, widget.node_id)
    act_add_article.triggered.connect(handle)
    menu.addAction(act_add_article)

    act_rename = QAction("Rename Folder", widget)
    event = QMouseEvent(QEvent.MouseButtonPress, QPoint(0, 0), Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
    handle = lambda : widget.SetEditMode(widget, (event, ))
    act_rename.triggered.connect(handle)
    menu.addAction(act_rename)

    act_del = QAction("Delete Folder", widget) # TODO
    act_del.triggered.connect(widget.RemoveNode)
    menu.addAction(act_del)

    menu.exec_(widget.mapToGlobal(pos))