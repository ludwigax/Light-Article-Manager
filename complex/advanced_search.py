from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QListWidget, \
    QLabel, QMessageBox, QToolBar, QStackedWidget, QRadioButton, QButtonGroup, QFrame, \
    QPushButton

from widget.button import StyleButton
from widget.label import KVLabel
from widget.search import SearchWidget
from widget.drag import DragCountLabel, DragListWidget, MetaItem
from widget.emitter import emitter

from complex.easy_search import EasySearchZone

from utils.thread import TaskQueue
from tools.web import webfuncs as wbf
from tools.web import webfuncs_selenium as wbfs
from tools.web import parse as prs

import setting
from setting import ACTIVE_ADVANCED_SEARCH_ENGINE

# small functions
def test_internet():
    return wbf.tcping(wbf.cfg.ADDRESSINFO)[0]

def google_login():
    flag, account_name = wbfs.google_login()
    if flag:
        return [account_name, None]
    else:
        raise Exception("Google Login Failed")

def wos_login():
    sid, wossid = wbfs.wos_login()
    if wossid:
        return [None, wossid]
    else:
        raise Exception("WOS Login Failed")
    
def gss(text):
    return wbfs.google_scholar_get(text)

def woss(text, wossid):
    kwd = [wbf.wos_keywords("topic", text, "AND")]
    return wbf.wos_query_post(kwd, wossid)

def cfs(text):
    return wbf.crossref_get(text)

def arxs(text):
    return wbf.arxiv_get(text)

def engine_search(text, wossid, idx):
    if idx == 0:
        return gss(text)
    elif idx == 1:
        return cfs(text)
    elif idx == 2:
        if not wossid:
            raise Exception("WOS Token Not Found")
        return woss(text, wossid)
    elif idx == 3:
        return arxs(text)
    
def engine_parse(response, idx):
    if idx == 0:
        return prs.google_scholar_parse(response)
    elif idx == 1:
        return prs.crossref_parse(response)
    elif idx == 2:
        return prs.wos_query_parse(response)
    elif idx == 3:
        return prs.arxiv_parse(response)

