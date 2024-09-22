from PySide6.QtCore import Qt, QModelIndex
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon, QAction
from PySide6.QtWidgets import QMenu

from mvc.model import SearchProxyModel, BinestedItem
from mvc.model import COLUMNS_WIDTH
from mvc.base import BaseModule

from widget.dialog import (
    new_article_dialog, modify_article_dialog, delete_article_dialog, \
    new_article_sylva_dialog, rename_folder_sylva_dialog, \
)
from widget.emitter import emitter

from sylva import NamedDict, FolderData
import utils.opn as opn
from utils.opn import to_data
import utils.combo as cb

class ModelViewModule(BaseModule):
    def __init__(self, parent, columns=None):
        super().__init__(parent, columns)
        self.set_slots()
    
    def enable_context_menu(self):
        if not self.menu:
            self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
            self.tree_view.customContextMenuRequested.connect(self.context_menu)
            self._menu = True

    def disable_context_menu(self):
        if self.menu:
            self.tree_view.setContextMenuPolicy(Qt.NoContextMenu)
            self.tree_view.customContextMenuRequested.disconnect(self.context_menu)
            self._menu = False
    
    def context_menu(self, point):
        raise NotImplementedError("Method not allowed")

    def set_delegate(self, col_idx: int, delegate: object):
        self.tree_view.setItemDelegateForColumn(col_idx, delegate(self.tree_view))
    
    def set_slots(self):
        self.tree_view.header().sectionClicked.connect(self._sort_by_column)
        # self.tree_view.header().sectionDoubleClicked.connect(self._sort_by_column) # TODO disabled
        self.tree_view.clicked.connect(self._row_selected)
        self.tree_view.doubleClicked.connect(self._row_focused_selected)

    # slots function
    def _sort_by_column(self, col_idx: int):
        print(f"Header clicked: {self.model.headerData(col_idx, Qt.Horizontal)} (Index: {col_idx})")
        col_idx, sort_order = self.sort_proxy_model(col_idx)

    def _sort_by_search(self, text: str):
        if text == "":
            self.proxy_model.resetOrder()
            return
        self.search_proxy_model(text, 0)

    def _row_selected(self, index):
        source_index = self.proxy_model.mapToSource(index)
        print(f"Row selected: {source_index.row()}")

        source_index = source_index.siblingAtColumn(0)
        item = self.model.itemFromIndex(source_index)
        if item.item_type == 1:
            return
        # outside function
        cb.row_selected(index, item.id)
        # end

    def _row_focused_selected(self, index):
        source_index = self.proxy_model.mapToSource(index)
        print(f"Row focused selected: {source_index.row()}")

        source_index = source_index.siblingAtColumn(0)
        item = self.model.itemFromIndex(source_index)
        if item.item_type == 1:
            return
        # outside function
        cb.row_focused_selected(index, item.id)
        # end

class NonNestedModule(ModelViewModule):
    def __init__(self, parent, columns=None):
        super().__init__(parent, columns)
        self.enable_context_menu()

    def set_slots(self):
        emitter.new_article.connect(self._new_article)
        emitter.modify_article.connect(self._modify_article)
        emitter.delete_article.connect(self._delete_article)
        return super().set_slots()

    def context_menu(self, point):
        index = self.tree_view.indexAt(point)
        index = index.siblingAtColumn(0)
        source_index = self.proxy_model.mapToSource(index)

        menu = QMenu(self.tree_view)
        action_list = []

        sort_action = QAction("Sort", self.tree_view)
        sort_action.triggered.connect(self.menu_sort)
        menu.addAction(sort_action)
        menu.addSeparator()

        new_article_action = QAction("New", self.tree_view)
        new_article_action.triggered.connect(lambda: self.menu_new_article(source_index))
        menu.addAction(new_article_action)

        if index.isValid():
            modify_article_action = QAction("Modify", self.tree_view)
            delete_article_action = QAction("Delete", self.tree_view)
            modify_article_action.triggered.connect(lambda: self.menu_modify_article(source_index))
            delete_article_action.triggered.connect(lambda: self.menu_delete_article(source_index))
            menu.addActions([modify_article_action, delete_article_action])

        menu.exec_(self.tree_view.viewport().mapToGlobal(point))

    # menu function
    def menu_sort(self):
        self.proxy_model.sort_order = Qt.DescendingOrder
        col_idx, sort_order = self.sort_proxy_model(0)
        self.tree_view.header().setSortIndicator(0, Qt.AscendingOrder)

    def menu_new_article(self, index):
        data = new_article_dialog(self.parent(), None)
        if not data:
            return
        cb.new_article(index, -1, data)

    def menu_modify_article(self, index):
        item = self.model.itemFromIndex(index)
        article = opn.get_article(item.id)
        data = modify_article_dialog(self.parent(), article)
        if not data:
            return
        cb.modify_article(index, item.id, data)

    def menu_delete_article(self, index):
        item = self.model.itemFromIndex(index)
        if not delete_article_dialog(self.parent()):
            return
        cb.delete_article(index, item.id)

    # slots function
    def _new_article(self, index, data: NamedDict = None):
        self.append_item(data)

    def _modify_article(self, index, data: NamedDict = None):
        self.remove_item(index)
        self.insert_item(data, index)

    def _delete_article(self, index):
        self.remove_item(index)

