import utils.opn as opn

from PySide6.QtWidgets import QDialog, QMessageBox, QInputDialog, QLineEdit
from PySide6.QtCore import Slot

from widget.emitter import emitter

from utils.opn import to_data
from sylva import Sylva, NoteData, FolderData

from typing import Tuple, Dict

import setting as stg

def sort_by_column(col_idx, order):
    pass

def row_selected(index, article_id):
    emitter.render_main_browser.emit(article_id)
    emitter.clear_note_viewer.emit()
    emitter.render_note_viewer.emit(article_id)

def row_focused_selected(index, article_id):
    emitter.open_pdf_internal.emit(article_id)

def row_selected_notem(index, note_id):
    emitter.render_note_editor.emit(note_id)

def on_row_delegate_clicked(index, var):
    pass

def new_article(index, article_id, data):
    article = opn.create_article(data, None)
    article = opn.add_article(article)
    if stg.ACTIVE_REFRESHING_VIEW:
        emitter.new_article.emit(None, to_data(article))
    return True

def modify_article(index, article_id, data):
    article = opn.get_article(article_id)
    opn.reset_article(data, article)
    if stg.ACTIVE_REFRESHING_VIEW:
        if index is not None:
            emitter.modify_article.emit(index, to_data(article))
        else:
            emitter.refresh_mvm.emit()
        emitter.refresh_nvm.emit()
        emitter.render_main_browser.emit(article_id)
    return True

def delete_article(index, article_id):
    opn.delete_article(article_id)
    opn.delete_folder_article_by_id(article_id)
    if stg.ACTIVE_REFRESHING_VIEW:
        emitter.delete_article.emit(index)
        emitter.refresh_nvm.emit()
        emitter.refresh_note_viewer.emit(article_id)
        emitter.render_main_browser.emit(article_id)
        emitter.render_note_editor.emit(None)
    return True
    
def new_article_sylva(index, sylva_id, article_id):
    print(index, sylva_id, article_id)
    opn.add_folder_article(sylva_id, article_id)

    if stg.ACTIVE_REFRESHING_VIEW:
        article = opn.get_article(article_id)
        emitter.new_article_sylva.emit(index, to_data(article))
    return True

def remove_article_sylva(index, sylva_id, idx2):
    opn.delete_folder_article(sylva_id, idx2)
    if stg.ACTIVE_REFRESHING_VIEW:
        emitter.remove_article_sylva.emit(index)
    return True

def new_folder_sylva(index, text, idx1):
    text = text if text else "New Folder"
    item = opn.add_folder(idx1 + 1, text)
    if stg.ACTIVE_REFRESHING_VIEW:
        data = FolderData(item["id"], item["name"])
        emitter.new_folder_sylva.emit(index, data)
    return True

def rename_folder_sylva(index, sylva_id, text):
    opn.rename_folder(sylva_id, text)
    if stg.ACTIVE_REFRESHING_VIEW:
        data = FolderData(sylva_id, text)
        emitter.rename_folder_sylva.emit(index, data)
    return True

def delete_folder_sylva(index, sylva_id):
    opn.delete_folder(sylva_id)
    if stg.ACTIVE_REFRESHING_VIEW:
        emitter.delete_folder_sylva.emit(index)
    return True

def new_note_passive(index, article_id):
    time = opn.get_time()
    data = NoteData(add_time = time, changed_time = time)
    note = opn.create_note(data)
    note = opn.add_note(note, opn.get_article(article_id))

    emitter.new_note.emit(index, to_data(note))
    emitter.render_note_editor.emit(note.id)
    return note.id, data, True

def on_new_note(clf, article_id): # TODO solve html problem
    return -1, None, False
    dialog = LNoteDialog(clf.parent(), 'Add New Note')
    if dialog.exec_() == QDialog.Rejected:
        return -1, None, False
    data = dialog.get_data()
    note = opn.create_note(data)
    opn.add_note(note, opn.get_article(article_id))
    return note.id, data, True

def on_modify_note(clf, note_id, article_id): # TODO solve html problem
    return -1, None, False
    note = opn.get_note(note_id)
    note_data = opn.to_data(note)
    dialog = LNoteDialog(clf.parent(), 'Modify Note')
    dialog.set_data(note_data)
    if dialog.exec_() == QDialog.Rejected:
        return -1, None, False
    data = dialog.get_data()
    opn.reset_note(data, note)
    return note.id, data, True

def delete_note(index, note_id):
    opn.delete_note(note_id)
    if stg.ACTIVE_REFRESHING_VIEW:
        emitter.delete_note.emit(index)
        emitter.render_note_editor.emit(note_id)
    return True