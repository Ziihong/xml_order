import pymysql
import pymysql.cursors
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import sys, datetime


class DB_Utils:

    def queryExecutor(self, sql, params):
        conn = pymysql.connect(host='localhost', user='guest', password='bemyguest', db='classicmodels', charset='utf8')

        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, params)
                rows = cursor.fetchall()
                return rows
        except Exception as e:
            print(e)
            print(type(e))
        finally:
            conn.close()

    def updateExecutor(self, sql, params):
        conn = pymysql.connect(host='localhost', user='guest', password='bemyguest', db='classicmodels', charset='utf8')

        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
            conn.commit()
        except Exception as e:
            print(e)
            print(type(e))
        finally:
            conn.close()


class DB_Queries:

    def selectCustomer(self):
        sql = "SELECT DISTINCT name FROM customers ORDER BY name"
        params = ()

        util = DB_Utils()
        rows = util.queryExecutor(sql=sql, params=params)
        return rows

    def selectCountry(self):
        sql = "SELECT DISTINCT country FROM customers ORDER BY country"
        params = ()

        util = DB_Utils()
        rows = util.queryExecutor(sql=sql, params=params)
        return rows

    def selectCity(self):
        sql = "SELECT DISTINCT city FROM customers ORDER BY city"
        params = ()

        util = DB_Utils()
        rows = util.queryExecutor(sql=sql, params=params)
        return rows

    # def selectUsingCustomer(self, value):
    #     if value == "없음":
    #         sql = "SELECT * FROM customers WHERE name IS NULL"
    #         params = ()
    #     else:
    #         sql = "SELECT * FROM customers WHERE name = %s"
    #         params = (value)
    #
    #     util = DB_Utils()
    #     rows = util.queryExecutor(sql=sql, params=params)
    #     return rows

    def selectUsingCountry(self, value):
        if value == "없음":
            sql = "SELECT orderNo, orderDate, requiredDate, shippedDate, status, name as customer, comments " \
                  "FROM orders JOIN customers USING(customerId) WHERE country IS NULL ORDER BY orderNo"
            params = ()
        else:
            sql = "SELECT orderNo, orderDate, requiredDate, shippedDate, status, name as customer, comments " \
                  "FROM orders JOIN customers USING(customerId) WHERE country = %s ORDER BY orderNo"
            params = (value)

        util = DB_Utils()
        rows = util.queryExecutor(sql=sql, params=params)
        return rows

    # def selectUsingCity(self, value):
    #     if value == "없음":
    #         sql = "SELECT * FROM customers WHERE city IS NULL"
    #         params = ()
    #     else:
    #         sql = "SELECT * FROM customers WHERE city = %s"
    #         params = (value)
    #
    #     util = DB_Utils()
    #     rows = util.queryExecutor(sql=sql, params=params)
    #     return rows

    def selectUsingOption(self, customer_value, country_value, city_value):

        print(customer_value, country_value, city_value)
        if customer_value == "ALL":
            customer_value = "IS NULL"
        if country_value == "ALL":
            country_value = "IS NULL"
        if city_value == "ALL":
            city_value = "IS NULL"

        sql = "SELECT * FROM customers WHERE customer = %s AND country = %s AND city = %s"
        params = (customer_value, country_value, city_value)

        util = DB_Utils()
        rows = util.queryExecutor(sql=sql, params=params)
        return rows


    def showAll(self):
        sql = "SELECT orderNo, orderDate, requiredDate, shippedDate, status, name as customer, comments " \
              "FROM orders JOIN customers USING(customerId) ORDER BY orderNo"
        params = ()

        util = DB_Utils()
        rows = util.queryExecutor(sql=sql, params=params)
        return rows

    def showDetail(self, value):

        sql = "SELECT orderLineNo, productCode, name as productName, quantity, priceEach, quantity*priceEach as 상품주문액 " \
              "FROM orderDetails od INNER JOIN orders o USING(orderNo) " \
              "INNER JOIN products p USING(productCode) " \
              "WHERE orderNo = %s ORDER BY orderLineNo"
        params = (str(value))

        # sql = "SELECT * FROM orderDetails OD CROSS JOIN orders O ON OD.orderNo = O.orderNo"
        # params = ()
        util = DB_Utils()
        rows = util.queryExecutor(sql=sql, params=params)
        return rows


# insert into orderDetails(orderNo, productCode, quantity, priceEach, orderLineNo) values
# insert into orders(orderNo, orderDate, requiredDate, shippedDate, status, comments, customerId) values
# insert into products(productCode, name, productLine, scale, vendor, description, quantityInStock, buyPrice, MSRP) values

