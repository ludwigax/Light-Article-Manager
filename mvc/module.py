from PyQt5.QtCore import QSortFilterProxyModel, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtWidgets import QTreeView, QHeaderView, QMenu, QAction

from mvc.model import (SearchProxyModel, BinestedItem,
    create_article_item, create_folder_item)
from mvc.model import COLUMNS_WIDTH
from mvc.base import BaseModule
import mvc.funcs as funcs

from archi import ProfileData
from utils.opn import to_data, to_profile

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

    # slots function
    def _sort_by_column(self, col_idx: int):
        print(f"Header clicked: {self.model.headerData(col_idx, Qt.Horizontal)} (Index: {col_idx})")

        col_idx, sort_order = self.sort_proxy_model(col_idx)
        # outside function
        funcs.on_sort_by_column(self, col_idx, sort_order)
        # end

    def _row_selected(self, index):
        source_index = self.proxy_model.mapToSource(index)
        print(f"Row selected: {source_index.row()}")

        source_index = source_index.siblingAtColumn(0)
        item = self.model.itemFromIndex(source_index)
        if isinstance(item, BinestedItem) and item.is_folder:
            return
        # outside function
        funcs.on_row_selected(self, item.article_id)
        # end

class NonNestedModule(ModelViewModule):
    def __init__(self, parent, columns=None):
        super().__init__(parent, columns)
        self.enable_context_menu()

    def context_menu(self, point):
        index = self.tree_view.indexAt(point)
        index = index.siblingAtColumn(0)
        source_index = self.proxy_model.mapToSource(index)

        menu = QMenu(self.tree_view)
        action_list = []

        sort_action = QAction("Sort", self.tree_view)
        menu.addAction(sort_action)
        menu.addSeparator()

        new_article_action = QAction("New", self.tree_view)
        sort_action.triggered.connect(self._sort_by_menu)
        new_article_action.triggered.connect(lambda: self._new_article(source_index))
        menu.addAction(new_article_action)

        if index.isValid():
            modify_article_action = QAction("Modify", self.tree_view)
            delete_article_action = QAction("Delete", self.tree_view)
            modify_article_action.triggered.connect(lambda: self._modify_article(source_index))
            delete_article_action.triggered.connect(lambda: self._delete_article(source_index))
            menu.addActions([modify_article_action, delete_article_action])

        menu.exec_(self.tree_view.viewport().mapToGlobal(point))

    def _sort_by_menu(self):
        col_idx, sort_order = self.sort_proxy_model(0)
        self.tree_view.header().setSortIndicator(0, Qt.AscendingOrder)
        self.proxy_model.sort_order = Qt.AscendingOrder

    def _new_article(self, index = None):
        # outside function
        article_id, data, flag = funcs.on_new_article(self)
        # end
        if not flag:
            return
        data = to_profile(data)
        self.add_item(article_id, data)

    def _modify_article(self, index):
        index = index.siblingAtColumn(0)
        item: BinestedItem = self.model.itemFromIndex(index)
        # outside function
        article_id, data, flag = funcs.on_modify_article(self, item.article_id)
        # end
        if not flag:
            return
        data = to_profile(data)
        self.remove_item(index)
        self.insert_item(article_id, data, index)

    def _delete_article(self, index):
        index = index.siblingAtColumn(0)
        item: BinestedItem = self.model.itemFromIndex(index)
        # outside function
        flag = funcs.on_delete_article(self, item.article_id)
        # end
        if not flag:
            return
        self.remove_item(index)

