from PySide6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem, QStyle
from PySide6.QtGui import  QIcon
from PySide6.QtCore import Qt

from mvc import funcs

class IconButtonDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        if option.state & QStyle.State_MouseOver:
            style = option.widget.style()
            style.drawPrimitive(QStyle.PE_PanelItemViewItem, option, painter, option.widget)
            icon = QIcon("../ui/src/plus.png")
            icon.paint(painter, option.rect, Qt.AlignLeft)
        else:
            super().paint(painter, option, index)

    def editorEvent(self, event, model, option, index):
        if event.type() == event.MouseButtonRelease and event.button() == Qt.LeftButton:
            row = index.row()
            print(f"Icon clicked, row: {row}")

            source_index = model.mapToSource(index)
            print(f"Delegate clicked: {index.row()}")
            
            # outside function
            funcs.on_row_delegate_clicked(source_index)
            # end
            return True
        return super().editorEvent(event, model, option, index)