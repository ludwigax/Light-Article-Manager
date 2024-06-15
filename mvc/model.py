from PyQt5.QtCore import QSortFilterProxyModel, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon

import ui.res_rc # TODO

class SearchProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(SearchProxyModel, self).__init__(parent)
        self.external_indices = []
        self.sort_order = Qt.AscendingOrder
        self.sort_indicator_column = -1

    def setExternalOrder(self, indices):
        self.external_indices = indices
        self.sort_indicator_column = -1
        self.invalidate()
        self.sort(0, Qt.AscendingOrder)

    def resetOrder(self):
        self.external_indices = []
        self.invalidateFilter()
        self.sort(-1)

    def filterAcceptsRow(self, source_row, source_parent):
        return not self.external_indices or source_row in self.external_indices

    def lessThan(self, left, right):
        if self.external_indices:
            left_row = left.row()
            right_row = right.row()
            return self.external_indices.index(left_row) < self.external_indices.index(right_row)
        return super(SearchProxyModel, self).lessThan(left, right)
    
class BinestedItem(QStandardItem):
    def __init__(self, is_folder, article_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_folder = is_folder
        self.article_id = article_id

def create_folder_item(text) -> BinestedItem:
    icon = QIcon(":icons/open-folder.png")
    item = BinestedItem(True, -1, icon, text)
    return item

def create_article_item(article_id, text) -> BinestedItem:
    icon = QIcon(":icons/google-docs.png")
    item = BinestedItem(False, article_id, icon, text)
    return item

COLUMNS_WIDTH = {
    'Title': 300,
    'Year': 40,
    'Journal': 150,
    'Author': 90,
    'Add Time': 90,
    'Rank': 50,
    '': 24
}