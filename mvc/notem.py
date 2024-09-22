from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon, QAction
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMenu

from mvc.model import NOTE_COLUMNS_WIDTH
from mvc.model import SearchProxyModel, BinestedItem, create_item
from mvc.base import BaseModule

import utils.opn as opn
import utils.combo as cb

from widget.dialog import delete_note_dialog
from widget.emitter import emitter

from sylva import NamedDict

class NoteModule(BaseModule):
    def __init__(self, parent):
        self.focus_id = None
        columns = list(NOTE_COLUMNS_WIDTH.keys())
        columns.remove('Article')
        super().__init__(parent, columns, NOTE_COLUMNS_WIDTH)

        self.set_slots()
        self.enable_context_menu()

    def append_item(self, data: NamedDict):
        row = self.package_item(data = data)
        self.model.appendRow(row)

    def insert_item(self, data: NamedDict, index):
        row = self.package_item(data = data)
        self.model.insertRow(index.row(), row)

    def package_item(self, data: NamedDict):
        row = []
        if "Title" in self.columns:
            item: BinestedItem = create_item(2, data.id, data.title)
            row.append(item)
        if "Modified Time" in self.columns:
            date_item = QStandardItem(data.changed_time)
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
        if not self.focus_id:
            return
        index = self.tree_view.indexAt(point)
        index = index.siblingAtColumn(0)
        source_index = self.proxy_model.mapToSource(index)

        menu = QMenu(self.tree_view)

        new_note_action = QAction("New", self.tree_view)
        new_note_action.triggered.connect(lambda: self.menu_new_note(source_index))
        new_note_passive_action = QAction("New Passive", self.tree_view)
        new_note_passive_action.triggered.connect(lambda: self.menu_new_note_passive(source_index))
        menu.addActions([new_note_passive_action, new_note_action])
        if index.isValid():
            modify_note_action = QAction("Modify", self.tree_view)
            delete_note_action = QAction("Delete", self.tree_view)
            modify_note_action.triggered.connect(lambda: self.menu_modify_note(source_index))
            delete_note_action.triggered.connect(lambda: self.menu_delete_note(source_index))
            menu.addActions([modify_note_action, delete_note_action])

        menu.exec_(self.tree_view.viewport().mapToGlobal(point))
    
    def set_slots(self):
        # disable the sort function TODO
        # self.tree_view.header().sectionClicked.connect(self._sort_by_column)
        self.tree_view.clicked.connect(self._row_selected)
        emitter.new_note.connect(self._new_note)
        emitter.delete_note.connect(self._delete_note)

    def _row_selected(self, index):
        source_index = self.proxy_model.mapToSource(index)
        print(f"Note Row selected: {source_index.row()}")

        source_index = source_index.siblingAtColumn(0)
        item = self.model.itemFromIndex(source_index) # TODO
        # outside function
        cb.row_selected_notem(source_index, item.id)
        # end

    # menu functions
    def menu_new_note(self, index): # TODO
        pass

    def menu_modify_note(self, index):
        pass

    def menu_new_note_passive(self, index):
        cb.new_note_passive(index, self.focus_id)

    def menu_delete_note(self, index):
        item = self.model.itemFromIndex(index)
        if delete_note_dialog(self.parent()):
            cb.delete_note(index, item.id)

    # slots functions
    def _new_note(self, index, data = None):
        self.append_item(data)

    def _delete_note(self, index):
        self.remove_item(index)
    
    # def _modify_note(self, index):
    #     index = index.siblingAtColumn(0)
    #     item: PropItem = self.model.itemFromIndex(index)
    #     # outside function
    #     note_id, data, flag = funcs.on_modify_note(self, item.note_id, self.focus_id)
    #     # end
    #     if not flag:
    #         return 

    #     self.remove_item(index)
    #     self.insert_item(note_id, data, index)