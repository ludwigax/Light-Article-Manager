from PyQt5.QtCore import QSortFilterProxyModel, Qt, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtWidgets import QTreeView, QHeaderView

from mvc.model import (SearchProxyModel, BinestedItem, create_article_item, create_folder_item)
from mvc.model import COLUMNS_WIDTH

from archi import ProfileData

class BaseModule:
    def __init__(self, parent, columns=None):
        self._parent = parent

        if columns is None:
            self.columns = list(COLUMNS_WIDTH.keys())
        else:
            self.columns = [col for col in columns if col in COLUMNS_WIDTH.keys()]

        self.model = QStandardItemModel(parent)
        self.model.setHorizontalHeaderLabels(self.columns)
        self.proxy_model = SearchProxyModel(parent)
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setSortCaseSensitivity(Qt.CaseInsensitive)

        self.tree_view = QTreeView(parent)
        self.tree_view.setModel(self.proxy_model)

        for i, col in enumerate(self.columns):
            self.tree_view.setColumnWidth(i, COLUMNS_WIDTH[col])

        self.tree_view.setEditTriggers(QTreeView.NoEditTriggers)
        self.tree_view.setSelectionMode(QTreeView.ExtendedSelection)

        self.tree_view.header().setSectionsClickable(True)
        self.tree_view.header().setSortIndicatorShown(True)
        self.tree_view.header().setSectionResizeMode(QHeaderView.Fixed)

        self.tree_view.header().setSortIndicator(-1, Qt.AscendingOrder)
        self.set_nested(False)
        self._menu = False
        
    def parent(self):
        return self._parent
    
    @property
    def nested(self):
        return self._nested
    
    @property
    def menu(self):
        return self._menu
    
    def set_nested(self, flag: bool = False):
        self._nested = flag
        self.tree_view.setRootIsDecorated(flag)
    
    def add_item(self, article_id: int, data: ProfileData):
        row = self.package_item(article_id, data = data)
        self.model.appendRow(row)

    def insert_item(self, article_id: int, data: ProfileData, index):
        row = self.package_item(article_id, data = data)
        self.model.insertRow(index.row(), row)

    def package_item(self, article_id: int, is_nested: bool = False, is_folder: bool = None, data: ProfileData = None):
        assert(not is_nested or is_folder is not None)
        row = []
        if is_nested:
            if is_folder:
                item = create_folder_item(data.title)
            else:
                item = create_article_item(article_id, data.title)
        else:
            item = create_article_item(article_id, data.title)
        if "Title" in self.columns:
            row.append(item)
        if "Year" in self.columns:
            year_item = QStandardItem(data.year)
            row.append(year_item)
        if "Journal" in self.columns:
            journal_item = QStandardItem(data.journal)
            row.append(journal_item)
        if "Author" in self.columns:
            author_item = QStandardItem(data.author)
            row.append(author_item)
        if "Add Time" in self.columns:
            add_time_item = QStandardItem(data.add_time)
            row.append(add_time_item)
        if "Rank" in self.columns:
            rank_item = QStandardItem()
            rank_item.setData(data.rank, Qt.DisplayRole)
            row.append(rank_item)
        if "" in self.columns:
            button_item = QStandardItem(QIcon('../ui/src/plus.png'), "")
            row.append(button_item)
        
        for item in row:
            item.setEditable(False)
        return row

    def remove_item(self, index):
        self.model.removeRow(index.row())

    def search_proxy_mdoel(self, text: str, col_idx: int = 0):
        # type_list = []
        indices = {}
        if self.proxy_model.external_indices:
            self.proxy_model.resetOrder()

        row_count = self.proxy_model.rowCount()
        for row in range(row_count):
            proxy_index = self.proxy_model.index(row, col_idx)
            
            data = self.proxy_model.data(proxy_index, role=Qt.DisplayRole)
            if data is None:
                continue
            # data_type = type(data) # TODO demo
            data = data.lower()

            if text.lower() not in data:
                continue
            source_index = self.proxy_model.mapToSource(proxy_index)
            if source_index.parent() == QModelIndex():
                key = -1
            else:
                key = source_index.parent().row()
            indices.setdefault(key, []).append(source_index.row())
        self.proxy_model.setExternalOrder(indices)
        return col_idx, self.proxy_model.sort_order

    def sort_proxy_model(self, col_idx: int):
        if self.proxy_model.sort_indicator_column == col_idx:
            self.proxy_model.sort_order = Qt.DescendingOrder if self.proxy_model.sort_order == Qt.AscendingOrder else Qt.AscendingOrder
        else:
            self.proxy_model.sort_order = Qt.AscendingOrder

        self.proxy_model.sort_indicator_column = col_idx
        if self.proxy_model.external_indices:
            self.proxy_model.resetOrder()
        self.proxy_model.sort(col_idx, self.proxy_model.sort_order)
        return col_idx, self.proxy_model.sort_order
    
    def enable_context_menu(self):
        raise NotImplementedError("Method not allowed")

    def disable_context_menu(self):
        raise NotImplementedError("Method not allowed")
    
    def context_menu(self, point):
        raise NotImplementedError("Method not allowed")

    def set_delegate(self, col_idx: int, delegate: object):
        raise NotImplementedError("Method not allowed")
    
    def set_slots(self):
        self.tree_view.header().sectionClicked.connect(self._sort_by_column)
        # self.tree_view.header().sectionDoubleClicked.connect(self._sort_by_column) # TODO disable this function

    # slots function
    def _sort_by_column(self, col_idx: int):
        col_idx, sort_order = self.sort_proxy_model(col_idx)