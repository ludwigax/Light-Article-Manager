from PySide6.QtCore import Signal, QObject, QUrl
from sylva import NamedDict


class Emitter(QObject):
    render_main_viewer = Signal()
    clear_main_viewer = Signal()
    refresh_mvm = Signal()
    refresh_nvm = Signal()

    render_note_viewer = Signal(int)
    refresh_note_viewer = Signal(int)
    clear_note_viewer = Signal()

    render_main_browser = Signal(int)
    clear_main_browser = Signal()

    render_note_editor = Signal(int)
    clear_note_editor = Signal()

    open_pdf_internal = Signal()
    change_editor_mode = Signal(int)
    import_internet = Signal(object)

    new_article = Signal(object, NamedDict)
    modify_article = Signal(object, NamedDict)
    delete_article = Signal(object)

    new_article_sylva = Signal(object, NamedDict)
    remove_article_sylva = Signal(object)
    new_folder_sylva = Signal(object, NamedDict)
    rename_folder_sylva = Signal(object, NamedDict)
    delete_folder_sylva = Signal(object)

    new_note = Signal(object, NamedDict)
    delete_note = Signal(object)

emitter = Emitter()

