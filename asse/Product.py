import sys

from PyQt6 import QtCore
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication

from entity.ProductItem import ProductItem


class Product(QWidget):

    def itemClicked(self, flag):
        if flag:
            # 设置中心组件样式
            self.center_widget.setStyleSheet("""
            QWidget#center_widget{
                background-color: #FFFFFF;
                border: 2px solid #90EE90;
            }
            """)

        else:
            self.center_widget.setStyleSheet("""
                        QWidget#center_widget{
                            background-color: #FFFFFF;
                            border: 1px solid #E0E0E0;
                        }
                        """)

    def setState(self, flag):
        if self.Item.nums % 2 == 0:
            self.itemClicked(True)
        else:
            self.itemClicked(False)
        self.Item.nums += 1

    def __init__(self, ProductItem):
        # 构造方法 封装product对象
        super().__init__()
        self.Item = ProductItem

        # 创建一个中心部件
        self.center_widget = QWidget(self)
        # 设置中心部件大小
        self.center_widget.setFixedSize(125, 120)
        self.center_widget.setObjectName("center_widget")
        # 设置中心部件样式
        self.center_widget.setStyleSheet("""
        QWidget#center_widget{
            background-color: #FFFFFF;
            border-radius: 10px;
            border: 1px solid #E0E0E0;
        }
        """)
        # 添加点击事件
        self.center_widget.mousePressEvent = self.setState

        # 创建一个垂直布局
        self.layout = QVBoxLayout(self.center_widget)

        # 创建图标
        self.icon_label = QLabel(self.center_widget)
        self.icon_label.setObjectName("icon_label")
        self.icon_label.setPixmap(QIcon(self.Item.icon_path).pixmap(30, 30))
        # 图标上边距为20
        self.icon_label.setStyleSheet("QLabel#icon_label{margin-top: 20px;}")
        # 图标居中
        self.icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # 图标添加到Listview 居中
        self.layout.addWidget(self.icon_label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        # 创建标题
        self.name_label = QLabel(self.Item.name, self.center_widget)
        self.name_label.setObjectName("name_label")
        # 标题添加到Listview
        self.layout.addWidget(self.name_label, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        # 按钮添加到Listview
        self.layout.addWidget(self.Item.btn.pushButton, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

    def getWidget(self):
        return self.center_widget


if __name__ == '__main__':
    app = QApplication(sys.argv)
    item = ProductItem("java", "../static/Icon/java.png", "java", "下载")
    product = Product(item)

    product.show()
    sys.exit(app.exec())
