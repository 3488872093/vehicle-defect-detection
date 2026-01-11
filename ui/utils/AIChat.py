import os
from datetime import datetime
import markdown
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QFrame,
    QWidget, QTextEdit, QScrollArea, QSizePolicy, QLabel, QApplication
)
from PySide6.QtCore import Qt, QTimer
from together import Together
import sys

class ChatDialog(QDialog):
    # 缓存样式，避免重复生成
    USER_BUBBLE_STYLE = """
        QTextEdit {
            background: #E3EFFF;
            color: #333333;
            padding: 15px 20px;
            border-radius: 12px;
            border: 1px solid #D0E0FF;
            font-size: 16px;
            line-height: 1.4;
        }
    """
    AI_BUBBLE_STYLE = """
        QTextEdit {
            background: #FFFFFF;
            color: #444444;
            padding: 15px 20px;
            border-radius: 12px;
            border: 1px solid #EEEEEE;
            font-size: 16px;
            line-height: 1.4;
        }
    """
    SENDER_STYLE = """
        QLabel {
            color: %s;
            padding: 2px 5px;
            border-radius: 4px;
            font-weight: bold;
        }
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        # 从环境变量获取 API 密钥
        self.client = Together(api_key=os.getenv("TOGETHER_API_KEY", "ae574e22d6dd455379eff3c0894279b8ad67f439a1013be9aea9adf1dc121860"))
        self.setWindowTitle("AIChat")
        self.resize(700, 500)
        self.setup_styles()
        self.initUI()
        self.setup_connections()

    def setup_styles(self):
        """设置全局样式"""
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
            QLineEdit:disabled {
                background-color: #F5F5F5;
                color: #000000;
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
        """初始化界面布局"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        # 聊天区域
        self.chat_area_widget = QWidget()
        self.chat_area_widget.setStyleSheet("background-color: white;")
        self.chat_layout = QVBoxLayout(self.chat_area_widget)
        self.chat_layout.setContentsMargins(10, 10, 10, 10)
        self.chat_layout.setSpacing(10)
        self.chat_layout.addStretch()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.chat_area_widget)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        main_layout.addWidget(self.scroll_area, stretch=1)

        # 输入区域
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
        """设置信号与槽连接"""
        self.send_button.clicked.connect(self.send_message)
        self.input_field.returnPressed.connect(self.send_message)

    def send_message(self):
        """发送用户消息"""
        message = self.input_field.text().strip()
        if not message:
            return

        self.append_message(message, is_user=True)
        self.input_field.setEnabled(False)
        self.input_field.setPlaceholderText("AI 正在思考...")
        self.input_field.clear()

        QTimer.singleShot(1000, lambda: self.process_ai_response(message))
        QTimer.singleShot(1000, lambda: [self.input_field.setEnabled(True), self.input_field.setPlaceholderText("输入消息...")])

    def process_ai_response(self, message):
        """处理 AI 回复"""
        response = self.call_deepseek_api(message)
        self.append_message(response or "暂时无法获取回复", is_user=False)


    def create_message_bubble(self, text, is_user):
        """创建自适应内容的消息气泡"""
        # 转换 Markdown 为 HTML
        html = markdown.markdown(text)

        # 创建气泡容器
        bubble = QLabel()
        bubble.setWordWrap(True)  # 允许自动换行
        bubble.setTextFormat(Qt.RichText)
        bubble.setText(html)
        bubble.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # 设置样式
        bubble_style = [
            "background: %s;" % ("#E3EFFF" if is_user else "#FFFFFF"),
            "color: %s;" % ("#333333" if is_user else "#444444"),
            "padding: 12px 16px;",
            "border-radius: 12px;",
            "border: 1px solid %s;" % ("#D0E0FF" if is_user else "#EEE"),
            "font-size: 15px;",
            "line-height: 1.5;"
        ]
        bubble.setStyleSheet("QLabel{" + " ".join(bubble_style) + "}")

        # 设置最大宽度（动态计算，窗口宽度的 65%）
        max_bubble_width = int(self.width() * 0.65)

        # 计算内容的理想大小
        bubble.setMaximumWidth(max_bubble_width)  # 设置最大宽度限制
        bubble.adjustSize()  # 调整大小以适应内容
        ideal_width = bubble.sizeHint().width()  # 获取内容的理想宽度
        ideal_height = bubble.sizeHint().height()  # 获取内容的理想高度

        # 如果内容宽度小于最大宽度，则使用实际宽度，否则使用最大宽度并依赖换行
        final_width = min(ideal_width, max_bubble_width)
        bubble.setFixedWidth(final_width)  # 设置最终宽度
        bubble.setMinimumHeight(ideal_height)  # 设置最小高度，确保内容完全显示

        return bubble
    
    def append_message(self, text, is_user=False):
        """添加消息到聊天区域"""
        container = QWidget()
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)  # 发送者标签与气泡之间的水平间距

        sender_label = QLabel("You" if is_user else "AI")
        sender_label.setStyleSheet(self.SENDER_STYLE % ("#4A90E2" if is_user else "#666666"))
        sender_label.setAlignment(Qt.AlignCenter)

        bubble = self.create_message_bubble(text, is_user)
        timestamp = QLabel(datetime.now().strftime("%H:%M:%S"))
        timestamp.setStyleSheet("color: #888888; font-size: 12px;")

        # 使用 QVBoxLayout 将气泡和时间戳垂直排列
        bubble_layout = QVBoxLayout()
        bubble_layout.setSpacing(5)  # 气泡与时间戳之间的垂直间距
        bubble_layout.addWidget(bubble)
        bubble_layout.addWidget(timestamp, alignment=Qt.AlignRight if is_user else Qt.AlignLeft)

        # 将发送者标签与气泡水平排列
        if is_user:
            layout.addStretch()
            layout.addWidget(bubble)  # 气泡在左
            layout.addWidget(sender_label)  # 发送者标签在右
            layout.setContentsMargins(40, 0, 0, 0)
        else:
            layout.addWidget(sender_label)  # 发送者标签在左
            layout.addLayout(bubble_layout)  # 气泡在右
            layout.addStretch()
            layout.setContentsMargins(0, 0, 40, 0)

        self.chat_layout.insertWidget(self.chat_layout.count()-1, container)
        self.scroll_to_bottom()

    def scroll_to_bottom(self):
        """滚动到聊天底部"""
        scroll_bar = self.scroll_area.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())

    def call_deepseek_api(self, message):
        """调用 DeepSeek API"""
        try:
            response = self.client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V3",
                messages=[{"role": "user", "content": message}],
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"抱歉，AI 服务出错：{str(e)}"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = ChatDialog()
    dialog.show()
    sys.exit(app.exec())