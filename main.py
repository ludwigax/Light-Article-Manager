import os
import sys
from typing import List, Tuple

from PyQt5.QtWidgets import QApplication
# from widget.mainwindow import LMainWindow
from widget.mainwindow2 import LMainWindow

os.environ["LAM_WORK_DIR"] = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':

    # temp
    from func import global_session
    from utils import opn
    from sqlalchemy import text

    # root = opn.add_node_folder(global_session(), "ROOT", None)
    # folder1 = opn.add_node_folder(global_session(), "Folder1", root.node_id)
    # for article in opn.get_all_articles(global_session()):
    #     opn.add_node_article(global_session(), article, folder1.node_id)

    app = QApplication(sys.argv)
    mainWindow = LMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())