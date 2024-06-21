from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu, QAction

from mvc.model import NOTE_COLUMNS_WIDTH
from mvc.model import SearchProxyModel, PropItem, create_note_item
from mvc.base import BaseModule

from mvc import funcs

import utils.opn as opn
from utils.opn import to_profile

from archi import ProfileNote

class NoteModule(BaseModule):
    def __init__(self, parent):
        self.focus_id = None
        columns = list(NOTE_COLUMNS_WIDTH.keys())
        columns.remove('Article')
        super().__init__(parent, columns, NOTE_COLUMNS_WIDTH)

        self.set_slots()
        self.enable_context_menu()

    def add_item(self, note_id: int, data: ProfileNote):
        row = self.package_item(note_id, data = data)
        self.model.appendRow(row)

    def insert_item(self, note_id: int, data: ProfileNote, index):
        row = self.package_item(note_id, data = data)
        self.model.insertRow(index.row(), row)

    def package_item(self, note_id: int, data: ProfileNote):
        row = []
        if "Title" in self.columns:
            item: PropItem = create_note_item(note_id, data.title)
            row.append(item)
        if "Date" in self.columns:
            date_item = QStandardItem(data.date)
            row.append(date_item)
        if "" in self.columns:
            button_item = QStandardItem(QIcon(), " ")
            row.append(button_item)

        for i, item in enumerate(row):
            # if i == 0: TODO
            #     continue
            item.setEditable(False)
        return row
    
    def remove_item(self, index):
        return super().remove_item(index)
    
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
        index = self.tree_view.indexAt(point)
        index = index.siblingAtColumn(0)
        source_index = self.proxy_model.mapToSource(index)

        menu = QMenu(self.tree_view)

        new_note_action = QAction("New", self.tree_view)
        new_note_action.triggered.connect(lambda: self._new_note(source_index))
        menu.addAction(new_note_action)
        if index.isValid():
            modify_note_action = QAction("Modify", self.tree_view)
            delete_note_action = QAction("Delete", self.tree_view)
            modify_note_action.triggered.connect(lambda: self._modify_note(source_index))
            delete_note_action.triggered.connect(lambda: self._delete_note(source_index))
            menu.addActions([modify_note_action, delete_note_action])

        menu.exec_(self.tree_view.viewport().mapToGlobal(point))
    
    def set_slots(self):
        # disable the sort function TODO
        # self.tree_view.header().sectionClicked.connect(self._sort_by_column)
        self.tree_view.clicked.connect(self._row_selected)

    def _row_selected(self, index):
        source_index = self.proxy_model.mapToSource(index)
        print(f"Note Row selected: {source_index.row()}")

        source_index = source_index.siblingAtColumn(0)
        item = self.model.itemFromIndex(source_index) # TODO
        # outside function
        funcs.on_note_row_selected(self, item.note_id)
        # end

    def _new_note(self, index = None):
        # outside function
        note_id, data, flag = funcs.on_new_note(self, self.focus_id)
        # end
        if not flag:
            return
        data = to_profile(data)
        self.add_item(note_id, data)
    
    def _modify_note(self, index):
        index = index.siblingAtColumn(0)
        item: PropItem = self.model.itemFromIndex(index)
        # outside function
        note_id, data, flag = funcs.on_modify_note(self, item.note_id, self.focus_id)
        # end
        if not flag:
            return 
        data = to_profile(data)
        self.remove_item(index)
        self.insert_item(note_id, data, index)

    def _delete_note(self, index):
        index = index.siblingAtColumn(0)
        item: PropItem = self.model.itemFromIndex(index)
        # outside function
        flag = funcs.on_delete_note(self, item.note_id)
        # end
        if not flag:
            return
        self.remove_item(index)