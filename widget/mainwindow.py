import os
import sys
from typing import List, Tuple

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog,\
    QMessageBox, QDialog, QTextBrowser, QListWidget, QTextEdit, QTreeWidgetItem, QInputDialog
from PyQt5.QtCore import Qt, pyqtSignal

from PyQt5.QtWidgets import QTabWidget, QVBoxLayout

from ui import Ui_MainWindow
from widget.dialog import LArticleDialog, LKeywordDialog, LNoteDialog, LGroupDialog
from widget.widget import LSearchItem, LNoteItem, LAddItem, LArticleItem, LFolderItem, LCheckItem, \
    LFolderAddItem
import widget.action as act
from crawler import DownloadWorker

from database import Article, Keyword, Note
import database
from archi import ArticleData, NoteData, AnnotationData
import utils
import utils.format as fmt
import utils.opn as opn
from utils.opn import to_data, to_profile

from mvc.module import NestedModule, NonNestedModule

from tools import extract_annotations, extract_bib_info

import markdown2
import datetime

from func import global_session

class LMainWindow(QMainWindow, Ui_MainWindow):
    render_signal = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Ludwig Article Manager")
        self.focus_id = None
        self.download_id = None
        self.log = []

        self.btn_search.clicked.connect(self.onSearchClicked)
        self.btn_clear.clicked.connect(self.onClearClicked)
        self.btn_import.clicked.connect(self.onImportClicked)
        self.btn_importb.clicked.connect(self.onImportBatchClicked)
        self.btn_addman.clicked.connect(self.onManualClicked)
        self.btn_add_key.clicked.connect(self.onAddKeywordClicked)
        self.btn_add_note.clicked.connect(self.onAddNoteClicked)
        self.btn_mdf.clicked.connect(self.onModifyClicked)
        self.btn_download.clicked.connect(self.onDownloadClicked)
        self.btn_sync.clicked.connect(self.onNoteSynchronousClicked)
        # self.btn_sync_r.clicked.connect(self.onNoteSynchronousClicked)

        def temp_anchor_fcn(path):
            if act.openAritcleFile(path):
                self.showArticleMain(self.focus_id)
        self.browser_main.anchorClicked.connect(temp_anchor_fcn)


        self.browser_info.setHook(mouseDoubleClick_hook=self.onArticleModifierDoubleClicked, mouseDoubleClick_state=True)
        self.browser_kwd.setHook(mouseDoubleClick_hook=self.onKeywordsModifierDoubleClicked, mouseDoubleClick_state=True)
        def onSearchKey(widget: QWidget, params):
            e = params[0]
            if e.key() == Qt.Key_Return:
                self.onSearchClicked()
                return 1
            else:
                return 0
        self.textedit_search.setHook(keyPress_hook=onSearchKey, keyPress_state=None)

        # render a permanent item as a button TODO
        # widget = LAddItem()
        # act.addListWidgetItem(widget, self.list_notes)

        # render the tree view # TODO 
        # self.renderTree("ROOT")
        # self.renderAllArticlesList()
        # self.syncState(False)
        self.tabWidget.setEnabled(False)

        # temp 2nd window
        secondary_window = QDialog(self)
        secondary_window.setWindowTitle("Secondary")
        secondary_window.setGeometry(100, 300, 800, 500)
        
        # Create a QTabWidget
        tab_widget = QTabWidget()
        
        # Create two tabs
        tab1 = QWidget()
        tab2 = QWidget()
        
        articles = opn.get_all_articles()

        self.mvm = NonNestedModule(self, columns=None)
        self.nvm = NestedModule(self, columns=None)

        self.render_signal.connect(self.showArticleMain)

        for article in articles:
            self.mvm.add_item(article.id, to_profile(to_data(article)))

        from archi import Archi, ProfileData
        archi = Archi()
        archi.load()
        for kv in archi.data:
            item = self.nvm.add_item(-1, True, ProfileData(kv['name'], '', '', '', '', ''))
            for idx in kv['data']:
                article = opn.get_article(idx)
                self.nvm.add_item(idx, False, to_profile(to_data(article)), item)

        # Set layout for the first tab and add self.mvm
        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(self.mvm.tree_view)
        tab1.setLayout(tab1_layout)
        
        # Set layout for the second tab and add self.nvm
        tab2_layout = QVBoxLayout()
        tab2_layout.addWidget(self.nvm.tree_view)
        tab2.setLayout(tab2_layout)
        
        # Add tabs to the QTabWidget
        tab_widget.addTab(tab1, "Tab 1")
        tab_widget.addTab(tab2, "Tab 2")
        
        # Set the QTabWidget as the layout for the dialog
        layout = QVBoxLayout()
        layout.addWidget(tab_widget)
        secondary_window.setLayout(layout)
        
        secondary_window.setModal(False)  # Non-blocking
        secondary_window.show()

        # third window
        from PyQt5.QtWidgets import QToolBar, QAction
        third_window = QDialog(self)
        third_window.setWindowTitle("Third")
        third_window.setGeometry(1100, 150, 800, 800)
        
        toolbar = QToolBar("Toolbar", third_window)
        test_action = QAction("Test", third_window)
        test_action.triggered.connect(self.temp_add_note)
        toolbar.addAction(test_action)
        
        # 创建 QTextBrowser
        self.docking_browser = QTextBrowser(third_window)
        
        layout2 = QVBoxLayout(third_window)
        layout2.addWidget(toolbar)
        layout2.addWidget(self.docking_browser)

        third_window.setLayout(layout2)
        third_window.setModal(False)
        third_window.show()

    def temp_add_note(self):
        if not self.focus_id:
            self.print(fmt.RED_BOLD("No valid article selected"))
            return
        text, ok = QInputDialog.getText(self, 'Add Notes', "Enter: ")
        if ok:
            note = NoteData(
                note=text,
                date=datetime.datetime.now().strftime("%Y-%m-%d")
            )
            note = opn.create_note(note)
            opn.add_note(note, opn.get_article(self.focus_id))

    # --------------------------------------------------------------------------------
    # mainwindow GUI functions
    # browser
    def setFocusArticle(self, article_id: int = None):
        self.focus_id = article_id

    def renderBrowser(self, content, browser_name: str = "main"):
        # content = markdown2.markdown(content)
        if browser_name == "main":
            # self.browser_main.setHtml(content) # disable old
            self.docking_browser.setHtml(content) # new feature
        elif browser_name == "info":
            self.browser_info.setHtml(content)
        elif browser_name == "kwd":
            self.browser_kwd.setHtml(content)

    def clearBrowser(self, browser_name: str = "main"):
        if browser_name == "main":
            self.browser_main.clear()
        elif browser_name == "info":
            self.browser_info.clear()
        elif browser_name == "kwd":
            self.browser_kwd.clear()

    def refreshBrowser(self, content, browser_name: str = "main"):
        self.clearBrowser(browser_name)
        if content:
            self.renderBrowser(content, browser_name)

    # lists
    def renderList(self, content_list: List[Tuple[str, int]], list_name: str = "searchs"):
        if list_name == "searchs":
            act.setListWidget(LArticleItem, self.list_searchs, content_list)
        elif list_name == "notes":
            act.setListWidget(LNoteItem, self.list_notes, content_list)

    def clearList(self, list_name: str = "searchs"):
        if list_name == "searchs":
            act.clearListWidget(self.list_searchs)
        elif list_name == "articles":
            act.clearListWidget(self.list_articles)
        elif list_name == "notes":
            act.clearListWidget(self.list_notes, 1)

    def removeListItem(self, widget: QWidget, list_name: str = "searchs"):
        if list_name == "searchs":
            act.removeListWidgetItem(widget, self.list_searchs)
        if list_name == "articles":
            act.removeListWidgetItem(widget, self.list_articles)
        elif list_name == "notes":
            act.removeListWidgetItem(widget, self.list_notes)

    # trees # TODO
    def renderTree(self, root_name = "ROOT"):
        raise Exception("For Debugging")
        root_node = opn.get_root_node(global_session(), root_name)
        if not root_node:
            return
        
        act.clearTreeWidget(self.tree_root)
        def add_tree_item(node, parent_item: QTreeWidgetItem):
            if node.node_type == "folder":
                widget = LFolderItem(node.node_id, node.node_name)
                item = act.addTreeWidgetItem(widget, parent_item, self.tree_root)
                for child in node.children:
                    add_tree_item(child, item)
            elif node.node_type == "article":
                article = opn.get_article(global_session(), node.article_id)
                widget = LArticleItem(article.id, article.title, node_id=node.node_id)
                act.addTreeWidgetItem(widget, parent_item, self.tree_root)

        for child in root_node.children:
            add_tree_item(child, self.tree_root)
        btn_widget = LFolderAddItem()
        act.addTreeWidgetItem(btn_widget, self.tree_root, self.tree_root)

    def renderAllArticlesList(self):
        raise Exception("For Debugging")
        self.clearList("articles")
        articles = opn.get_all_articles(global_session())
        content_list = [(article.title, article.id) for article in articles]
        act.setListWidget(LArticleItem, self.list_articles, content_list)

    # page
    def setPageIndex(self, page: int, container_name: str = "stacked"):
        if container_name == "stacked":
            self.stackedWidget.setCurrentIndex(page)
        elif container_name == "tab":
            self.tabWidget.setCurrentIndex(page)
    
    def getPageIndex(self, container_name: str = "stacked"):
        if container_name == "stacked":
            return self.stackedWidget.currentIndex()
        elif container_name == "tab":
            return self.tabWidget.currentIndex()

    # others
    def changeState(self, state: bool):
        self.btn_search.setEnabled(state)
        self.btn_clear.setEnabled(state)
        self.btn_download.setEnabled(state)
        self.textedit_search.setEnabled(state)
        self.list_searchs.setEnabled(state)

    def syncState(self, state: bool):
        self.btn_sync.setEnabled(state)
        self.btn_sync_r.setEnabled(state)

    def print(self, content):
        self.log.append(content)
        content = markdown2.markdown("<br>".join(self.log))
        self.browser_cmd.setHtml(content)
        self.browser_cmd.verticalScrollBar().setValue(self.browser_cmd.verticalScrollBar().maximum())

    # --------------------------------------------------------------------------------
    # event functions
    
    
    # --------------------------------------------------------------------------------
    # slot functions
    def onSearchClicked(self):
        self.print("[DEBUG] Enter _onSearchClicked function")
        if (not self.textedit_search.toPlainText()) or not (search_pattern := self.textedit_search.toPlainText().strip()):
            self.print(fmt.RED_BOLD("No search pattern!"))
            return
        if search_pattern[0] == "@":
            self.shellCommand(search_pattern[1:])
        else:
            self.clearList("searchs")
            if search_results := self.doSearch(search_pattern):
                self.renderList(search_results, "searchs")
                self.print(fmt.RED_BOLD("Search Finished!"))
            else:
                self.print(fmt.RED_BOLD("No results found!"))

    def onImportClicked(self):
        self.print("[DEBUG] Enter _onImportClicked function")
        if not (file_path := QFileDialog.getOpenFileName(self, 'Open file', '', fmt.BIB_FILTER)[0]):
            return
        data = extract_bib_info(file_path)
        if not data:
            self.print(fmt.RED_BOLD("No valid information extracted!"))
            return
        if self.importArticle(data):
            self.print(fmt.RED_BOLD("Imported successfully!"))
        # self.showViewList()

    def onImportBatchClicked(self):
        self.print("[DEBUG] Enter _onImportBatchClicked function")
        if not (file_paths := QFileDialog.getOpenFileNames(self, 'Open folder', '', fmt.BIB_FILTER)[0]):
            return
        for file in file_paths:
            extracted_info = extract_bib_info(file)
            if not extracted_info:
                self.print(fmt.RED_BOLD("No valid information extracted!"))
                continue
            if self.importArticle(extracted_info):
                self.print(fmt.RED_BOLD("Imported successfully!"))
        # self.showViewList()
    
    def onManualClicked(self):
        self.print("[DEBUG] Enter _onManualClicked function")
        dialog = LArticleDialog(self, 'Add manually')
        if dialog.exec_() == QDialog.Rejected:
            return
        data = dialog.get_data()
        if not data.title:
            self.print(fmt.RED_BOLD("No title found!"))
            return
        if self.importArticle(data):
            self.print(fmt.RED_BOLD("Imported successfully!"))
        # self.showViewList()
    
    def onAddKeywordClicked(self):
        self.print("[DEBUG] Enter _onAddKeywordClicked function")
        if not self.focus_id:
            self.print(fmt.RED_BOLD("No valid article selected"))
            return
        dialog = LKeywordDialog(self, 'Add keyword')
        if dialog.exec_() == QDialog.Rejected:
            return
        keywords: List[str] = dialog.get_data()
        act.addKeywords(keywords)
        if self.getPageIndex("stacked") == 1:
            self.showArticleModifer(self.focus_id, ["kwd"])
        else:
            self.showArticleMain(self.focus_id)

    def onAddNoteClicked(self):
        self.print("[DEBUG] Enter _onAddNoteClicked function")
        if not self.focus_id:
            self.print(fmt.RED_BOLD("No valid article selected"))
            return
        dialog = LNoteDialog(self, 'Add note')
        if dialog.exec_() == QDialog.Rejected:
            return
        data = dialog.get_data()
        act.addNote(data)
        if self.getPageIndex("stacked") == 1:
            self.showArticleModifer(self.focus_id, ["notes"])
        else:
            self.showArticleMain(self.focus_id)

    def onDownloadClicked(self):
        self.print("[DEBUG] Enter _onDownloadClicked function")
        if not self.focus_id:
            self.print(fmt.RED_BOLD("No valid article selected"))
            return
        article = act.getArticle(self.focus_id)
        if not article.doi:
            self.print(fmt.RED_BOLD("No valid url found"))
            return
        self.download_id = self.focus_id

        path = fmt.absolute_path(article.local_path) or fmt.absolute_path(article.doi + ".pdf")
        self.worker = DownloadWorker(article.doi, path)
        self.worker.update_progress.connect(self.onDownloadProgress)
        self.worker.terminate_progress.connect(self.onDownloadTerminated)
        self.worker.finished.connect(self.onDownloadFinished)
        self.worker.start()

    def onDownloadProgress(self, percentage):
        self.log = []
        progress = fmt.progressbar(percentage)
        self.print(f"{progress} {percentage}%")

    def onDownloadTerminated(self, reason):
        self.worker.flag = False
        self.print(fmt.RED_BOLD(reason))

    def onDownloadFinished(self):
        flag = self.worker.flag
        self.worker.deleteLater()
        self.worker = None
        if not flag:
            return
        article = act.getArticle(self.download_id)
        path = fmt.absolute_path(article.local_path) or fmt.absolute_path(article.doi + ".pdf")
        if not os.path.exists(path):
            self.print(fmt.RED_BOLD("Download Failed!"))
        else:
            article.local_path = fmt.related_path(path)
            self.print(fmt.RED_BOLD("Download Finished!"))
            if self.focus_id == self.download_id:
                self.showArticleMain(self.focus_id)
                self.showArticleModifer(self.focus_id, ["all"])
        global_session().commit()
        self.download_id = None

    def onClearClicked(self):
        self.print("[DEBUG] Enter _onClearClicked function")
        self.clearArticleMain(self)
        self.clearArticleModifer(self)
        self.print(fmt.RED_BOLD("Noop!"))

    def onModifyClicked(self):
        self.print("[DEBUG] Enter _onModifyClicked function")
        if not self.focus_id:
            self.print(fmt.RED_BOLD("No valid article selected"))
            return
        self.btn_mdf.setText("Finish")
        self.btn_mdf.clicked.disconnect()
        self.btn_mdf.clicked.connect(self.onFinishClicked)
        self.setPageIndex(1, "stacked")
        self.showArticleModifer(self.focus_id, ["all"])
        self.changeState(False)

    def onFinishClicked(self):
        self.print("[DEBUG] Enter _onFinishClicked function")
        self.btn_mdf.setText("Modified")
        self.btn_mdf.clicked.disconnect()
        self.btn_mdf.clicked.connect(self.onModifyClicked)
        self.setPageIndex(0, "stacked")
        self.showArticleMain(self.focus_id)
        self.changeState(True)

    def onArticleModifierDoubleClicked(self, widget: QWidget, params):
        self.print("[DEBUG] Enter _onArticleModifierDoubleClicked function")
        assert(widget == self.browser_info)
        article = act.getArticle(self.focus_id)
        dialog = LArticleDialog(self, 'Modify article')
        dialog.set_data(article)
        if dialog.exec_() == QDialog.Rejected:
            return
        data = dialog.get_data()
        if not act.checkPath(fmt.absolute_path(data.local_path)):
            self.print(fmt.RED_BOLD("Warning: Invalid file path!"))
            data.local_path = None
        act.resetArticle(data, article)
        self.showArticleModifer(self.focus_id, ["info"])

    def onKeywordsModifierDoubleClicked(self, widget: QWidget, params):
        self.print("[DEBUG] Enter _onKeywordsModifierDoubleClicked function")
        assert(widget == self.browser_kwd)
        article = act.getArticle(self.focus_id)
        dialog = LKeywordDialog(self, 'Modify keyword')
        dialog.set_data(article.keywords)
        if dialog.exec_() == QDialog.Rejected:
            return
        keywords: List[str] = dialog.get_data()
        act.resetKeywords(keywords, article)
        self.showArticleModifer(self.focus_id, ["kwd"])

    def onNoteModifierAddClicked(self):
        self.print("[DEBUG] Enter _onNoteModifierAddClicked function")
        article = self.focus_id
        dialog = LNoteDialog(self, 'Add note')
        if dialog.exec_() == QDialog.Rejected:
            return
        data = dialog.get_data()
        act.addNote(data, article)
        self.showArticleModifer(self.focus_id, ["notes"])

    def onNoteModifierItemClicked(self, note_id):
        self.print("[DEBUG] Enter _onNoteModifierItemClicked function")
        note = opn.get_note(note_id)
        assert(note.article_id == self.focus_id)
        dialog = LNoteDialog(self, 'Modify note')
        dialog.set_data(note)
        if dialog.exec_() == QDialog.Rejected:
            return
        data = dialog.get_data()
        act.resetNote(data, note)
        self.showArticleModifer(self.focus_id, ["notes"])

    def onNoteSynchronousClicked(self):
        self.print("[DEBUG] Enter _onNoteSynchronousClicked function")
        assert(self.focus_id)
        article = act.getArticle(self.focus_id)
        assert(article.local_path)
        notes = opn.get_article_notes(article)
        annots = extract_annotations(fmt.absolute_path(article.local_path))

        if not annots:
            self.print(fmt.RED_BOLD("No annotations found!"))
            return

        notes_dict, annots_dict = {}, {}
        for note in notes:
            notes_dict.setdefault(note.page_number, []).append(note)
        for annot in annots:
            annots_dict.setdefault(annot[2], []).append(annot)
            
        n_page = max(list(notes_dict.keys()) + list(annots_dict.keys()))

        del_notes = []
        
        for p in range(1, n_page + 1):
            if not annots_dict.get(p, None):
                del_notes.extend(notes_dict.get(p, []))
            else:
                if notes_dict.get(p, None):
                    temp_notes = notes_dict[p]
                    for note in temp_notes:
                        refer_text = [annot[0] for annot in annots_dict[p]]
                        if note.quote_content in refer_text:
                            idx = refer_text.index(note.quote_content)
                            act.resetNote({
                                'note': annots_dict[p][idx][1],
                                'date': datetime.datetime.now().strftime("%Y-%m-%d"),
                                'quote_content': note.quote_content,
                                'page_number': p,
                            }, note)
                            annots_dict[p].pop(idx)
                        else:
                            del_notes.append(note)
                for annot in annots_dict[p]:
                    self.print("[DEBUG] Add note")
                    act.addNote({
                        'note': annot[1],
                        'date': datetime.datetime.now().strftime("%Y-%m-%d"),
                        'quote_content': annot[0],
                        'page_number': p,
                    }, article)
        for note in del_notes:
            act.deleteNote(note.id)

    def onFolderArticleAddClicked(self, parent_widget, node_id): # on delete
        self.print("[DEBUG] Enter _onFolderArticleAddClicked function")
        diag = LGroupDialog(self, 'Add article to folder')
        articles = opn.get_all_articles()
        for article in articles:
            widget = LCheckItem(article.id, article.title)
            diag.add_item(widget)
        if diag.exec_() == QDialog.Rejected:
            return
        articles = [act.getArticle(id) for id in diag.get_data()]
        nodes = [opn.add_node_article(global_session(), article, node_id) for article in articles]
        global_session().commit()

        item = self.tree_root.itemAt(parent_widget.pos())
        for article, node in zip(articles, nodes):
            widget = LArticleItem(article.id, article.title, node_id=node.node_id)
            act.addTreeWidgetItem(widget, item, self.tree_root)
            self.tree_root.update()

    def onFolderAddClicked(self): # on delete
        self.print("[DEBUG] Enter _onFolderAddClicked function")
        root_node = opn.get_root_node(global_session(), "ROOT")
        node = opn.add_node_folder(global_session(), "New Folder", root_node.node_id)
        global_session().commit()
        widget = LFolderItem(node.node_id, node.node_name)
        
        # insert the new folder item to second last position
        index_to_folder = self.tree_root.topLevelItemCount() - 1
        item = QTreeWidgetItem()
        self.tree_root.insertTopLevelItem(index_to_folder, item)
        self.tree_root.setItemWidget(item, 0, widget)

    def onFolderDeleteClicked(self, folder_widget): # on delete
        self.print("[DEBUG] Enter _onFolderDeleteClicked function")
        node_id = folder_widget.node_id
        act.deleteFolderNode(node_id)
        global_session().commit()
        act.removeTreeWidgetItem(folder_widget, self.tree_root)

    # --------------------------------------------------------------------------------
    # combo functions
    def shellCommand(self, command: str):
        if command == "ALL":
            self.clearList("searchs")
            articles = opn.get_all_articles(global_session())
            content_list = [(article.title, article.id) for article in articles]
            self.renderList(content_list, "searchs")
        elif command == "KW":
            keywords = opn.get_all_keywords(global_session())
            raise Exception("For Debugging")
            # content = fmt.keywords_md(keywords)
            # self.renderBrowser(content, "main")

    def doSearch(self, search_pattern) -> List[Tuple[str, int]]:
        articles = opn.search_title_articles(global_session(), search_pattern)
        keywords = opn.search_keyword_articles(global_session(), search_pattern)
        search_counts = {}
        for article in articles:
            search_counts[article.id] = search_counts.get(article.id, 0) + 1
        for keyword in keywords:
            for article in keyword.articles:
                search_counts[article.id] = search_counts.get(article.id, 0) + 1
        search_counts = sorted(search_counts.items(), key=lambda x: x[1], reverse=True)
        articles = [opn.get_article(global_session(), article_id) for article_id, _ in search_counts]
        if len(articles) == 0:
            return None
        return [(fmt.highlight_search_results(article.title, search_pattern), article.id) for article in articles]

    def importArticle(self, datas: ArticleData | List[ArticleData]):
        if isinstance(datas, ArticleData):
            datas = [datas]
        for data in datas:
            if data.local_path is not None and not act.checkPath(fmt.absolute_path(data.local_path)):
                self.print(fmt.RED_BOLD("Warning: Invalid file path!"))
                data.local_path = None
            article = opn.create_article(data)
            opn.add_article(article)
            self.mvm.add_item(article.id, to_profile(data))
        return True

    def showArticleMain(self, article: Article | int):
        article = act.getArticle(article)
        content = fmt.get_article_html(article)
        content = fmt.wrap_html(content, fmt.CSS_THEMES["microsoft_white"])
        # content = fmt.article_md(article)
        self.setFocusArticle(article.id)
        self.renderBrowser(content, "main")
        is_sync = not article.local_path is None
        self.syncState(is_sync)

    def showArticleModifer(self, article: Article | int, browser_name: str | List[str] = "info"):
        article = act.getArticle(article)
        if isinstance(browser_name, str):
            browser_name = [browser_name]
        if browser_name[0] == "all":
            browser_name = ["info", "kwd", "notes"]
        self.setFocusArticle(article.id)
        if "info" in browser_name:
            # content = fmt.article_md(article, article_only=True)
            content = fmt.get_article_html(article, article_only=True)
            content = fmt.wrap_html(content, fmt.CSS_THEMES["microsoft_white"])
            self.renderBrowser(content, "info")
        if "kwd" in browser_name:
            # content = fmt.keywords_md(article.keywords)
            content = fmt.get_keywords_html(article.keywords)
            content = fmt.wrap_html(content, fmt.CSS_THEMES["microsoft_white"])
            self.renderBrowser(content, "kwd")
        if "notes" in browser_name:
            pass
            # TODO to be developed
            # self.clearList("notes")
            # self.renderList([(fmt.note_md(note), note.id) for note in article.notes], "notes") # TODO

    def showViewList(self):
        self.renderTree("ROOT")
        self.renderAllArticlesList()

    def clearArticleMain(self):
        self.clearBrowser("main")
        self.syncState(False)

    def clearArticleModifer(self):
        self.clearBrowser("info")
        self.clearBrowser("kwd")
        self.clearList("notes")