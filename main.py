import sys
import logging
import os
from pathlib import Path
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication, QDialog, QMessageBox, 
)


# 设置工作目录为脚本所在目录
os.chdir(Path(__file__).parent)

# 将 ui 目录添加到系统路径中
sys.path.append(str(Path.cwd() / "ui"))

# 禁用日志和标准输出
sys.stdout = open(os.devnull, 'w')
logging.disable(logging.CRITICAL)

from login.login import LoginDialog
from utils import glo
from yoloshow.Window import YOLOSHOWWindow as yoloshowWindow


if __name__ == '__main__':
    app = QApplication([])

    try:
        LoginDialog.setup_database()
    except Exception as e:
        QMessageBox.critical(None, "初始化错误", f"数据库初始化失败: {str(e)}")
        sys.exit(1)

    app.setWindowIcon(QIcon('images/logo-1.ico'))
    app.setStyleSheet("QFrame { border: none; }")
    
    login_dialog = LoginDialog()
    login_dialog.setWindowIcon(QIcon('images/logo-1.ico'))
    if login_dialog.exec() != QDialog.Accepted:
        sys.exit(0)

    yoloshow = yoloshowWindow()
    glo._init()
    glo.set_value('yoloshow', yoloshow)
    yoloshow_glo = glo.get_value('yoloshow')
    yoloshow_glo.show()
    
    sys.exit(app.exec())