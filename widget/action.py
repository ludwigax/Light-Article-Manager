import os
from typing import List, Tuple

from PySide6.QtWidgets import QWidget, QListWidgetItem, QTreeWidgetItem, QTreeWidget, QListWidget, \
    QPlainTextEdit
from database import Article, Keyword, Note
import utils.format as fmt
import utils.opn as opn

from sylva import ArticleData, NoteData

from func import global_session

def getArticle(article: int | Article) -> Article:
    if isinstance(article, int):
        article = opn.get_article(article)
    return article

def checkPath(path: str):
    if os.path.exists(str(path)):
        return True
    return False

def setTextEditFit(widget: QPlainTextEdit): # hook function
    # font_metrics = QFontMetrics(widget.font())
    line_count = widget.document().lineCount()
    # print(line_count, font_metrics.lineSpacing())
    widget.setFixedHeight(line_count * 16 + 12) # 16 is the line spacing, 12 is the padding

def addKeywords(keywords: List[str], article: Article | int = None):
    article = getArticle(article)
    opn.add_keywords(opn.create_keywords(keywords), article)

def addNote(data: NoteData, article: Article | int = None):
    article = getArticle(article)
    opn.add_note(opn.create_note(data), article)

def resetKeywords(keywords: List[str], article: Article | int = None):
    article = getArticle(article)
    opn.reset_keywords(opn.create_keywords(keywords), article)

def resetArticle(data: ArticleData, article: Article | int = None):
    article = getArticle(article)
    opn.reset_article(data, article)

def resetNote(data: ArticleData, note: Note | int):
    if isinstance(note, int):
        note = opn.get_note(note)
    opn.reset_note(data, note)

def removeKeywords(article: Article | int = None):
    article = getArticle(article)
    opn.reset_keywords([], article)

def deleteArticle(article_id: int):
    opn.delete_article(article_id)

def deleteArticleCascade(article_id: int):
    opn.cascade_delete_article(article_id)

def deleteNote(note_id: int):
    opn.delete_note(note_id)

def openAritcleFile(path: str):
    try:
        fmt.open_path(path)
    except Exception as e:
        return False
    return True

# --------------------------------------------------------------------------------
# basic operations
def setListWidget(widget_obj, listWidget: QListWidget, content_list: List[Tuple[str, int]]):
    for content, id in content_list:
        widget = widget_obj(id)
        widget.SetItemText(content)
        addListWidgetItem(widget, listWidget)

def clearListWidget(listWidget: QListWidget, start=0):
    while listWidget.count() > start:
        item = listWidget.takeItem(start)
        widget = listWidget.itemWidget(item)
        if widget:
            widget.deleteLater()
        del item

def addListWidgetItem(widget: QWidget, listWidget: QListWidget):
    item = QListWidgetItem(listWidget)
    item.setSizeHint(widget.sizeHint())
    listWidget.addItem(item)
    listWidget.setItemWidget(item, widget)

def removeListWidgetItem(widget: QWidget, listWidget: QListWidget):
    item = listWidget.itemAt(widget.pos())
    listWidget.takeItem(listWidget.row(item))
    widget.deleteLater()
    del item

def addTreeWidgetItem(widget: QWidget, parent_item: QTreeWidgetItem, treeWidget: QTreeWidget) -> QTreeWidgetItem:
    item = QTreeWidgetItem(parent_item)
    treeWidget.setItemWidget(item, 0, widget)
    return item

def removeTreeWidgetItem(widget: QWidget, treeWidget: QTreeWidget):
    item = treeWidget.itemAt(widget.pos())

    def remove_item_and_children(item):
        while item.childCount() > 0:
            child = item.child(0)
            remove_item_and_children(child)
            item.removeChild(child)

        parent = item.parent()
        if parent:
            parent.removeChild(item)
        else:
            index = treeWidget.indexOfTopLevelItem(item)
            treeWidget.takeTopLevelItem(index)

        widget = treeWidget.itemWidget(item, 0)
        if widget:
            widget.deleteLater()
        item = None

    remove_item_and_children(item)

def clearTreeWidget(treeWidget: QTreeWidget):
    treeWidget.clear()