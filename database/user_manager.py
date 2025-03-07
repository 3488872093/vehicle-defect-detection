import sqlite3
from pathlib import Path

# 数据库文件路径，位于项目根目录下的 data/users.db
DATABASE_PATH = Path(__file__).resolve().parent.parent / 'database' / 'users.db'

def initialize_db():
    """
    初始化数据库，创建 users 表（如果尚不存在）。
    """
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        ''')
        conn.commit()


class UserManager:
    def __init__(self):
        """
        初始化数据库连接。
        """
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.conn.row_factory = sqlite3.Row  # 支持按列名访问
        self.cursor = self.conn.cursor()

    print("Connecting to database at:", DATABASE_PATH)

    def verify_user(self, username, password):
        """
        验证用户名和密码是否正确
        :param username: 用户名
        :param password: 密码
        :return: 如果匹配返回 True，否则返回 False
        """
        self.cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
        return self.cursor.fetchone() is not None

    def user_exists(self, username):
        """
        检查指定的用户名是否已存在
        :param username: 用户名
        :return: 如果存在返回 True，否则返回 False
        """
        self.cursor.execute(
            "SELECT 1 FROM users WHERE username = ?",
            (username,)
        )
        return self.cursor.fetchone() is not None

    def create_user(self, username, password):
        """
        创建一个新用户
        :param username: 用户名
        :param password: 密码
        :return: 成功返回 True，失败返回 False（例如：用户名已存在）
        """
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # 用户名重复导致插入失败
            return False
        except Exception as e:
            # 开发时可考虑记录日志
            print("创建用户时发生错误:", e)
            return False

    def close(self):
        """
        关闭数据库连接
        """
        if self.conn:
            self.conn.close()

    def __del__(self):
        self.close()