# ----------------------------
class AdvancedSearchZone(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.search_engine = 0
        self.wossid = None
        self.google_account = None
        self.task_queue = TaskQueue(1)

        if ACTIVE_ADVANCED_SEARCH_ENGINE:
            self.activate()
        else:
            self.inactivate()
    
    def inactivate(self):
        self.init_widget = StyleButton(self, "RED")
        self.init_widget.setText("Enable Advanced")
        self.init_widget.setFixedSize(170, 40)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.init_widget)
        self.setLayout(layout)
        self.init_widget.clicked.connect(self.enable_advanced_search)

    def enable_advanced_search(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Confirmation")
        msg_box.setText((
            "这些高级功能可以让你使用伪装技术，执行更复杂和大规模的任务，"
            "包括从学术网站上进行高度定制的文献检索和抓取。要启用这些高级功能，"
            "你需要安装Selenium Python扩展、Chrome浏览器和ChromeDriver，"
            "还要配置Chrome的用户资料路径。请注意，一些网站可能禁止e数据抓取；"
            "此功能仅用于教育和学术目的，不能用于违法爬取网站。"
        ))
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

        setting.set_cache("active_advanced_search", True)
        self.init_widget.setParent(None)
        self.init_widget.deleteLater()
        self.init_widget = None
        QWidget().setLayout(self.layout())
        
        self.update()
        self.activate()

    def activate(self):
        layout = QVBoxLayout()

        # toolbar
        self.toolbar = QToolBar("Toolbar", self)
        self.test_internet = StyleButton(self, "GREEN")
        self.test_internet.setText("TCPing")
        self.test_internet.clicked.connect(self.action_test_internet)
        self.login_google = StyleButton(self, "RED")
        self.login_google.setText("Login Google")
        self.login_google.clicked.connect(self.action_login_google)
        self.login_wos = StyleButton(self, "BLUE")
        self.login_wos.setText("Login WOS")
        self.login_wos.clicked.connect(self.action_login_wos)

        self.toolbar.addWidget(self.test_internet)
        self.toolbar.addWidget(self.login_google)
        self.toolbar.addWidget(self.login_wos)

        layout.addWidget(self.toolbar)

        # layout 1
        layout_1 = QGridLayout()
        layout_1.setSpacing(10)

        self.google_label = KVLabel("GOOGLE", "UNKNOWN", "black")
        self.crossref_label = KVLabel("CROSSREF", "UNKNOWN", "black")
        self.wos_label = KVLabel("WOS", "UNKNOWN", "black")
        self.arxiv_label = KVLabel("ARXIV", "UNKNOWN", "black")

        layout_1.addWidget(self.google_label, 0, 0)
        layout_1.addWidget(self.crossref_label, 0, 1)
        layout_1.addWidget(self.wos_label, 0, 2)
        layout_1.addWidget(self.arxiv_label, 0, 3)

        self.google_account_label = KVLabel("GOOGLE ACCOUNT", "my_google_account", "black")
        self.wos_credentials_label = KVLabel("WOS TOKEN", "my_wos_credentials", "black")

        layout_1.addWidget(self.google_account_label, 1, 0, 1, 2)
        layout_1.addWidget(self.wos_credentials_label, 1, 2, 1, 2)
        layout.addLayout(layout_1)

        # layout 2
        layout_2 = QHBoxLayout()

        # layout 2 left
        layout_2l = QVBoxLayout()
        choices = ["GOOGLE", "CROSSREF", "WOS", "ARXIV"]
        radio_button_style = """
            QRadioButton {
                background-color: #f0f0f0;
                font-weight: bold;
                font-size: 12px;
                padding: 2px;
            }
            QRadioButton:checked {
                background-color: #e0e0e0;
                color: #000000;
            }
        """

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        button_layout = QHBoxLayout()
        for i, choice in enumerate(choices):
            radio_button = QRadioButton(choice, self)
            radio_button.setCheckable(True)
            radio_button.setStyleSheet(radio_button_style)
            self.button_group.addButton(radio_button)
            button_layout.addWidget(radio_button)
        layout_2l.addLayout(button_layout)

        self.stacked_widget = QStackedWidget()
        for i in range(1): # TODO
            self.page_google = EasySearchZone(self)
            self.stacked_widget.addWidget(self.page_google)
        layout_2l.addWidget(self.stacked_widget)
        layout_2.addLayout(layout_2l)

        # layout 2 right
        layout_2r = QVBoxLayout()
        self.buff_listwidget = DragListWidget(True, False)
        self.buff_listwidget.setFrameShape(QFrame.Panel)
        self.buff_listwidget.setFrameShadow(QFrame.Sunken)
        self.buff_listwidget.setLineWidth(2)

        self.buff_label = DragCountLabel(True, False)
        self.buff_label.setFrameShape(QFrame.Panel)
        self.buff_label.setFrameShadow(QFrame.Sunken)
        self.buff_label.setLineWidth(2)
        self.buff_label.setAlignment(Qt.AlignCenter)

        self.clear_list_button = QPushButton("Clear List")
        self.clear_bucket_button = QPushButton("Clear Bucket")
        self.import_button = QPushButton("Import Result")
        self.import_button.setEnabled(False)

        layout_2r.addWidget(self.buff_listwidget)
        layout_2r.addWidget(self.buff_label)
        layout_2r.addWidget(self.clear_list_button)
        layout_2r.addWidget(self.clear_bucket_button)
        layout_2r.addWidget(self.import_button)
        layout_2r.setStretch(0, 3)
        layout_2r.setStretch(1, 1)

        layout_2.addLayout(layout_2r)
        layout_2.setStretch(0, 7)
        layout_2.setStretch(1, 3)

        layout.addLayout(layout_2)

        self.setLayout(layout)
        self.set_slots()

    def set_slots(self):
        self.button_group.buttonClicked.connect(self.set_engine)
        self.page_google.search_widget.search_signal.connect(self.action_start_search)
        self.clear_list_button.clicked.connect(self.buff_listwidget.clear)
        self.clear_bucket_button.clicked.connect(self.buff_label.clearMetaData)
        self.import_button.clicked.connect(self.import_result)
        self.buff_label._metadats_changed.connect(self.import_button.setEnabled)

    def set_taskqueue(self, task_queue: TaskQueue):
        self.task_queue = task_queue

    def action_test_internet(self):
        self.task_queue.add_task(
            test_internet, 
            (), 
            callback=[self.set_status, self.action_error_display]
        )

    def action_login_google(self):
        self.task_queue.add_task(
            google_login, 
            (), 
            callback=[self.set_accounts, self.action_error_display]
        )

    def action_login_wos(self):
        self.task_queue.add_task(
            wos_login, 
            (), 
            callback=[self.set_accounts, self.action_error_display]
        )

    def action_start_search(self, text):
        if not text:
            return
        
        search = lambda x: engine_search(x, self.wossid, self.search_engine)
        parse = lambda x: self.action_parsing_search(x, self.search_engine)
        self.task_queue.add_task(
            search,
            params=(text,),
            callback=[parse, self.action_error_display]
        )

    def action_parsing_search(self, response, idx):
        results = engine_parse(response, idx)
        self.page_google.set_search_results(results)
        print("handle search")

    def action_error_display(self, error):
        self.page_google.render_status(f"Error: {error}")

    def set_status(self, params):
        flags = ["UNACCESS", "ACCESS"]
        colors = ["red", "green"]
        self.google_label.setTexts("GOOGLE", flags[params[0]], colors[params[0]])
        self.crossref_label.setTexts("CROSSREF", flags[params[1]], colors[params[1]])
        self.wos_label.setTexts("WOS", flags[params[2]], colors[params[2]])
        self.arxiv_label.setTexts("ARXIV", flags[params[3]], colors[params[3]])

    def set_accounts(self, params):
        if params[0]:
            self.google_account = params[0]
            self.google_account_label.setTexts("GOOGLE ACCOUNT", params[0], "purple")
        if params[1]:
            self.wossid = params[1]
            self.wos_credentials_label.setTexts("WOS TOKEN", params[1], "purple")

    def set_engine(self, button):
        idx = self.button_group.buttons().index(button)
        if idx == 2:
            self.page_google.render_status("Error: WOS is not access now")
            self.button_group.buttons()[0].setChecked(True)
            self.search_engine = 0
            raise Exception("WOS is not access now")
        print(f"Set Engine {idx}")
        self.search_engine = idx
        from setting import set_cache
        set_cache("search_engine", idx)

    def import_result(self):
        if not self.buff_label._metadatas:
            self.import_button.setEnabled(False)
            return
        
        for metadata in self.buff_label._metadatas:
            emitter.import_internet.emit(metadata)
        self.import_button.setEnabled(False)
        self.buff_label.clearMetaData()

    def deleteLater(self):
        self.task_queue.stop_threads()
        super().deleteLater()