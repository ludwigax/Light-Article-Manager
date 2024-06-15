import sys
from PyQt5.QtWidgets import QApplication, QTreeView, QMainWindow, QHeaderView, QMenu, QStyleOptionViewItem, QStyle
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QSortFilterProxyModel, QModelIndex, QRect

from mvc.delegate import IconButtonDelegate

from mvc.module import NonNestedModule, NestedModule

from archi import ProfileData

data_list = [
    (0, ProfileData('Folder Test', '', '', '', '2022-01-01', '')),
    (-1, ProfileData('Article 1', '2021', 'Journal A', 'Author A', '2022-01-01', '1')),
    (-1, ProfileData('Article 2', '2020', 'Journal B', 'Author B', '2022-01-02', '2')),
    (-1, ProfileData('Article 3', '2019', 'Journal C', 'Author C', '2022-01-03', '3')),
    (0, ProfileData('Folder Train', '', '', '', '2022-04-01', '')),
    (-1, ProfileData('Article 4', '2018', 'Journal D', 'Author D', '2022-01-04', '4')),
    (-1, ProfileData('Article 5', '2017', 'Journal E', 'Author E', '2022-01-05', '5')),
    (-1, ProfileData('Article 6', '2016', 'Journal F', 'Author F', '2022-01-06', '6')),
    (-1, ProfileData('Article 7', '2015', 'Journal G', 'Author G', '2022-01-07', '7')),
    (-1, ProfileData('Article 8', '2014', 'Journal H', 'Author H', '2022-01-08', '8')),
    (-1, ProfileData('Article 9', '2013', 'Journal I', 'Author I', '2022-01-09', '9')),
    (-1, ProfileData('Article 10', '2012', 'Journal J', 'Author F', '2022-01-09', '9')),
    (-1, ProfileData('Article 11', '2011', 'Journal K', 'Author D', '2022-01-09', '9')),
    (-1, ProfileData('Article 12', '2010', 'Journal I', 'Author I', '2022-01-09', '9')),
    (0, ProfileData('Folder Other', '', '', '', '2022-07-01', '')),
]

data_list2 = [
    ((0, 0), ProfileData('Article 1', '2021', 'Journal A', 'Author A', '2022-01-01', '1')),
    ((0, 1), ProfileData('Article 2', '2020', 'Journal B', 'Author B', '2022-01-02', '2')),
    ((0, 2), ProfileData('Article 3', '2019', 'Journal C', 'Author C', '2022-01-03', '3')),
    ((1, 0), ProfileData('Article 4', '2018', 'Journal D', 'Author D', '2022-01-04', '4')),
    ((1, 1), ProfileData('Article 5', '2017', 'Journal E', 'Author E', '2022-01-05', '5')),
    ((1, 2), ProfileData('Article 6', '2016', 'Journal F', 'Author F', '2022-01-06', '6')),
    ((1, 3), ProfileData('Article 7', '2015', 'Journal G', 'Author G', '2022-01-07', '7')),
    ((1, 4), ProfileData('Article 8', '2014', 'Journal H', 'Author H', '2022-01-08', '8')),
    ((1, 5), ProfileData('Article 9', '2013', 'Journal I', 'Author I', '2022-01-09', '9')),
    ((1, 6), ProfileData('Article 10', '2012', 'Journal J', 'Author F', '2022-01-09', '9')),
    ((1, 7), ProfileData('Article 11', '2011', 'Journal K', 'Author D', '2022-01-09', '9')),
    ((1, 8), ProfileData('Article 12', '2010', 'Journal I', 'Author I', '2022-01-09', '9')),
]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TreeView Example")
        self.setGeometry(300, 300, 600, 400)
        
        self.mvm = NestedModule(self, columns=None)
        # self.mvm = NonNestedModule(self, columns=None)
        self.setCentralWidget(self.mvm.tree_view)

        self.mvm.set_delegate(6, IconButtonDelegate)

        # Adding Items to Model
        self.list_add(data_list)

        # for data in data_list2:
        #     self.add_article(data[1])

    def add_article(self, data):
        self.mvm.add_item(0, data)

    def list_add(self, data_list):
        for idx, data in data_list:
            if idx == 0:
                item = self.mvm.add_item(0, idx, data)
            else:
                self.mvm.add_item(0, idx, data, item)

    def apply_external_sort(self, indices):
        self.mvm.proxy_model.setExternalOrder(indices)

    def selected_row_action(self):
        print("Action for selected row")

    def unselected_row_action(self):
        print("Action for no selected row")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    # 示例：应用外部排序
    external_indices = [1, 0]  # 假设外部排序结果的索引
    main_window.apply_external_sort(external_indices)

    sys.exit(app.exec_())
