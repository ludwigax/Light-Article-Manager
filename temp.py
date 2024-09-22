from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                               QPushButton, QLabel, QListWidget, QListWidgetItem)
from PySide6.QtCore import Qt

class SearchWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # 初始化窗口
        self.setWindowTitle("Search Window")
        self.setGeometry(100, 100, 600, 400)
        
        # 主布局
        main_layout = QVBoxLayout()
        
        # 搜索框和按钮（虽然暂时没有功能）
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Enter search keyword...")
        self.search_button = QPushButton("Search", self)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        
        # 搜索状态标签
        self.status_label = QLabel(self)
        self.status_label.setText("Status: Showing preloaded search results")
        
        # ListWidget 显示每页的标题
        self.list_widget = QListWidget(self)
        self.list_widget.itemClicked.connect(self.goto_page)
        
        # 用于显示搜索结果内容的 QLabel
        self.result_label = QLabel(self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setWordWrap(True)  # 允许换行
        
        # 翻页按钮
        navigation_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous", self)
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button = QPushButton("Next", self)
        self.next_button.clicked.connect(self.next_page)
        navigation_layout.addWidget(self.prev_button)
        navigation_layout.addWidget(self.next_button)
        
        # 将组件添加到主布局
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.list_widget)
        main_layout.addWidget(self.result_label)
        main_layout.addLayout(navigation_layout)
        
        self.setLayout(main_layout)
        
        # 预加载的搜索结果
        self.search_results = self.mock_search_results()
        self.current_page = 0
        
        # 加载预设的结果
        self.load_results()
    
    def mock_search_results(self):
        """模拟一些预加载的搜索结果"""
        return [
            {'title': 'Result 1', 'content': 'This is the content for result 1.'},
            {'title': 'Result 2', 'content': 'This is the content for result 2.'},
            {'title': 'Result 3', 'content': 'This is the content for result 3.'},
            {'title': 'Result 4', 'content': 'This is the content for result 4.'},
            {'title': 'Result 5', 'content': 'This is the content for result 5.'}
        ]
    
    def load_results(self):
        """加载预设的搜索结果到界面"""
        self.list_widget.clear()
        
        for index, result in enumerate(self.search_results):
            # 将每页的标题添加到 ListWidget
            list_item = QListWidgetItem(f"Page {index + 1}: {result['title']}")
            self.list_widget.addItem(list_item)
        
        # 显示第一页
        self.current_page = 0
        self.update_page()
    
    def goto_page(self, item):
        """跳转到指定页面"""
        self.current_page = self.list_widget.row(item)
        self.update_page()
    
    def update_page(self):
        """更新显示当前页面的内容"""
        result = self.search_results[self.current_page]
        self.result_label.setText(result['content'])
        self.status_label.setText(f"Status: Viewing page {self.current_page + 1}/{len(self.search_results)}")
    
    def prev_page(self):
        """翻到上一页"""
        if self.current_page > 0:
            self.current_page -= 1
            self.update_page()
    
    def next_page(self):
        """翻到下一页"""
        if self.current_page < len(self.search_results) - 1:
            self.current_page += 1
            self.update_page()

# 运行程序
if __name__ == "__main__":
    app = QApplication([])
    window = SearchWindow()
    window.show()
    app.exec()