class NestedModule(ModelViewModule):
    def __init__(self, parent, columns=None):
        super().__init__(parent, columns)
        self.set_nested(True)
        self.enable_context_menu()

    def add_item(self, article_id: int, is_folder: bool, data: ProfileData, item: BinestedItem = None): # folder_idx: 0, -1
        if not is_folder and item is None:
            raise AttributeError("Article cannot add to ROOT!")
        row = self.package_item(article_id, True, is_folder, data)
        if not item:
            self.model.appendRow(row)
            return row[0]
        else:
            item.appendRow(row)
    
    def insert_item(self, article_id: int, is_folder: bool, data: ProfileData, index, offset = 0):
        if self.item_level(index) == 1:
            index = index.parent()
        item = self.package_item(article_id, True, is_folder, data)
        if is_folder:
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
    
    def context_menu(self, point):
        index = self.tree_view.indexAt(point)
        index = index.siblingAtColumn(0)
        source_index = self.proxy_model.mapToSource(index)
        item: BinestedItem = self.model.itemFromIndex(source_index)

        menu = QMenu(self.tree_view)

        sort_action = QAction("Sort", self.tree_view)
        sort_action.triggered.connect(self._sort_by_menu)
        menu.addAction(sort_action)
        menu.addSeparator()

        if index.isValid():
            new_article_action = QAction("New Article", self.tree_view)
            new_article_action.triggered.connect(lambda: self._new_article_archi(source_index))
            menu.addAction(new_article_action)

            if not item.is_folder:
                remove_article_action = QAction("Remove Article", self.tree_view)
                remove_article_action.triggered.connect(lambda: self._remove_article_archi(source_index))
                menu.addAction(remove_article_action)
            menu.addSeparator()

        new_folder_action = QAction("New Folder", self.tree_view)
        new_folder_action.triggered.connect(lambda: self._new_folder_archi(source_index))
        menu.addAction(new_folder_action)

        if index.isValid() and item.is_folder:
            rename_folder_action = QAction("Rename Folder", self.tree_view)
            delete_folder_action = QAction("Delete Folder", self.tree_view)
            rename_folder_action.triggered.connect(lambda: self._rename_folder_archi(source_index))
            delete_folder_action.triggered.connect(lambda: self._delete_folder_archi(source_index))
            menu.addActions([rename_folder_action, delete_folder_action])

        menu.exec_(self.tree_view.viewport().mapToGlobal(point))

    def _sort_by_menu(self):
        col_idx, sort_order = self.sort_proxy_model(0)
        self.tree_view.header().setSortIndicator(0, Qt.AscendingOrder)
        self.proxy_model.sort_order = Qt.AscendingOrder

    def _new_article_archi(self, index):
        index = index.siblingAtColumn(0)
        if self.item_level(index) == 1:
            index = index.parent()
        item = self.model.itemFromIndex(index)
        title = item.text()
        # outside function
        id_list, datas, flag = funcs.on_new_article_archi(self, title, -1)
        if not flag:
            return
        # end
        for article_id, data in zip(id_list, datas):
            self.add_item(article_id, 0, data, item)

    def _remove_article_archi(self, index):
        index = index.siblingAtColumn(0)
        item: BinestedItem = self.model.itemFromIndex(index)
        assert(not item.is_folder)
        
        idx2 = item.row()
        idx1 = item.parent().row()
        title = item.parent().text()
        # outside function
        funcs.on_remove_article_archi(self, title, idx1, idx2)
        # end
        self.remove_item(index) 

    def _new_folder_archi(self, index):
        index = index.siblingAtColumn(0)
        if index.isValid():
            if self.item_level(index) == 1:
                index = index.parent()
            row_idx = index.row()
        else:
            row_idx = self.model.rowCount() - 1
        # outside function
        folder_name = funcs.on_new_folder_archi(self, "New Folder", row_idx + 1)
        # end
        item = self.package_item(-1, True, True, ProfileData(folder_name, "", "", "", "", ""))
        self.model.insertRow(row_idx + 1, item)

    def _rename_folder_archi(self, index):
        index = index.siblingAtColumn(0)
        item: BinestedItem = self.model.itemFromIndex(index)
        title = item.text()
        idx1 = item.row()
        # outside function
        folder_name, flag = funcs.on_rename_folder_archi(self, title, idx1)
        if not flag:
            return
        # end
        self.remove_item(index)
        self.insert_item(-1, True, ProfileData(folder_name, "", "", "", "", ""), index, offset=0)

    def _delete_folder_archi(self, index):
        index = index.siblingAtColumn(0)
        item: BinestedItem = self.model.itemFromIndex(index)
        idx1 = item.row()
        title = item.text()
        # outside function
        funcs.on_delete_folder_archi(self, title, idx1)
        # end
        self.remove_item(index)