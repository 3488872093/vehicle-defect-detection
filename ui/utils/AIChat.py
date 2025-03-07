import requests
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QFrame,
    QWidget, QLabel, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFontMetrics
from together import Together

class ChatDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.client = Together(api_key="ae574e22d6dd455379eff3c0894279b8ad67f439a1013be9aea9adf1dc121860")
        self.setWindowTitle("AIChat")
        self.resize(800, 600)
        self.setup_styles()
        self.initUI()
        self.setup_connections()

    def setup_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
            }
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 25px;
                padding: 12px 20px;
                font-size: 16px;
                background-color: white;
                margin: 10px;
            }
            QPushButton {
                background-color: #4A90E2;
                color: white;
                border: none;
                border-radius: 24px; 
                width: 48px;
                height: 48px;
                padding: 0px;
                margin-right: 15px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
            QPushButton:pressed {
                background-color: #2A5F8F;
            }
            QScrollBar:vertical {
                background: #EBEBEB;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #C1C1C1;
                border-radius: 4px;
                min-height: 30px;
            }
        """)

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        # 创建消息显示区域，使用 QScrollArea+QWidget 嵌套布局实现
        self.chat_area_widget = QWidget()
        self.chat_area_widget.setStyleSheet("background-color: white;")
        self.chat_layout = QVBoxLayout(self.chat_area_widget)
        self.chat_layout.setContentsMargins(10, 10, 10, 10)
        self.chat_layout.setSpacing(10)
        self.chat_layout.addStretch()  # 底部拉伸空间，保证消息靠上

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.chat_area_widget)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        main_layout.addWidget(self.scroll_area, stretch=1)

        # 输入区域：底部的输入框和发送按钮
        input_frame = QFrame()
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(5, 5, 5, 5)
        input_layout.setSpacing(10)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("输入消息...")
        self.send_button = QPushButton("发送")

        input_layout.addWidget(self.input_field, stretch=1)
        input_layout.addWidget(self.send_button)
        main_layout.addWidget(input_frame)

    def setup_connections(self):
        self.send_button.clicked.connect(self.send_message)
        self.input_field.returnPressed.connect(self.send_message)

    def send_message(self):
        message = self.input_field.text().strip()
        if not message:
            return

        self.append_message(message, is_user=True)
        self.input_field.clear()

        # 模拟 1 秒后 AI 回复
        QTimer.singleShot(1000, lambda: self.process_ai_response(message))

    def process_ai_response(self, message):
        response = self.call_deepseek_api(message)
        self.append_message(response or "暂时无法获取回复", is_user=False)

    def append_message(self, text, is_user=False):
        # 创建单条消息的容器组件
        container = QWidget()
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(30)

        # 发送者标签
        sender_label = QLabel("You" if is_user else "AI")
        sender_label.setStyleSheet("""
            QLabel {
                color: %s;
                font-weight: 600;
                font-size: 14px;
                min-width: 40px;
                padding: 2px 5px;
                border-radius: 4px;
            }
        """ % ("#4A90E2" if is_user else "#666666"))
        sender_label.setAlignment(Qt.AlignCenter)

        # 消息气泡
        bubble = self.create_message_bubble(text, is_user)
        
        # 布局排列：用户消息右对齐，AI 消息左对齐
        if is_user:
            layout.addStretch()
            layout.addWidget(bubble, alignment=Qt.AlignRight)
            layout.addWidget(sender_label, alignment=Qt.AlignRight)
            layout.setContentsMargins(60, 0, 0, 0)  # 右边距留白
        else:
            layout.addWidget(sender_label, alignment=Qt.AlignLeft)
            layout.addWidget(bubble, alignment=Qt.AlignLeft)
            layout.setContentsMargins(0, 0, 60, 0)  # 左边距留白
            layout.addStretch()

        # 将新消息插入到聊天区（在最后一个拉伸项之前）
        self.chat_layout.insertWidget(self.chat_layout.count()-1, container)
        QTimer.singleShot(100, self.scroll_to_bottom)

    def create_message_bubble(self, text, is_user):
        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setTextFormat(Qt.RichText)
        bubble.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        bubble.setMaximumWidth(500)
        
        style = """
            QLabel {
                background: %s;
                color: %s;
                padding: 15px 20px;
                border-radius: 12px;
                %s
                font-size: 16px;
                line-height: 1.4;
            }
        """ % (
            "#E3EFFF" if is_user else "#FFFFFF",
            "#333333" if is_user else "#444444",
            "border: 1px solid #D0E0FF;" if is_user else "border: 1px solid #EEEEEE;"
        )
        bubble.setStyleSheet(style)
        return bubble

    def scroll_to_bottom(self):
        # 保证滚动条始终滚动到底部
        scroll_bar = self.scroll_area.verticalScrollBar()
        scroll_bar.setRange(0, scroll_bar.maximum())
        scroll_bar.setValue(scroll_bar.maximum())

    def call_deepseek_api(self, message):
        try:
            response = self.client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V3",
                messages=[{"role": "user", "content": message}],
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"API请求错误: {e}")
            return None


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dialog = ChatDialog()
    dialog.show()
    sys.exit(app.exec())
