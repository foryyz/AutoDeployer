# Form implementation generated from reading ui file 'Btn.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


import sys
from enum import Enum

from PyQt6 import QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget

from Util import install_env, uninstall_env


class BtnType(Enum):
    DOWNLOAD = "下载"
    DELETE = "删除"


class BtnIcon(Enum):
    DOWNLOAD = "../static/Icon/下载.png"
    DELETE = "../static/Icon/删除.png"


class Btn(QWidget):

    # 定义下载方法
    def download(self):
        install_env(self.env_path)

    # 定义删除方法
    def delete(self):
        uninstall_env(self.env_path)

    def __init__(self, icon, type, text, env_path):
        super().__init__()
        self.pushButton = QtWidgets.QPushButton(self)
        self.type = type
        self.env_path = env_path
        self.pushButton.setText(text)
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(icon), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton.setIcon(self.icon)

        if self.type == BtnType.DOWNLOAD.value:
            self.pushButton.clicked.connect(self.download)
        elif self.type == BtnType.DELETE.value:
            self.pushButton.clicked.connect(self.delete)

        # 判断是下载还是删除
        if self.type == "下载":
            # 设置按钮样式 背景颜色为白色 字体颜色为黑色
            self.pushButton.setStyleSheet("""
                        QPushButton {
                            background-color: #FFFFFF;
                            color: black;
                            border: 1px solid #0056b3;
                            border-radius: 5px;
                            padding: 5px 10px;    
                            }    
                        QPushButton:hover {
                            background-color: #00FF7F;
                            }
                        """)
        elif self.type == "删除":
            self.pushButton.setStyleSheet("""
                        QPushButton {
                            background-color: #FFFFFF;
                            color: black;
                            border: 1px solid #0056b3;
                            border-radius: 5px;
                            padding: 5px 10px;    
                            }    
                        QPushButton:hover {
                            background-color: #FF6A6A;
                            }
                        """)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    btn = Btn("../static/Icon/下载", BtnType.DOWNLOAD.value, BtnType.DOWNLOAD.value, "../path")
    btn.show()
    sys.exit(app.exec())
