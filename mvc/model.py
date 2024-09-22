from PySide6.QtCore import QSortFilterProxyModel, Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon

import ui.res_rc # TODO

class SearchProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(SearchProxyModel, self).__init__(parent)
        self.external_indices = {}
        self.sort_order = Qt.AscendingOrder
        self.sort_indicator_column = -1

    def setExternalOrder(self, indices: dict):
        self.external_indices = indices
        self.sort_indicator_column = -1
        self.invalidate()
        self.sort(0, Qt.AscendingOrder)

    def resetOrder(self):
        self.external_indices = {}
        self.invalidateFilter()
        self.sort(-1)

    def filterAcceptsRow(self, source_row, source_parent):
        if not self.external_indices:
            return True
        if source_parent.isValid():
            return source_row in self.external_indices.get(source_parent.row(), [])
        else:
            return source_row in self.external_indices[-1]

    def lessThan(self, left, right): # TOCHANGE
        if self.external_indices:
            assert(left.parent().row() == right.parent().row())
            left_row = left.row()
            right_row = right.row()
            key = left.parent().row()
            return self.external_indices.get(key, []).index(left_row) < self.external_indices.get(key, []).index(right_row)
        return super(SearchProxyModel, self).lessThan(left, right)

class PropItem(QStandardItem):
    def __init__(self, keys = [], values = [], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._prop_dict = dict(zip(keys, values))

    def __getattr__(self, key):
        if key == '_prop_dict':
            return getattr(self, '_prop_dict')
        if key in self.__dict__.get('_prop_dict', {}):
            return self._prop_dict[key]
        else:
            raise AttributeError(f"'PropItem' object has no attribute '{key}'")
        
    def __setattr__(self, key, value):
        if key == '_prop_dict':
            super().__setattr__(key, value)
        elif key in self.__dict__.get('_prop_dict', {}):
            self._prop_dict[key] = value
        else:
            super().__setattr__(key, value)

class BinestedItem(PropItem):
    r"""
    `item_type`: 1 - folder, 0 - article, 2 - note
    """
    def __init__(self, item_type, id, *args, **kwargs):
        keys = ['item_type', 'id']
        values = [item_type, id]
        super().__init__(keys, values, *args, **kwargs)

def create_item(type, id, text) -> BinestedItem | PropItem:
    if type == 1:
        icon = QIcon(":icons/open-folder.png")
    elif type == 0:
        icon = QIcon(":icons/google-docs.png")
    elif type == 2:
        icon = QIcon(":icons/post-it.png")
    else:
        raise ValueError(f"Invalid type: {type}")
    
    return BinestedItem(type, id, icon, text)


COLUMNS_WIDTH = {
    'Title': 300,
    'Year': 40,
    'Journal': 150,
    'Author': 90,
    'Add Time': 90,
    'Rank': 50,
    '': 24
}

NOTE_COLUMNS_WIDTH = {
    'Title': 240,
    'Modified Time': 95,
    'Article': 240,
    '': 24
}