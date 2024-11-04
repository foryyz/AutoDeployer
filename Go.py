import sys

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QGridLayout, QMainWindow, QScrollArea

from Util import get_env_can_be_install_list
from asse.Product import Product
from entity.ProductItem import ProductItem

n = 2


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AutoDeployer")
        self.setWindowIcon(QtGui.QIcon("./static/Icon/logo.png"))
        self.env_name = get_env_can_be_install_list()
        print(self.env_name)
        self.setFixedSize(728, 512)
        self.products = []
        # 创建主部件和布局
        main_widget = QWidget()
        main_widget.setObjectName("center_widget")

        # 垂直布局
        main_layout = QVBoxLayout(main_widget)
        main_layout.setObjectName("verticalLayout")

        first_line = QWidget()
        # 创建一个水平布局
        horizontalLayout = QtWidgets.QHBoxLayout(first_line)
        # 设置水平布局左上角对齐
        horizontalLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        # 创建一个label
        label = QtWidgets.QLabel()
        # 设置label的图片
        label.setPixmap(QtGui.QPixmap("./static/Icon/logo.png"))
        # 设置label的图片自适应
        label.setScaledContents(True)
        # 设置label的图片大小
        label.setFixedSize(50, 50)
        # 设置label的图片左对齐
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        horizontalLayout.addWidget(label)
        # 创建一个文本
        label_2 = QtWidgets.QLabel()
        label_2.setObjectName("AutoDeployer")
        label_2.setText("AutoDeployer")
        # 左对齐
        label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        label_2.setStyleSheet("font-size: 30px; font-weight: bold;")
        horizontalLayout.addWidget(label_2)

        # 添加水平布局到主布局
        main_layout.addWidget(first_line)

        # 创建一个网格布局
        slider_area = QWidget()
        slider_area.setObjectName("scrollArea")
        slider_layout = QGridLayout(slider_area)
        # 设置网格布局为左上角对齐
        slider_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        # 设置网格布局外边距
        slider_layout.setContentsMargins(20, 10, 10, 10)

        # 创建一些产品
        item1 = ProductItem("java", "./static/Icon/java.png", self.env_name[0], "下载")
        item2 = ProductItem("maven", "./static/Icon/Maven.png", self.env_name[1], "下载")

        # 添加一些标签到滑块区域，模拟内容超过窗口大小的情况
        self.products.append(Product(item1))
        self.products.append(Product(item2))

        # 将产品添加到网格区域中
        for i in range(n):
            slider_layout.addWidget(self.products[i].getWidget(), i // 5, i % 5)

        # 将滑块区域放入QScrollArea中
        scroll_area = QScrollArea()
        # 设置滑块样式
        scroll_area.setStyleSheet("""
           QScrollBar:vertical {
               width: 10px;
               background: #FFFFFF;
               margin: 0px 0px 0px 0px;
               border: 1px solid #CCCCCC;
           }
           QScrollBar::handle:vertical {
               background: #FF34B3;
           }
           QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
               height: 0px;   
           }     
           
        """)
        # 设置滑块区域为网格布局
        scroll_area.setWidget(slider_area)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(slider_area)

        # 将QScrollArea添加到主布局中
        main_layout.addWidget(scroll_area)

        # 设置中央部件为主部件
        self.setCentralWidget(main_widget)

        self.retranslateUi(self)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "AutoDeployer"))
        Form.setStyleSheet("""
           #center_widget {
               background-color: #104E8B;
               padding: 10px;
           }
           #AutoDeployer {
               color: #FFFFFF;
               font-size: 30px;
               font-weight: bold;
           }
           #scrollArea{
               background-color: #FFF5EE; 
           }
        """)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec())
