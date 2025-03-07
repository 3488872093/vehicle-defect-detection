from PySide6.QtGui import QIcon, QColor
from PySide6.QtWidgets import (
    QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QMessageBox, QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt

# 导入数据库操作模块
from database.user_manager import UserManager, initialize_db


def center_widget(widget):
    """将 widget 居中显示"""
    screen_geometry = QApplication.primaryScreen().availableGeometry()
    x = (screen_geometry.width() - widget.width()) // 2
    y = (screen_geometry.height() - widget.height()) // 2
    widget.move(x, y)


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("登录")
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.drag_pos = None

        self.initUI()
        self.applyStyles()
        center_widget(self)

    @staticmethod
    def setup_database():
        """初始化数据库（确保 data 目录存在并创建数据表）"""
        initialize_db()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        self.container = QFrame()
        self.container.setObjectName("container")
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(30, 30, 30, 30)
        container_layout.setSpacing(20)

        self.title_label = QLabel("欢迎登录")
        self.title_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(self.title_label)

        # 用户名输入框
        username_frame = QFrame()
        username_frame.setObjectName("usernameFrame")
        username_layout = QHBoxLayout(username_frame)
        username_layout.setContentsMargins(0, 0, 0, 0)
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("请输入用户名")
        self.username_edit.setFixedHeight(40)
        username_layout.addWidget(self.username_edit)
        container_layout.addWidget(username_frame)

        # 密码输入框和眼睛按钮
        password_frame = QFrame()
        password_frame.setObjectName("passwordFrame")
        password_layout = QHBoxLayout(password_frame)
        password_layout.setContentsMargins(0, 0, 0, 0)
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("请输入密码")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setFixedHeight(40)

        self.eye_button = QPushButton()
        self.eye_button.setIcon(QIcon("images/newsize/eye-close.png"))
        self.eye_button.setCheckable(True)
        self.eye_button.setFixedSize(36, 36)
        self.eye_button.setStyleSheet("border: none; background: transparent;")
        self.eye_button.clicked.connect(self.toggle_password_visibility)

        password_layout.addWidget(self.password_edit)
        password_layout.addWidget(self.eye_button)
        container_layout.addWidget(password_frame)

        # 登录、注册和取消按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        self.login_button = QPushButton("登录")
        self.register_button = QPushButton("注册")
        self.cancel_button = QPushButton("取消")
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.register_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch(1)
        container_layout.addLayout(button_layout)

        main_layout.addWidget(self.container)

        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.container.setGraphicsEffect(shadow)

        # 信号绑定
        self.login_button.clicked.connect(self.check_login)
        self.register_button.clicked.connect(self.open_register)
        self.cancel_button.clicked.connect(self.reject)

    def applyStyles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: transparent;
            }
            #container {
                background-color: #ffffff;
                border-radius: 10px;
            }
            QLabel {
                font-family: "Microsoft YaHei", sans-serif;
                font-size: 22px;
                font-weight: bold;
                color: #4a90e2;
            }
            QFrame#usernameFrame, QFrame#passwordFrame {
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #fefefe;
            }
            QLineEdit {
                font-family: "Microsoft YaHei", sans-serif;
                font-size: 14px;
                color: #333333;
                border: none;
                background-color: transparent;
                padding: 8px 8px 13px 8px;
            }
            QPushButton {
                font-family: "Microsoft YaHei", sans-serif;
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
                background-color: #4a90e2;
                border: none;
                border-radius: 5px;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #357ab8;
            }
            QPushButton:pressed {
                background-color: #2d6391;
            }
        """)

    def check_login(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()

        if not username or not password:
            self.show_error("用户名和密码不能为空")
            return

        try:
            user_manager = UserManager()
            if user_manager.verify_user(username, password):
                user_manager.close()
                self.accept()
            else:
                user_manager.close()
                self.show_error("用户名或密码错误")
        except Exception as e:
            self.show_error(f"数据库连接失败: {str(e)}")

    def show_error(self, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("错误")
        msg_box.setText(message)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                font-size: 20px;
            }
        """)
        msg_box.exec()

    def toggle_password_visibility(self):
        if self.eye_button.isChecked():
            self.password_edit.setEchoMode(QLineEdit.Normal)
            self.eye_button.setIcon(QIcon("images/newsize/eye.png"))
        else:
            self.password_edit.setEchoMode(QLineEdit.Password)
            self.eye_button.setIcon(QIcon("images/newsize/eye-close.png"))

    def open_register(self):
        try:
            # 这里建议暂时不传 parent 或注释下面两行以排除层级影响
            reg_dialog = RegisterDialog()
            reg_dialog.raise_()
            reg_dialog.activateWindow()
            if reg_dialog.exec() == QDialog.Accepted:
                self.username_edit.setText(reg_dialog.username_edit.text())
                self.password_edit.setText(reg_dialog.password_edit.text())
        except Exception as e:
            print("open_register 异常:", e)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.check_login()
        else:
            super().keyPressEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.drag_pos:
            delta = event.globalPosition().toPoint() - self.drag_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.drag_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.drag_pos = None


class RegisterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("注册")
        self.setFixedSize(400, 360)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.drag_pos = None

        self.initUI()
        self.applyStyles()
        center_widget(self)

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        self.container = QFrame()
        self.container.setObjectName("container")
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(30, 30, 30, 30)
        container_layout.setSpacing(20)

        self.title_label = QLabel("注册新账号")
        self.title_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(self.title_label)

        # 用户名输入框
        username_frame = QFrame()
        username_frame.setObjectName("usernameFrame")
        username_layout = QHBoxLayout(username_frame)
        username_layout.setContentsMargins(0, 0, 0, 0)
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("请输入用户名")
        self.username_edit.setFixedHeight(40)
        username_layout.addWidget(self.username_edit)
        container_layout.addWidget(username_frame)

        # 密码输入框
        password_frame = QFrame()
        password_frame.setObjectName("passwordFrame")
        password_layout = QHBoxLayout(password_frame)
        password_layout.setContentsMargins(0, 0, 0, 0)
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("请输入密码")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setFixedHeight(40)

        self.eye_button_pwd = QPushButton()
        self.eye_button_pwd.setIcon(QIcon("images/newsize/eye-close.png"))
        self.eye_button_pwd.setCheckable(True)
        self.eye_button_pwd.setFixedSize(36, 36)
        self.eye_button_pwd.setStyleSheet("border: none; background: transparent;")
        self.eye_button_pwd.clicked.connect(
            lambda: self.toggle_password_visibility(self.password_edit, self.eye_button_pwd)
        )

        password_layout.addWidget(self.password_edit)
        password_layout.addWidget(self.eye_button_pwd)
        container_layout.addWidget(password_frame)

        # 确认密码输入框
        confirm_frame = QFrame()
        confirm_frame.setObjectName("passwordFrame")
        confirm_layout = QHBoxLayout(confirm_frame)
        confirm_layout.setContentsMargins(0, 0, 0, 0)
        self.confirm_edit = QLineEdit()
        self.confirm_edit.setPlaceholderText("请确认密码")
        self.confirm_edit.setEchoMode(QLineEdit.Password)
        self.confirm_edit.setFixedHeight(40)

        self.eye_button_confirm = QPushButton()
        self.eye_button_confirm.setIcon(QIcon("images/newsize/eye-close.png"))
        self.eye_button_confirm.setCheckable(True)
        self.eye_button_confirm.setFixedSize(36, 36)
        self.eye_button_confirm.setStyleSheet("border: none; background: transparent;")
        self.eye_button_confirm.clicked.connect(
            lambda: self.toggle_password_visibility(self.confirm_edit, self.eye_button_confirm)
        )

        confirm_layout.addWidget(self.confirm_edit)
        confirm_layout.addWidget(self.eye_button_confirm)
        container_layout.addWidget(confirm_frame)

        # 注册和取消按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        self.register_button = QPushButton("注册")
        self.cancel_button = QPushButton("取消")
        button_layout.addWidget(self.register_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch(1)
        container_layout.addLayout(button_layout)

        main_layout.addWidget(self.container)

        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.container.setGraphicsEffect(shadow)

        # 信号绑定
        self.register_button.clicked.connect(self.check_register)
        self.cancel_button.clicked.connect(self.reject)

    def toggle_password_visibility(self, edit, button):
        """切换密码可见性"""
        if button.isChecked():
            edit.setEchoMode(QLineEdit.Normal)
            button.setIcon(QIcon("images/newsize/eye.png"))
        else:
            edit.setEchoMode(QLineEdit.Password)
            button.setIcon(QIcon("images/newsize/eye-close.png"))

    def applyStyles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: transparent;
            }
            #container {
                background-color: #ffffff;
                border-radius: 10px;
            }
            QLabel {
                font-family: "Microsoft YaHei", sans-serif;
                font-size: 22px;
                font-weight: bold;
                color: #4a90e2;
            }
            QFrame#usernameFrame, QFrame#passwordFrame {
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #fefefe;
            }
            QLineEdit {
                font-family: "Microsoft YaHei", sans-serif;
                font-size: 14px;
                color: #333333;
                border: none;
                background-color: transparent;
                padding: 8px 8px 14px 8px;
            }
            QPushButton {
                font-family: "Microsoft YaHei", sans-serif;
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
                background-color: #4a90e2;
                border: none;
                border-radius: 5px;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #357ab8;
            }
            QPushButton:pressed {
                background-color: #2d6391;
            }
        """)

    def check_register(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        confirm = self.confirm_edit.text().strip()

        if not username or not password or not confirm:
            self.show_error("所有字段均不能为空")
            return
        if password != confirm:
            self.show_error("两次输入的密码不一致")
            return

        try:
            user_manager = UserManager()
            if user_manager.user_exists(username):
                user_manager.close()
                self.show_error("用户名已存在")
                return

            if user_manager.create_user(username, password):
                user_manager.close()
                success_box = QMessageBox(self)
                success_box.setIcon(QMessageBox.Information)
                success_box.setWindowTitle("注册成功")
                success_box.setText("注册成功，请登录")
                success_box.setStyleSheet("""
                    QMessageBox {
                        background-color: white;
                    }
                    QLabel {
                        font-size: 20px;
                    }    
                """)
                success_box.exec()
                self.accept()
            else:
                user_manager.close()
                self.show_error("注册失败，请重试")
        except Exception as e:
            self.show_error(f"数据库错误: {str(e)}")

    def show_error(self, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("错误")
        msg_box.setText(message)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                font-size: 20px;
            }
        """)
        msg_box.exec()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.drag_pos:
            delta = event.globalPosition().toPoint() - self.drag_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.drag_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.drag_pos = None