class DetailWindow(QWidget):
    def __init__(self, orderNo):
        super().__init__()
        self.setupUI()
        self.drawTable(orderNo)
        self.show()
        print("init ", orderNo)

    def setupUI(self):

        # order_num
        self.orderNumLabel = QLabel("주문번호: ", self)
        # product_count
        self.productCountLabel = QLabel("상품개수: ", self)
        # product_price
        self.productPriceLabel = QLabel("주문액: ", self)

        # 주문 상세 내역
        self.detailLayout = QHBoxLayout()
        self.detailLayout.addWidget(self.orderNumLabel)
        self.detailLayout.addWidget(self.productCountLabel)
        self.detailLayout.addWidget(self.productPriceLabel)

        # 주문 상세 내역 QHBoxLayout -> QGroupBox
        self.detailGroupBox = QGroupBox("주문 상세 내역")
        self.detailGroupBox.setLayout(self.detailLayout)

        # QTableWidget
        self.tableWidget = QTableWidget(self)
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


    def drawTable(self, orderNo):

        query = DB_Queries()
        results = query.showDetail(orderNo)

        # 주문 상세 내역
        totalCount = len(results)
        totalPrice = 0
        for r in results:
            totalPrice += r["상품주문액"]
        self.setDetail(orderNo, totalCount, totalPrice)

        # 검색 결과 테이블
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(len(results))
        self.tableWidget.setColumnCount(len(results[0]))
        columnNames = list(results[0].keys())
        self.tableWidget.setHorizontalHeaderLabels(columnNames)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for rowIdx, result in enumerate(results):
            for colIdx, (k, v) in enumerate(result.items()):
                if v == None:
                    continue
                elif isinstance(v, datetime.date):
                    item = QTableWidgetItem(v.strftime("%Y-%m-%d"))
                else:
                    item = QTableWidgetItem(str(v))

                self.tableWidget.setItem(rowIdx, colIdx, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()


    def setDetail(self, orderNo, totalCount, totalPrice):
        self.orderNumLabel.setText("주문번호:  " + orderNo)
        self.productCountLabel.setText("상품개수:  " + str(totalCount) + "개")
        self.productPriceLabel.setText("주문액:  " + str(totalPrice))


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):

        # DB 검색문 실행
        query = DB_Queries()
        rowsCustomer = query.selectCustomer()
        rowsCountry = query.selectCountry()
        rowsCity = query.selectCity()

        colCustomer = list(rowsCustomer[0].keys())[0]
        itemsCustomer = ['없음' if row[colCustomer] == None else row[colCustomer] for row in rowsCustomer]

        colCountry = list(rowsCountry[0].keys())[0]
        itemsCountry = ['없음' if row[colCountry] == None else row[colCountry] for row in rowsCountry]

        colCity = list(rowsCity[0].keys())[0]
        itemsCity = ['없음' if row[colCity] == None else row[colCity] for row in rowsCity]


        self.customerValue = "NULL"
        self.countryValue = "NULL"
        self.cityValue = "NULL"


        # 주문 검색 - search
        # 콤보박스 설정
        self.customerLabel = QLabel("고객:")
        self.customerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.customerComboBox = QComboBox(self)
        self.customerComboBox.addItem("ALL")
        self.customerComboBox.addItems(itemsCustomer)
        self.customerComboBox.activated.connect(self.customerComboBox_Activated)

        self.countryLabel = QLabel("국가:")
        self.countryLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.countryComboBox = QComboBox(self)
        self.countryComboBox.addItem("ALL")
        self.countryComboBox.addItems(itemsCountry)
        self.countryComboBox.activated.connect(self.countryComboBox_Activated)

        self.cityLabel = QLabel("도시:")
        self.cityLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.cityComboBox = QComboBox(self)
        self.cityComboBox.addItem("ALL")
        self.cityComboBox.addItems(itemsCity)
        self.cityComboBox.activated.connect(self.cityComboBox_Activated)


        # 주문 검색 - result
        self.resultLabel = QLabel("검색된 주문의 개수: ")
        self.resultLabel.setAlignment(QtCore.Qt.AlignRight)


        # 푸쉬버튼
        self.searchButton = QPushButton("검색", self)
        self.searchButton.clicked.connect(self.searchButton_Clicked)
        self.initButton = QPushButton("초기화", self)
        self.initButton.clicked.connect(self.initButton_Clicked)


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
        self.tableWidget = QTableWidget()
        self.tableWidget.cellClicked.connect(self.tableCell_Clicked)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers) # 변경 불가능 옵션


        # 화면 전체 layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.groupBox)
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)


        # 테이블 초기화
        self.initTable()


    def customerComboBox_Activated(self):
        self.customerValue = self.customerComboBox.currentText()


    def countryComboBox_Activated(self):
        self.countryValue = self.countryComboBox.currentText()


    def cityComboBox_Activated(self):
        self.cityValue = self.cityComboBox.currentText()


    def initTable(self):
        self.initButton_Clicked()


    def drawTable(self, results):
        # 검색 결과 개수
        self.setResultCount(len(results))

        # 검색 결과 테이블
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(len(results))
        self.tableWidget.setColumnCount(len(results[0]))
        columnNames = list(results[0].keys())
        self.tableWidget.setHorizontalHeaderLabels(columnNames)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for rowIdx, result in enumerate(results):
            for colIdx, (k, v) in enumerate(result.items()):
                if v == None:
                    continue
                elif isinstance(v, datetime.date):
                    item = QTableWidgetItem(v.strftime("%Y-%m-%d"))
                else:
                    item = QTableWidgetItem(str(v))

                self.tableWidget.setItem(rowIdx, colIdx, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()


    def setResultCount(self, count):
        self.resultLabel.setText("검색된 주문의 개수:  " + str(count) + "개")


    # Click event
    def initButton_Clicked(self):
        self.customerComboBox.setCurrentText("ALL")
        self.countryComboBox.setCurrentText("ALL")
        self.cityComboBox.setCurrentText("ALL")

        query = DB_Queries()
        results = query.showAll()

        self.drawTable(results)


    def searchButton_Clicked(self):
        query = DB_Queries()
        # results = query.selectUsingOption(self.customerValue, self.countryValue, self.cityValue)
        results = query.selectUsingCountry(self.countryValue)

        self.drawTable(results)


    def tableCell_Clicked(self, row, col):
        # orderNo 선택
        orderNo = self.tableWidget.item(row, col).text()
        print(orderNo)

        # print(self.tableWidget.item(item).text())
        self.detailWindow = DetailWindow(orderNo)
        self.detailWindow.show()



def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

main()