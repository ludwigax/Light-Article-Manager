import utils.opn as opn

from PySide6.QtWidgets import QDialog, QMessageBox, QInputDialog, QLineEdit
from widget.dialog import LArticleDialog, LGroupDialog, CheckStateDialog, \
    LNoteDialog

from utils.opn import to_data
from sylva import Sylva, NoteData

def on_sort_by_column(clf, col_idx, order):
    pass

def on_row_selected(clf, article_id):
    clf.tree_view.window().render_signal.emit(article_id)

def on_row_focused_selected(clf, article_id):
    clf.tree_view.window().open_pdf_signal.emit(article_id)

def on_note_row_selected(clf, note_id):
    clf.tree_view.window().render_note_signal.emit(note_id)

def on_row_delegate_clicked(index):
    pass

def on_new_article(clf):
    dialog = LArticleDialog(clf.parent(), 'Add New Article')
    if dialog.exec_() == QDialog.Rejected:
        return -1, None, False
    data = dialog.get_data()
    article = opn.create_article(data, None)
    opn.add_article(article)
    return article.id, data, True

def on_modify_article(clf, article_id):
    article = opn.get_article(article_id)
    article_data = opn.to_data(article)
    dialog = LArticleDialog(clf.parent(), 'Modify Article')
    dialog.set_data(article_data)
    if dialog.exec_() == QDialog.Rejected:
        return -1, None, False
    data = dialog.get_data()
    opn.reset_article(data, article)
    return article.id, data, True

def on_delete_article(clf, article_id):
    if QMessageBox.question(clf.parent(), 'Delete', 'Ensure the deletion',
                            QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
        opn.delete_article(article_id)
        return True
    else:
        return False
    
def on_new_article_sylva(clf, title, idx1):
    # diag = LGroupDialog(clf.parent(), 'Add article to folder')
    # articles = opn.get_all_articles()
    # for article in articles:
    #     widget = LCheckItem(article.id, article.title)
    #     diag.add_item(widget)
    # if diag.exec_() == QDialog.Rejected:
    #     return None, None, False
    # archi = Archi()
    # archi.load()
    # id_list = list(diag.get_data())
    # datas = []
    # for id in id_list:
    #     datas.append(to_profile(to_data(opn.get_article(id))))
    #     opn.add_folder_article(archi, title, idx1, id)
    # archi.save()
    # return id_list, datas, True
    diag = CheckStateDialog(clf.parent(), 'Add article to folder')
    if diag.exec_() == QDialog.Rejected:
        return None, None, False
    archi = Sylva()
    archi.load()
    id_list = list(diag.get_data())
    datas = []
    for id in id_list:
        datas.append(to_data(opn.get_article(id)))
        opn.add_folder_article(archi, title, idx1, id)
    archi.save()
    return id_list, datas, True

def on_remove_article_sylva(clf, title, idx1, idx2):
    archi = Sylva()
    archi.load()
    opn.delete_folder_article(archi, title, idx1, idx2)
    archi.save()

def on_new_folder_sylva(clf, title, idx1):
    archi = Sylva()
    archi.load()
    title = opn.add_folder(archi, title, idx1)
    archi.save()
    return title

def on_rename_folder_sylva(clf, title, idx1):
    archi = Sylva()
    archi.load()
    new_title, ok_pressed = QInputDialog.getText(None, "Input", "Changed Name:", QLineEdit.Normal, "")
    if not ok_pressed:
        return new_title, False
    opn.rename_folder(archi, title, idx1, new_title)
    archi.save()
    return new_title, True

def on_delete_folder_sylva(clf, title, idx1):
    archi = Sylva()
    archi.load()
    opn.delete_folder(archi, title, idx1)
    archi.save()

def on_new_note_passive(clf, article_id):
    time = opn.get_time()
    data = NoteData(add_time = time, changed_time = time)
    note = opn.create_note(data)
    opn.add_note(note, opn.get_article(article_id))

    clf.tree_view.window().render_note_signal.emit(note.id)
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

def on_delete_note(clf, note_id, article_id = None):
    if QMessageBox.question(clf.parent(), 'Delete', 'Ensure the deletion',
                            QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
        opn.delete_note(note_id)
        clf.tree_view.window().delete_note_signal.emit(note_id)
        return True
    else:
        return False