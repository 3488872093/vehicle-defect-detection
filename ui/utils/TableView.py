# coding: utf-8
import sys
from PySide6.QtWidgets import QHeaderView, QApplication, QStyleOptionViewItem, QTableWidgetItem, QWidget, QHBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtGui import QPalette, QColor, QFont
from qfluentwidgets import TableWidget, TableItemDelegate

class TableViewDelegate(TableItemDelegate):
    """ 自定义委托，设置文本颜色与字体 """
    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex):
        super().initStyleOption(option, index)
        # 设置文本颜色为深色
        text_color = QColor("#3b3c50")
        option.palette.setColor(QPalette.Text, text_color)
        option.palette.setColor(QPalette.HighlightedText, text_color)
        # 使用黑体字体
        option.font.setFamily("Microsoft YaHei")
        option.font.setPointSize(14)

class TableViewQWidget(QWidget):
    def __init__(self, infoList=None):
        super().__init__()
        self.setWindowTitle("结果统计")
        self.hBoxLayout = QHBoxLayout(self)
        self.tableView = TableWidget(self)
        
        # 全局设置表格字体为黑体
        self.tableView.setFont(QFont("Microsoft YaHei", 14))
        # 设置自定义委托
        self.tableView.setItemDelegate(TableViewDelegate(self.tableView))
        
        # 初始化美化样式
        self._initTableStyle()
        
        # 初始化数据
        self.Info = infoList if infoList else list()
        self._initData()
        
        self.hBoxLayout.setContentsMargins(20, 10, 20, 10)
        self.hBoxLayout.addWidget(self.tableView)
        self.resize(600, 600)
        
        # 添加投影效果，提升立体感
        self._setDropShadow()

    def _setDropShadow(self):
        """ 设置表格的投影效果 """
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.tableView.setGraphicsEffect(shadow)

    def _initTableStyle(self):
        """ 初始化蓝白简约风格的表格样式 """
        # 开启交替行背景颜色
        self.tableView.setAlternatingRowColors(True)
        
        # 表头样式：纯色蓝背景、白色文字、黑体字、圆润视觉效果
        header_style = """
        QHeaderView::section {
            background-color: #3c85bc;
            color: white;
            font-family: "Microsoft YaHei";
            font-size: 18px;
            font-weight: bold;
            padding: 8px;
            border: none;
        }
        """
        self.tableView.horizontalHeader().setStyleSheet(header_style)
        self.tableView.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        
        # 整体表格样式：白色背景、柔和网格、圆角边框及自定义字体
        self.tableView.setStyleSheet("""
        QTableWidget {
            border: 1px solid #d0d0d0;
            border-radius: 8px;
            padding: 6px;
            background-color: #ffffff;
            gridline-color: #d0d0d0;
        }
        QTableWidget::viewport {
            border: none;
            background: transparent;
        }                                   
        QTableWidget::item:alternate {
            background-color: #e9f1f6;
        }
        QTableWidget::item:hover {
            background-color: #d0eaff;
        }
        QScrollBar:vertical {
            background: #f0f0f0;
            width: 10px;
            margin: 0px;
            border-radius: 5px;
        }
        QScrollBar::handle:vertical {
            background: #a1c9f4;
            min-height: 20px;
            border-radius: 5px;
        }
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0px;
        }
        """)
        
        # 表格基础设置
        self.tableView.setRowCount(1000)
        self.tableView.setColumnCount(3)
        self.tableView.verticalHeader().hide()
        self.tableView.setHorizontalHeaderLabels(['序号', '类别', '数量'])
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.setSortingEnabled(True)

    def _initData(self):
        """ 初始化表格数据 """
        info_count = 1
        for i, info in enumerate(self.Info):
            # 序号列
            item = QTableWidgetItem(str(info_count))
            item.setTextAlignment(Qt.AlignCenter)
            self.tableView.setItem(i, 0, item)
            info_count += 1
            # 其他列数据
            for j in range(1, len(info) + 1):
                item = QTableWidgetItem(info[j - 1])
                item.setTextAlignment(Qt.AlignCenter)
                self.tableView.setItem(i, j, item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = TableViewQWidget()
    w.show()
    app.exec()