class NestedModule(ModelViewModule):
    def __init__(self, parent, columns=None):
        super().__init__(parent, columns)
        self.set_nested(True)
        self.enable_context_menu()

    def append_item(self, item_type: int, data: NamedDict = None, index = None): # folder_idx: 0, -1
        if item_type == 0 and index is None:
            raise AttributeError("Article cannot add to ROOT!")
        row = self.package_item(1, item_type, data = data)
        if not index:
            self.model.appendRow(row)
        else:
            item = self.model.itemFromIndex(index)
            item.appendRow(row)
        return row
    
    def insert_item(self, item_type: int, data: NamedDict = None, index = None, offset = 0):
        if self.item_level(index) == 1:
            index = index.parent()
        item = self.package_item(1, item_type, data = data)
        if item_type == 1:
            row_idx = index.row()
            self.model.insertRow(row_idx + offset, item)
        else:
            upper_item = self.model.itemFromIndex(index)
            upper_item.appendRow(item)

    def remove_item(self, index):
        if self.item_level(index) == 1:
            parent_index = index.parent()
            parent_item = self.model.itemFromIndex(parent_index)
            if parent_item:
                parent_item.removeRow(index.row())
        else:
            self.model.removeRow(index.row())
    
    def item_level(self, index):
        level = 0
        while index.parent().isValid():
            index = index.parent()
            level += 1
        return level
    
    def search_proxy_model(self, text: str, col_idx: int = 0):
        # override function
        indices = {}
        if self.proxy_model.external_indices:
            self.proxy_model.resetOrder()

        top_row_count = self.proxy_model.rowCount()

        for top_row in range(top_row_count):
            top_index = self.proxy_model.index(top_row, 0)
            top_source_index = self.proxy_model.mapToSource(top_index)

            key = -1
            indices.setdefault(key, []).append(top_source_index.row())

            child_row_count = self.proxy_model.rowCount(top_index)

            for child_row in range(child_row_count):
                child_index = self.proxy_model.index(child_row, col_idx, top_index)
                child_source_index = self.proxy_model.mapToSource(child_index)

                data = self.proxy_model.data(child_index, role=Qt.DisplayRole)
                if data is None:
                    continue
                
                data = data.lower()
                if text.lower() not in data:
                    continue

                key = child_source_index.parent().row()
                indices.setdefault(key, []).append(child_source_index.row())
        self.proxy_model.setExternalOrder(indices)
        print(indices)
        return col_idx, self.proxy_model.sort_order
    
    def set_slots(self):
        emitter.new_article_sylva.connect(self._new_article_sylva)
        emitter.remove_article_sylva.connect(self._remove_article_sylva)
        emitter.new_folder_sylva.connect(self._new_folder_sylva)
        emitter.rename_folder_sylva.connect(self._rename_folder_sylva)
        emitter.delete_folder_sylva.connect(self._delete_folder_sylva)
        return super().set_slots()
    
    def context_menu(self, point):
        index = self.tree_view.indexAt(point)
        index = index.siblingAtColumn(0)
        source_index = self.proxy_model.mapToSource(index)
        item: BinestedItem = self.model.itemFromIndex(source_index)

        menu = QMenu(self.tree_view)

        sort_action = QAction("Sort", self.tree_view)
        sort_action.triggered.connect(self.menu_sort)
        menu.addAction(sort_action)
        menu.addSeparator()

        if index.isValid():
            new_article_action = QAction("New Article", self.tree_view)
            new_article_action.triggered.connect(lambda: self.menu_new_article_sylva(source_index))
            menu.addAction(new_article_action)

            if item.item_type == 0:
                modify_article_action = QAction("Modify Article", self.tree_view)
                modify_article_action.triggered.connect(lambda: self.menu_modify_article(source_index))
                remove_article_action = QAction("Remove Article", self.tree_view)
                remove_article_action.triggered.connect(lambda: self.menu_remove_article_sylva(source_index))
                menu.addActions([modify_article_action, remove_article_action])
            menu.addSeparator()

        new_folder_action = QAction("New Folder", self.tree_view)
        new_folder_action.triggered.connect(lambda: self.menu_new_folder_sylva(source_index))
        menu.addAction(new_folder_action)

        if index.isValid() and item.item_type == 1:
            rename_folder_action = QAction("Rename Folder", self.tree_view)
            delete_folder_action = QAction("Delete Folder", self.tree_view)
            rename_folder_action.triggered.connect(lambda: self.menu_rename_folder_sylva(source_index))
            delete_folder_action.triggered.connect(lambda: self.menu_delete_folder_sylva(source_index))
            menu.addActions([rename_folder_action, delete_folder_action])

        menu.exec_(self.tree_view.viewport().mapToGlobal(point))

    # menu function
    def menu_sort(self):
        self.proxy_model.sort_order = Qt.DescendingOrder
        col_idx, sort_order = self.sort_proxy_model(0)
        self.tree_view.header().setSortIndicator(0, Qt.AscendingOrder)

    def menu_new_article_sylva(self, index):
        id_list = new_article_sylva_dialog(self.parent())
        if not id_list:
            return
        if self.item_level(index) == 1:
            index = index.parent()
        item = self.model.itemFromIndex(index)
        for id in id_list:
            cb.new_article_sylva(index, item.id, id)

    def menu_remove_article_sylva(self, index):
        item = self.model.itemFromIndex(index)
        parent_item = item.parent()
        cb.remove_article_sylva(index, parent_item.id, index.row())

    def menu_new_folder_sylva(self, index):
        if index.isValid() and self.item_level(index) == 1:
            index = index.parent()
        if index.isValid():
            idx1 = index.row()
        else:
            idx1 = self.model.rowCount() - 1
        cb.new_folder_sylva(index, None, idx1)

    def menu_rename_folder_sylva(self, index):
        text = rename_folder_sylva_dialog(self.parent())
        if not text:
            return
        item = self.model.itemFromIndex(index)
        cb.rename_folder_sylva(index, item.id, text)

    def menu_delete_folder_sylva(self, index):
        item = self.model.itemFromIndex(index)
        cb.delete_folder_sylva(index, item.id)

    def menu_modify_article(self, index):
        item = self.model.itemFromIndex(index)
        article = opn.get_article(item.id)
        data = modify_article_dialog(self.parent(), article)
        if not data:
            return
        cb.modify_article(None, item.id, data)

    # slots function
    def _new_article_sylva(self, index, data: NamedDict = None):
        self.append_item(0, data, index)

    def _remove_article_sylva(self, index):
        self.remove_item(index)

    def _new_folder_sylva(self, index, data: NamedDict = None):
        self.insert_item(1, data, index, offset=1)

    def _rename_folder_sylva(self, index, data: NamedDict = None):
        self.remove_item(index)
        self.insert_item(1, data, index, offset=0)

    def _delete_folder_sylva(self, index):
        assert(not self.item_level(index) == 1)
        self.remove_item(index)
