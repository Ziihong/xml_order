# import pymysql
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import sys


class DetailWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.show()

    def setupUI(self):

        # order_num
        orderNumLabel = QLabel("주문번호: ", self)
        # product_count
        productCount = QLabel("상품개수: ", self)
        # product_price
        productPrice = QLabel("주문액: ", self)

        # 주문 상세 내역
        self.detailLayout = QHBoxLayout()
        self.detailLayout.addWidget(orderNumLabel)
        self.detailLayout.addWidget(productCount)
        self.detailLayout.addWidget(productPrice)

        # 주문 상세 내역 QHBoxLayout -> QGroupBox
        self.detailGroupBox = QGroupBox("주문 상세 내역")
        self.detailGroupBox.setLayout(self.detailLayout)

        # QTableWidget
        self.tableWidget = QTableWidget(100, 8)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers) # 변경 불가능


        # 파일 출력 radio button
        self.radioBtnCSV = QRadioButton("CSV", self)
        self.radioBtnCSV.setChecked(True)
        self.radioBtnJSON = QRadioButton("JSON", self)
        self.radioBtnXML = QRadioButton("XML", self)

        # 저장 button
        self.saveButton = QPushButton("저장", self)

        self.radioLayout = QHBoxLayout()
        self.radioLayout.addWidget(self.radioBtnCSV)
        self.radioLayout.addWidget(self.radioBtnJSON)
        self.radioLayout.addWidget(self.radioBtnXML)
        self.radioLayout.addWidget(self.saveButton)

        # 파일 출력 QHBoxLayout -> QGroupBox
        self.fileGroupBox = QGroupBox("파일 출력")
        self.fileGroupBox.setLayout(self.radioLayout)


        # 화면 전체 layout
        layout = QGridLayout()
        layout.addWidget(self.detailGroupBox)
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.fileGroupBox)


        self.setLayout(layout)



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):

        # 주문 검색 - search
        self.customerLabel = QLabel("고객:")
        self.customerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.customerComboBox = QComboBox(self)

        self.countryLabel = QLabel("국가:")
        self.countryLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.countryComboBox = QComboBox(self)

        self.cityLabel = QLabel("도시:")
        self.cityLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.cityComboBox = QComboBox(self)

        self.searchButton = QPushButton("검색", self)

        # 주문 검색 - result
        self.resultLabel = QLabel("검색된 주문의 개수: ")
        self.resultLabel.setAlignment(QtCore.Qt.AlignRight)
        self.initButton = QPushButton("초기화", self)

        # 주문 검색 QGridLayout
        searchLayout = QGridLayout()
        searchLayout.addWidget(self.customerLabel, 0, 0)
        searchLayout.addWidget(self.customerComboBox, 0, 1)
        searchLayout.addWidget(self.countryLabel, 0, 2)
        searchLayout.addWidget(self.countryComboBox, 0, 3)
        searchLayout.addWidget(self.cityLabel, 0, 4)
        searchLayout.addWidget(self.cityComboBox, 0, 5)
        searchLayout.addWidget(self.searchButton, 0, 6)
        searchLayout.addWidget(self.resultLabel, 1, 0)
        searchLayout.addWidget(self.initButton, 1, 6)

        # 주문 검색 QGridLayout -> QGropBox
        self.groupBox = QGroupBox("주문 검색")
        self.groupBox.setLayout(searchLayout)


        # QTableWidget
        self.tableWidget = QTableWidget(100, 8)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers) # 변경 불가능
        self.tableWidget.cellClicked.connect(self.tableCell_Clicked)


        # 화면 전체 layout
        layout = QVBoxLayout()
        layout.addWidget(self.groupBox)
        layout.addWidget(self.tableWidget)

        self.setLayout(layout)


    def tableCell_Clicked(self):
        self.detailWindow = DetailWindow()
        self.detailWindow.show()



def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

main()