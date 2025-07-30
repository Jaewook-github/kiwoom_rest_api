import os

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
import sys
import datetime
from multiprocessing import Process, Queue

from loguru import logger
import pandas as pd
from PyQt5.QtCore import Qt, QSettings, QTimer, QAbstractTableModel, QTime
from PyQt5.QtGui import QColor, QIcon, QFont
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QGridLayout, QGroupBox, QLabel,
                             QLineEdit, QPushButton, QComboBox, QSpinBox,
                             QDoubleSpinBox, QRadioButton, QCheckBox, QTimeEdit,
                             QTableView, QTabWidget, QSplitter, QFrame,
                             QSizePolicy, QHeaderView)

from tr_process_functions import tr_general_req_func, tr_order_req_func
from websocket_functions import run_websocket
from utils import log_exceptions


class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
            elif role == Qt.TextAlignmentRole:
                return Qt.AlignCenter
            if role == Qt.ForegroundRole:
                if self._data.columns[index.column()] in ("수익률(%)", "전일대비(%)"):
                    try:
                        value = self._data.iloc[index.row(), index.column()]
                        if isinstance(value, str) and "," in value:
                            value = int(value.replace(",", ""))
                        if float(value) < 0:
                            return QColor(Qt.blue)
                        elif float(value) > 0:
                            return QColor(Qt.red)
                    except:
                        return str(value)
        return None

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[section]
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return self._data.index[section]
        return None

    def setData(self, index, value, role):
        return False

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable


def format_number(text_edit):
    plain_number = text_edit.text().replace(',', '')
    try:
        formatted_number = f"{int(plain_number):,}"
    except ValueError:
        formatted_number = ''
    cursor_pos = text_edit.cursorPosition()
    text_edit.setText(formatted_number)
    text_edit.setCursorPosition(cursor_pos)


class KiwoomAPI(QMainWindow):
    def __init__(
            self,
            tr_req_queue=None,
            tr_result_queue=None,
            order_tr_req_queue=None,
            websocket_req_queue=None,
            websocket_result_queue=None,
    ):
        super().__init__()
        self.tr_req_queue = tr_req_queue
        self.tr_result_queue = tr_result_queue
        self.order_tr_req_queue = order_tr_req_queue
        self.websocket_req_queue = websocket_req_queue
        self.websocket_result_queue = websocket_result_queue

        self.settings = QSettings('MyAPP20250501', 'myApp20250501')

        # 데이터 초기화
        self.condition_df = pd.DataFrame(columns=["조건index", "조건명"])
        self.condition_name_to_index_dict = dict()
        self.condition_index_to_name_dict = dict()
        self.account_info_df = pd.DataFrame(columns=["종목명", "현재가", "매입가", "보유수량", "매매가능수량", "수익률(%)"])

        try:
            self.realtime_tracking_df = pd.read_pickle("realtime_tracking_df.pkl")
        except FileNotFoundError:
            self.realtime_tracking_df = pd.DataFrame(
                columns=["종목명", "현재가", "매입가", "수익률(%)", "트레일링 발동 여부", "트레일링 발동 후 고가", "매수주문여부", "매도주문여부"]
            )

        self.last_saved_realtime_tracking_df = self.realtime_tracking_df.copy(deep=True)
        self.stock_code_to_basic_info_dict = dict()
        self.order_info_df = pd.DataFrame(columns=["주문접수시간", "종목코드", "주문수량", "매수매도구분"])
        self.realtime_registered_codes_set = set()
        self.amend_ordered_num_set = set()

        self.transaction_cost = 0.18
        self.current_realtime_count = 0
        self.max_realtime_count = 95
        self.is_no_transaction = True
        self.has_init = False

        self.init_ui()
        self.setup_timers()
        self.init_data()

    def init_ui(self):
        self.setWindowTitle("키움증권 자동매매 프로그램")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)

        # 메인 위젯 및 레이아웃
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 상단 컨트롤 패널
        control_panel = self.create_control_panel()
        main_layout.addWidget(control_panel)

        # 설정 패널 (스플리터로 분할)
        settings_splitter = QSplitter(Qt.Horizontal)

        # 매수 설정
        buy_settings = self.create_buy_settings()
        settings_splitter.addWidget(buy_settings)

        # 매도 설정
        sell_settings = self.create_sell_settings()
        settings_splitter.addWidget(sell_settings)

        settings_splitter.setSizes([400, 600])
        main_layout.addWidget(settings_splitter)

        # 데이터 테이블 영역
        table_widget = self.create_table_widget()
        main_layout.addWidget(table_widget)

        # 레이아웃 비율 설정
        main_layout.setStretchFactor(control_panel, 0)
        main_layout.setStretchFactor(settings_splitter, 0)
        main_layout.setStretchFactor(table_widget, 1)

    def create_control_panel(self):
        group = QGroupBox("제어 패널")
        layout = QGridLayout(group)

        # 자동매매 제어 버튼
        self.autoOnPushButton = QPushButton("자동매매 ON")
        self.autoOnPushButton.setStyleSheet(
            "QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 8px; }")
        self.autoOnPushButton.clicked.connect(self.auto_trade_on)

        self.autoOffPushButton = QPushButton("자동매매 OFF")
        self.autoOffPushButton.setStyleSheet(
            "QPushButton { background-color: #f44336; color: white; font-weight: bold; padding: 8px; }")
        self.autoOffPushButton.clicked.connect(self.auto_trade_off)

        self.savePushButton = QPushButton("설정 저장")
        self.savePushButton.setStyleSheet(
            "QPushButton { background-color: #2196F3; color: white; font-weight: bold; padding: 8px; }")
        self.savePushButton.clicked.connect(self.save_settings)

        # 자동매매 시간 설정
        time_label = QLabel("자동매매 시간:")
        self.marketStartTimeEdit = QTimeEdit()
        self.marketStartTimeEdit.setTime(QTime(9, 0, 0))
        self.marketStartTimeEdit.setDisplayFormat("HH:mm:ss")

        time_separator = QLabel("~")
        time_separator.setAlignment(Qt.AlignCenter)

        self.marketEndTimeEdit = QTimeEdit()
        self.marketEndTimeEdit.setTime(QTime(15, 30, 0))
        self.marketEndTimeEdit.setDisplayFormat("HH:mm:ss")

        # 미체결 관리
        amend_label = QLabel("미체결 관리:")
        self.amendOrderSpinBox = QSpinBox()
        self.amendOrderSpinBox.setRange(0, 999)
        self.amendOrderSpinBox.setValue(60)
        amend_desc = QLabel("초 이상 미체결 발생 시 시장가 정정 주문")

        # 최대 자동매매 종목 수
        max_count_label = QLabel("최대 자동매매 종목 수:")
        self.maxAutoTradeCountSpinBox = QSpinBox()
        self.maxAutoTradeCountSpinBox.setRange(0, 95)
        self.maxAutoTradeCountSpinBox.setValue(10)

        # 레이아웃 배치
        layout.addWidget(self.autoOnPushButton, 0, 0)
        layout.addWidget(self.autoOffPushButton, 0, 1)
        layout.addWidget(self.savePushButton, 0, 2)

        layout.addWidget(time_label, 1, 0)
        layout.addWidget(self.marketStartTimeEdit, 1, 1)
        layout.addWidget(time_separator, 1, 2)
        layout.addWidget(self.marketEndTimeEdit, 1, 3)

        layout.addWidget(amend_label, 2, 0)
        layout.addWidget(self.amendOrderSpinBox, 2, 1)
        layout.addWidget(amend_desc, 2, 2, 1, 2)

        layout.addWidget(max_count_label, 3, 0)
        layout.addWidget(self.maxAutoTradeCountSpinBox, 3, 1)

        return group

    def create_buy_settings(self):
        group = QGroupBox("매수 설정")
        layout = QVBoxLayout(group)

        # 매수 조건식
        condition_layout = QHBoxLayout()
        condition_layout.addWidget(QLabel("매수 조건식:"))
        self.buyConditionComboBox = QComboBox()
        self.buyConditionComboBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        condition_layout.addWidget(self.buyConditionComboBox)
        layout.addLayout(condition_layout)

        # 매수 금액
        amount_layout = QHBoxLayout()
        amount_layout.addWidget(QLabel("매수 금액:"))
        self.buyAmountLineEdit = QLineEdit("200,000")
        self.buyAmountLineEdit.setAlignment(Qt.AlignCenter)
        self.buyAmountLineEdit.textChanged.connect(lambda: format_number(self.buyAmountLineEdit))
        amount_layout.addWidget(self.buyAmountLineEdit)
        layout.addLayout(amount_layout)

        # 매수 주문 방식
        order_type_layout = QVBoxLayout()
        self.marketBuyRadioButton = QRadioButton("시장가 매수")
        self.marketBuyRadioButton.setChecked(True)
        order_type_layout.addWidget(self.marketBuyRadioButton)

        limit_layout = QHBoxLayout()
        self.limitBuyRadioButton = QRadioButton("현재가 대비")
        self.limitBuySpinBox = QSpinBox()
        self.limitBuySpinBox.setRange(-10, 10)
        self.limitBuySpinBox.setValue(0)
        limit_layout.addWidget(self.limitBuyRadioButton)
        limit_layout.addWidget(self.limitBuySpinBox)
        limit_layout.addWidget(QLabel("호가로 지정가 주문"))
        order_type_layout.addLayout(limit_layout)

        layout.addLayout(order_type_layout)

        return group

    def create_sell_settings(self):
        group = QGroupBox("매도 설정")
        layout = QVBoxLayout(group)

        # 매도 조건식
        condition_layout = QHBoxLayout()
        condition_layout.addWidget(QLabel("매도 조건식:"))
        self.sellConditionComboBox = QComboBox()
        self.sellConditionComboBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        condition_layout.addWidget(self.sellConditionComboBox)
        layout.addLayout(condition_layout)

        # 손절 설정
        stop_loss_layout = QHBoxLayout()
        self.stopLossCheckBox = QCheckBox("평균단가 대비 현재 수익률이")
        self.stopLossCheckBox.setChecked(True)
        self.stopLossDoubleSpinBox = QDoubleSpinBox()
        self.stopLossDoubleSpinBox.setRange(-99.0, 99.0)
        self.stopLossDoubleSpinBox.setValue(-2.0)
        self.stopLossDoubleSpinBox.setSingleStep(0.1)
        stop_loss_layout.addWidget(self.stopLossCheckBox)
        stop_loss_layout.addWidget(self.stopLossDoubleSpinBox)
        stop_loss_layout.addWidget(QLabel("% 이하로 내려가면 전량 매도 주문"))
        layout.addLayout(stop_loss_layout)

        # 트레일링 스탑 설정
        trailing_layout1 = QHBoxLayout()
        self.trailingStopCheckBox = QCheckBox("평균단가 대비 현재 수익률이")
        self.trailingStopCheckBox.setChecked(True)
        self.trailingStopDoubleSpinBox1 = QDoubleSpinBox()
        self.trailingStopDoubleSpinBox1.setRange(-99.0, 99.0)
        self.trailingStopDoubleSpinBox1.setValue(2.0)
        self.trailingStopDoubleSpinBox1.setSingleStep(0.1)
        trailing_layout1.addWidget(self.trailingStopCheckBox)
        trailing_layout1.addWidget(self.trailingStopDoubleSpinBox1)
        trailing_layout1.addWidget(QLabel("% 이상으로 올라가면 트레일링 발동"))
        layout.addLayout(trailing_layout1)

        trailing_layout2 = QHBoxLayout()
        trailing_layout2.addWidget(QLabel("      ↳ 트레일링 발동 이후 고가 대비 등락률(%)이"))
        self.trailingStopDoubleSpinBox2 = QDoubleSpinBox()
        self.trailingStopDoubleSpinBox2.setRange(-99.0, 99.0)
        self.trailingStopDoubleSpinBox2.setValue(-1.0)
        self.trailingStopDoubleSpinBox2.setSingleStep(0.1)
        trailing_layout2.addWidget(self.trailingStopDoubleSpinBox2)
        trailing_layout2.addWidget(QLabel("% 이하로 내려가면 전량 매도 주문"))
        layout.addLayout(trailing_layout2)

        # 매도 주문 방식
        sell_order_layout = QVBoxLayout()
        self.marketSellRadioButton = QRadioButton("시장가 매도")
        self.marketSellRadioButton.setChecked(True)
        sell_order_layout.addWidget(self.marketSellRadioButton)

        limit_sell_layout = QHBoxLayout()
        self.limitSellRadioButton = QRadioButton("현재가 대비")
        self.limitSellSpinBox = QSpinBox()
        self.limitSellSpinBox.setRange(-10, 10)
        self.limitSellSpinBox.setValue(0)
        limit_sell_layout.addWidget(self.limitSellRadioButton)
        limit_sell_layout.addWidget(self.limitSellSpinBox)
        limit_sell_layout.addWidget(QLabel("호가로 지정가 주문"))
        sell_order_layout.addLayout(limit_sell_layout)

        layout.addLayout(sell_order_layout)

        return group

    def create_table_widget(self):
        tab_widget = QTabWidget()

        # 계좌 현황 탭
        account_tab = QWidget()
        account_layout = QVBoxLayout(account_tab)
        self.accountInfoTableView = QTableView()
        self.accountInfoTableView.setEditTriggers(QTableView.NoEditTriggers)
        self.accountInfoTableView.setSortingEnabled(True)
        self.accountInfoTableView.horizontalHeader().setStretchLastSection(True)
        account_layout.addWidget(self.accountInfoTableView)
        tab_widget.addTab(account_tab, "계좌 현황")

        # 자동매매 현황 탭
        auto_trade_tab = QWidget()
        auto_trade_layout = QVBoxLayout(auto_trade_tab)

        # 종목 편출 컨트롤
        pop_layout = QHBoxLayout()
        pop_layout.addWidget(QLabel("종목코드:"))
        self.popStockCodeLineEdit = QLineEdit("005930")
        self.popStockCodeLineEdit.setAlignment(Qt.AlignCenter)
        self.popStockCodeLineEdit.setMaximumWidth(100)
        pop_layout.addWidget(self.popStockCodeLineEdit)

        self.popPushButton = QPushButton("리스트 편출")
        self.popPushButton.clicked.connect(self.pop_btn_clicked)
        pop_layout.addWidget(self.popPushButton)
        pop_layout.addStretch()
        auto_trade_layout.addLayout(pop_layout)

        # 자동매매 테이블
        self.autoTradeInfoTableView = QTableView()
        self.autoTradeInfoTableView.setEditTriggers(QTableView.NoEditTriggers)
        self.autoTradeInfoTableView.setSortingEnabled(True)
        self.autoTradeInfoTableView.horizontalHeader().setStretchLastSection(True)
        auto_trade_layout.addWidget(self.autoTradeInfoTableView)

        tab_widget.addTab(auto_trade_tab, "자동매매 현황")

        return tab_widget

    def setup_timers(self):
        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.receive_websocket_result)
        self.timer1.start(10)

        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.receive_tr_result)
        self.timer2.start(100)

        self.timer3 = QTimer()
        self.timer3.timeout.connect(self.update_pandas_models)
        self.timer3.start(1000)

        self.timer4 = QTimer()
        self.timer4.timeout.connect(self.save_pickle)
        self.timer4.start(5000)

        self.timer5 = QTimer()
        self.timer5.timeout.connect(self.check_amend_orders)
        self.timer5.start(1000)

        self.timer6 = QTimer()
        self.timer6.timeout.connect(self.check_valid_time)

    def init_data(self):
        self.init_time()
        self.load_settings()

        self.websocket_req_queue.put(dict(action_id="조건검색식리스트"))
        self.tr_req_queue.put(dict(action_id="계좌조회"))

    # 기존 메서드들은 그대로 유지
    @log_exceptions
    def check_valid_time(self):
        if not (self.market_start_time <= datetime.datetime.now() <= self.market_end_time):
            self.is_no_transaction = True
        else:
            self.is_no_transaction = False

    def check_amend_orders(self):
        self.timer5.stop()
        now_time = datetime.datetime.now()
        for order_num, row in self.order_info_df.copy(deep=True).iterrows():
            try:
                if order_num in self.amend_ordered_num_set:
                    self.order_info_df.drop(order_num, inplace=True)
                    continue
                주문접수시간 = row['주문접수시간']
                종목코드 = row['종목코드']
                주문수량 = row['주문수량']
                매수매도구분 = row['매수매도구분']
                if 종목코드 not in self.realtime_tracking_df.index:
                    continue
                basic_info_dict = self.stock_code_to_basic_info_dict.get(종목코드, None)
                if basic_info_dict is None:
                    logger.info(f"종목코드: {종목코드} 기본정보 부재!")
                    continue
                order_time = datetime.datetime.now().replace(
                    hour=int(주문접수시간[:-4]),
                    minute=int(주문접수시간[-4:-2]),
                    second=int(주문접수시간[-2:]),
                )
                if now_time > order_time and (now_time - order_time).seconds > self.amendOrderSpinBox.value():
                    logger.debug(f"종목코드: {종목코드}, 주문번호: {order_num} 정정 주문 진행!")
                    if 매수매도구분 == "매수":
                        주문가격 = basic_info_dict["상한가"]
                    elif 매수매도구분 == "매도":
                        주문가격 = basic_info_dict["하한가"]
                    else:
                        logger.info(f"매수매도구분: {매수매도구분} continue!")
                        continue
                    self.order_info_df.drop(order_num, inplace=True)
                    self.order_tr_req_queue.put(
                        dict(
                            action_id="정정주문",
                            종목코드=종목코드,
                            주문번호=order_num,
                            주문수량=주문수량,
                            주문가격=주문가격,
                        )
                    )
                    self.amend_ordered_num_set.add(order_num)
            except Exception as e:
                logger.exception(e)
        self.timer5.start(1000)

    def save_pickle(self):
        self.timer4.stop()
        try:
            are_equal = self.realtime_tracking_df.equals(self.last_saved_realtime_tracking_df)
            if not are_equal:
                self.realtime_tracking_df.to_pickle("realtime_tracking_df.pkl")
                self.last_saved_realtime_tracking_df = self.realtime_tracking_df.copy(deep=True)
                logger.info("Saved df!")
        except Exception as e:
            logger.exception(e)
        self.timer4.start(5000)

    @log_exceptions
    def pop_btn_clicked(self):
        target_code = self.popStockCodeLineEdit.text().replace(" ", "")
        self.realtime_tracking_df.drop(target_code, inplace=True)
        logger.info(f"종목코드: {target_code} drop")
        self.update_pandas_models()

    def update_pandas_models(self):
        self.timer3.stop()
        try:
            model = PandasModel(self.account_info_df)
            self.accountInfoTableView.setModel(model)
            self.accountInfoTableView.resizeColumnsToContents()

            model2 = PandasModel(self.realtime_tracking_df)
            self.autoTradeInfoTableView.setModel(model2)
            self.autoTradeInfoTableView.resizeColumnsToContents()
        except Exception as e:
            logger.exception(e)
        self.timer3.start(1000)

    @log_exceptions
    def auto_trade_on(self):
        self.autoOnPushButton.setEnabled(False)
        self.autoOffPushButton.setEnabled(True)
        self.websocket_req_queue.put(
            dict(
                action_id="조건검색실시간등록",
                조건index=self.condition_name_to_index_dict[self.buyConditionComboBox.currentText()],
            )
        )
        logger.info(f"조건명: {self.buyConditionComboBox.currentText()} 실시간 등록")
        self.websocket_req_queue.put(
            dict(
                action_id="조건검색실시간등록",
                조건index=self.condition_name_to_index_dict[self.sellConditionComboBox.currentText()],
            )
        )
        logger.info(f"조건명: {self.sellConditionComboBox.currentText()} 실시간 등록")
        self.is_no_transaction = False
        self.init_time()
        self.marketStartTimeEdit.setEnabled(False)
        self.marketEndTimeEdit.setEnabled(False)
        self.timer6.start(1000)

    def init_time(self):
        market_start_time = self.marketStartTimeEdit.dateTime()
        self.market_start_time = datetime.datetime.now().replace(
            hour=market_start_time.time().hour(),
            minute=market_start_time.time().minute(),
            second=market_start_time.time().second(),
        )
        market_end_time = self.marketEndTimeEdit.dateTime()
        self.market_end_time = datetime.datetime.now().replace(
            hour=market_end_time.time().hour(),
            minute=market_end_time.time().minute(),
            second=market_end_time.time().second(),
        )

    @log_exceptions
    def auto_trade_off(self):
        self.autoOnPushButton.setEnabled(True)
        self.autoOffPushButton.setEnabled(False)
        self.websocket_req_queue.put(
            dict(
                action_id="조건검색실시간해제",
                조건index=self.condition_name_to_index_dict[self.buyConditionComboBox.currentText()],
            )
        )
        logger.info(f"조건명: {self.buyConditionComboBox.currentText()} 실시간 등록 해제")
        self.websocket_req_queue.put(
            dict(
                action_id="조건검색실시간해제",
                조건index=self.condition_name_to_index_dict[self.sellConditionComboBox.currentText()],
            )
        )
        logger.info(f"조건명: {self.sellConditionComboBox.currentText()} 실시간 등록 해제")
        self.is_no_transaction = True
        self.marketStartTimeEdit.setEnabled(True)
        self.marketEndTimeEdit.setEnabled(True)
        self.timer6.stop()

    def register_realtime_info(self, stock_code):
        if stock_code not in self.realtime_registered_codes_set:
            self.realtime_registered_codes_set.add(stock_code)
            self.websocket_req_queue.put(
                dict(
                    action_id="실시간등록",
                    종목코드=stock_code,
                )
            )
            self.current_realtime_count += 1

    @log_exceptions
    def on_receive_account_info(self, data):
        df = data['df']
        if len(df) > 0:
            self.account_info_df = df[["종목코드", "종목명", "현재가", "매입가", "보유수량", "매매가능수량", "수익률(%)"]]
            self.account_info_df.set_index("종목코드", inplace=True)
            for stock_code, row in self.account_info_df.iterrows():
                self.register_realtime_info(stock_code)
                if self.stock_code_to_basic_info_dict.get(stock_code) is None:
                    self.tr_req_queue.put(
                        dict(
                            action_id="주식기본정보",
                            종목코드=stock_code,
                        )
                    )
                if stock_code in self.realtime_tracking_df.index:
                    self.realtime_tracking_df.at[stock_code, "매입가"] = row["매입가"]
                    self.realtime_tracking_df.at[stock_code, "현재가"] = row["현재가"]
                    self.realtime_tracking_df.at[stock_code, "수익률(%)"] = row["수익률(%)"]
        if not self.has_init:
            for stock_code, row in self.realtime_tracking_df.copy(deep=True).iterrows():
                if stock_code not in self.account_info_df.index:
                    self.realtime_tracking_df.drop(stock_code, inplace=True)
                    logger.debug(f"종목코드: {stock_code}, 실시간 트래킹 리스트에서 drop!")
        self.update_pandas_models()
        self.has_init = True

    def receive_tr_result(self):
        self.timer2.stop()
        try:
            if not self.tr_result_queue.empty():
                data = self.tr_result_queue.get()
                if data['action_id'] == "계좌조회":
                    self.on_receive_account_info(data)
                elif data['action_id'] == "주식기본정보":
                    basic_info_dict = data['basic_info_dict']
                    종목코드 = data['종목코드']
                    self.stock_code_to_basic_info_dict[종목코드] = basic_info_dict
                    if 종목코드 in self.realtime_tracking_df.index and self.realtime_tracking_df.at[
                        종목코드, "매수주문여부"] == False:
                        logger.info(f"종목코드: {종목코드} 매수주문 진행!")
                        현재가 = basic_info_dict["현재가"]
                        self.realtime_tracking_df.at[종목코드, "종목명"] = basic_info_dict["종목명"]
                        self.realtime_tracking_df.at[종목코드, "현재가"] = 현재가
                        self.realtime_tracking_df.at[종목코드, "매수주문여부"] = True
                        시장가여부 = self.marketBuyRadioButton.isChecked()
                        주문가격 = ''
                        if not 시장가여부:
                            틱단위 = self.get_tick_size(현재가)
                            주문가격 = self.get_order_price(현재가 + self.limitBuySpinBox.value() * 틱단위)
                        주문금액 = int(self.buyAmountLineEdit.text().replace(",", ""))
                        주문수량 = int(주문금액 // 주문가격) if 주문가격 != '' else int(주문금액 // 현재가)
                        if 주문수량 <= 0:
                            logger.debug(f"종목코드: {종목코드}, 주문수량: {주문수량}")
                            self.timer2.start(100)
                            return
                        logger.debug(f"종목코드: {종목코드}, 현재가: {현재가}, 주문가격: {주문가격}")
                        self.order_tr_req_queue.put(
                            dict(
                                action_id="매수주문",
                                종목코드=종목코드,
                                주문수량=주문수량,
                                주문가격=주문가격,
                                시장가여부=시장가여부,
                            )
                        )
                elif data['action_id'] == "":
                    pass
        except Exception as e:
            logger.exception(e)
        self.timer2.start(100)

    @staticmethod
    def get_order_price(now_price):
        now_price = int(now_price)
        if now_price < 2000:
            return now_price
        elif 5000 > now_price >= 2000:
            return now_price - now_price % 5
        elif now_price >= 5000 and now_price < 20000:
            return now_price - now_price % 10
        elif now_price >= 20000 and now_price < 50000:
            return now_price - now_price % 50
        elif now_price >= 50000 and now_price < 200000:
            return now_price - now_price % 100
        elif now_price >= 200000 and now_price < 500000:
            return now_price - now_price % 500
        else:
            return now_price - now_price % 1000

    @staticmethod
    def get_tick_size(now_price):
        now_price = int(now_price)
        if now_price < 2000:
            return 1
        elif 5000 > now_price >= 2000:
            return 5
        elif now_price >= 5000 and now_price < 20000:
            return 10
        elif now_price >= 20000 and now_price < 50000:
            return 50
        elif now_price >= 50000 and now_price < 200000:
            return 100
        elif now_price >= 200000 and now_price < 500000:
            return 500
        else:
            return 1000

    def on_receive_order_result(self, data):
        종목코드 = data['종목코드']
        주문상태 = data['주문상태']
        단위체결가 = data['단위체결가']
        단위체결량 = data['단위체결량']
        주문수량 = data['주문수량']
        미체결수량 = data['미체결수량']
        종목명 = data['종목명']
        주문및체결시간 = data['주문및체결시간']
        주문번호 = data['주문번호']
        주문구분 = data['주문구분']

        if 주문상태 == "접수" and 종목코드 in self.realtime_tracking_df.index:
            self.order_info_df.loc[주문번호] = {
                "주문접수시간": 주문및체결시간, "종목코드": 종목코드, "주문수량": 주문수량, "매수매도구분": 주문구분,
            }

        if 주문상태 == "체결" and 미체결수량 == 0 and 주문번호 in self.order_info_df.index:
            logger.debug(f"주문번호: {주문번호} 체결완료!")
            self.order_info_df.drop(주문번호, inplace=True)

        if 주문상태 == "체결" and data['주문구분'] in ("매수", "매수정정"):
            if 종목코드 in self.account_info_df.index:
                보유수량 = self.account_info_df.at[종목코드, "보유수량"]
                매입가 = self.account_info_df.at[종목코드, "매입가"]
                new_매입가 = round((매입가 * 보유수량 + 단위체결가 * 단위체결량) / (보유수량 + 단위체결량), 1)
                self.account_info_df.at[종목코드, "보유수량"] = 보유수량 + 단위체결량
                self.account_info_df.at[종목코드, "매매가능수량"] += 단위체결량
                self.account_info_df.at[종목코드, "매입가"] = new_매입가
                if 종목코드 in self.realtime_tracking_df.index:
                    self.realtime_tracking_df.at[종목코드, "매입가"] = new_매입가
            else:
                self.account_info_df.loc[종목코드] = {
                    "종목명": 종목명,
                    "현재가": 단위체결가,
                    "매입가": 단위체결가,
                    "보유수량": 단위체결량,
                    "매매가능수량": 단위체결량,
                    "수익률(%)": -self.transaction_cost,
                }
                if 종목코드 in self.realtime_tracking_df.index:
                    self.realtime_tracking_df.at[종목코드, "매입가"] = 단위체결가
                    self.realtime_tracking_df.at[종목코드, "수익률(%)"] = -self.transaction_cost
        elif 주문상태 == "체결" and data['주문구분'] in ("매도", "매도정정"):
            if 종목코드 in self.account_info_df.index:
                self.account_info_df.at[종목코드, "보유수량"] -= 단위체결량
                self.account_info_df.at[종목코드, "매매가능수량"] -= 단위체결량
                보유수량 = self.account_info_df.at[종목코드, "보유수량"]
                if 보유수량 <= 0:
                    self.account_info_df.drop(종목코드, inplace=True)
                    if 종목코드 in self.realtime_tracking_df.index:
                        self.realtime_tracking_df.drop(종목코드, inplace=True)
                        logger.info(f"종목코드: {종목코드} 트래킹 리스트에서 drop!")
                        self.websocket_req_queue.put(
                            dict(
                                action_id="실시간해제",
                                종목코드=종목코드,
                            )
                        )
                        if 종목코드 in self.realtime_registered_codes_set:
                            self.realtime_registered_codes_set.remove(종목코드)
                        self.current_realtime_count -= 1

    def on_receive_condition_list(self, data):
        self.condition_df = data['df']
        self.condition_name_to_index_dict = dict(zip(self.condition_df["조건명"], self.condition_df["조건index"]))
        self.condition_index_to_name_dict = dict(zip(self.condition_df["조건index"], self.condition_df["조건명"]))
        self.buyConditionComboBox.addItems(self.condition_df["조건명"])
        self.sellConditionComboBox.addItems(self.condition_df["조건명"])
        self.load_settings(is_init=False)
        logger.info("조건검색식리스트 가져오기 성공!")

    @log_exceptions
    def on_receive_realtime_condition_event(self, data):
        조건식idx = data['조건식idx']
        종목코드 = data['종목코드']
        편입편출 = data['편입편출']

        if all([
            self.current_realtime_count < self.max_realtime_count,
            self.condition_name_to_index_dict[self.buyConditionComboBox.currentText()] == 조건식idx,
            편입편출 == "I",
            not self.is_no_transaction,
            len(self.realtime_tracking_df) < self.maxAutoTradeCountSpinBox.value(),
            종목코드 not in self.account_info_df.index,
            종목코드 not in self.realtime_tracking_df.index,
        ]):
            logger.debug(f"종목코드: {종목코드} 실시간등록 / 주식기본정보 요청 진행")
            self.register_realtime_info(종목코드)
            self.tr_req_queue.put(
                dict(
                    action_id="주식기본정보",
                    종목코드=종목코드,
                )
            )
            self.realtime_tracking_df.loc[종목코드] = {
                "종목명": None,
                "현재가": None,
                "매입가": None,
                "수익률(%)": None,
                "트레일링 발동 여부": False,
                "트레일링 발동 후 고가": None,
                "매수주문여부": False,
                "매도주문여부": False,
            }

        if all([
            종목코드 in self.realtime_tracking_df.index and self.realtime_tracking_df.at[종목코드, "매수주문여부"] == True,
            종목코드 in self.realtime_tracking_df.index and self.realtime_tracking_df.at[종목코드, "매도주문여부"] == False,
            self.condition_name_to_index_dict[self.sellConditionComboBox.currentText()] == 조건식idx,
            편입편출 == "I",
            not self.is_no_transaction,
        ]):
            logger.info(f"종목코드: {종목코드} 조건식 기반 매도!")
            self.sell_order(종목코드)

    def sell_order(self, 종목코드):
        if 종목코드 not in self.account_info_df.index:
            logger.info(f"종목코드: {종목코드} is not in account info!")
            return
        self.realtime_tracking_df.at[종목코드, "매도주문여부"] = True
        logger.debug(f"종목코드: {종목코드} 매도 진행")
        시장가여부 = self.marketSellRadioButton.isChecked()
        주문가격 = ''
        주문수량 = self.account_info_df.at[종목코드, "매매가능수량"]
        현재가 = self.account_info_df.at[종목코드, "현재가"]
        if not 시장가여부:
            틱단위 = self.get_tick_size(현재가)
            주문가격 = self.get_order_price(현재가 + self.limitSellSpinBox.value() * 틱단위)
        self.order_tr_req_queue.put(
            dict(
                action_id="매도주문",
                종목코드=종목코드,
                주문수량=주문수량,
                주문가격=주문가격,
                시장가여부=시장가여부,
            )
        )

    def on_receive_realtime_tick(self, data):
        종목코드 = data['종목코드']
        현재가 = data['현재가']
        if 종목코드 in self.account_info_df.index:
            self.account_info_df.at[종목코드, "현재가"] = 현재가
            매입가 = self.account_info_df.at[종목코드, "매입가"]
            수익률 = round((현재가 - 매입가) / 매입가 * 100 - self.transaction_cost, 2)
            self.account_info_df.at[종목코드, "수익률(%)"] = 수익률
            if 종목코드 in self.realtime_tracking_df.index:
                self.on_realtime_tracking_df_update(종목코드, 현재가, 수익률)

    def on_realtime_tracking_df_update(self, 종목코드, 현재가, 수익률):
        self.realtime_tracking_df.at[종목코드, "현재가"] = 현재가
        self.realtime_tracking_df.at[종목코드, "수익률(%)"] = 수익률
        if self.is_no_transaction:
            return
        매도주문여부 = self.realtime_tracking_df.at[종목코드, "매도주문여부"]
        트레일링발동여부 = self.realtime_tracking_df.at[종목코드, "트레일링 발동 여부"]
        트레일링발동후고가 = self.realtime_tracking_df.at[종목코드, "트레일링 발동 후 고가"]
        if 트레일링발동여부 and not pd.isnull(트레일링발동후고가):
            트레일링발동후고가 = max(트레일링발동후고가, 현재가)
            self.realtime_tracking_df.at[종목코드, "트레일링 발동 후 고가"] = 트레일링발동후고가
        if 매도주문여부 == False and self.stopLossCheckBox.isChecked() and 수익률 < self.stopLossDoubleSpinBox.value():
            logger.info(f"종목코드: {종목코드} 수익률: {수익률: .4f} < {self.stopLossDoubleSpinBox.value()}으로 스탑로스 발동!")
            self.sell_order(종목코드)
        if all([
            트레일링발동여부 == False,
            매도주문여부 == False,
            self.trailingStopCheckBox.isChecked(),
            수익률 >= self.trailingStopDoubleSpinBox1.value(),
        ]):
            logger.info(f"종목코드: {종목코드} 수익률: {수익률: .4f} >= {self.trailingStopDoubleSpinBox1.value()}으로 트레일링 스탑 발동!")
            self.realtime_tracking_df.at[종목코드, "트레일링 발동 후 고가"] = 현재가
            self.realtime_tracking_df.at[종목코드, "트레일링 발동 여부"] = True

        if all([
            트레일링발동여부 == True,
            매도주문여부 == False,
            not pd.isnull(트레일링발동후고가) and (현재가 - 트레일링발동후고가) / 트레일링발동후고가 * 100 < self.trailingStopDoubleSpinBox2.value(),
        ]):
            logger.info(f"종목코드: {종목코드} 고가대비 하락률(%): {(현재가 - 트레일링발동후고가) / 트레일링발동후고가 * 100: .4f}으로 트레일링 스탑 주문 발동!")
            self.sell_order(종목코드)

    def receive_websocket_result(self):
        self.timer1.stop()
        try:
            if not self.websocket_result_queue.empty():
                data = self.websocket_result_queue.get()
                if data['action_id'] == "실시간체결":
                    self.on_receive_realtime_tick(data)
                elif data['action_id'] == "조건검색식리스트":
                    self.on_receive_condition_list(data)
                elif data['action_id'] == "조건식실시간편입편출":
                    self.on_receive_realtime_condition_event(data)
                elif data['action_id'] == "주문접수및체결":
                    self.on_receive_order_result(data)
        except Exception as e:
            logger.exception(e)
        self.timer1.start(10)

    @log_exceptions
    def load_settings(self, is_init=True):
        self.buyAmountLineEdit.setText(self.settings.value('buyAmountLineEdit', defaultValue="200,000", type=str))
        self.marketBuyRadioButton.setChecked(self.settings.value('marketBuyRadioButton', defaultValue=True, type=bool))
        self.limitBuyRadioButton.setChecked(self.settings.value('limitBuyRadioButton', defaultValue=False, type=bool))
        self.marketSellRadioButton.setChecked(
            self.settings.value('marketSellRadioButton', defaultValue=True, type=bool))
        self.limitSellRadioButton.setChecked(self.settings.value('limitSellRadioButton', defaultValue=False, type=bool))
        self.stopLossCheckBox.setChecked(self.settings.value('stopLossCheckBox', defaultValue=True, type=bool))
        self.trailingStopCheckBox.setChecked(self.settings.value('trailingStopCheckBox', defaultValue=True, type=bool))
        self.limitBuySpinBox.setValue(self.settings.value("limitBuySpinBox", 0, int))
        self.amendOrderSpinBox.setValue(self.settings.value("amendOrderSpinBox", 60, int))
        self.maxAutoTradeCountSpinBox.setValue(self.settings.value("maxAutoTradeCountSpinBox", 10, int))
        self.limitSellSpinBox.setValue(self.settings.value("limitSellSpinBox", 0, int))
        self.stopLossDoubleSpinBox.setValue(self.settings.value("stopLossDoubleSpinBox", -2.0, float))
        self.trailingStopDoubleSpinBox1.setValue(self.settings.value("trailingStopDoubleSpinBox1", 2.0, float))
        self.trailingStopDoubleSpinBox2.setValue(self.settings.value("trailingStopDoubleSpinBox2", -1.0, float))
        if not is_init:
            self.buyConditionComboBox.setCurrentIndex(self.settings.value('buyConditionComboBox', 0, type=int))
            self.sellConditionComboBox.setCurrentIndex(self.settings.value('sellConditionComboBox', 0, type=int))
        self.marketStartTimeEdit.setTime(
            QTime.fromString(self.settings.value('marketStartTimeEdit', "090000"), "HHmmss"))
        self.marketEndTimeEdit.setTime(QTime.fromString(self.settings.value('marketEndTimeEdit', "153000"), "HHmmss"))

    @log_exceptions
    def save_settings(self):
        self.settings.setValue('buyAmountLineEdit', self.buyAmountLineEdit.text())
        self.settings.setValue('buyConditionComboBox', self.buyConditionComboBox.currentIndex())
        self.settings.setValue('sellConditionComboBox', self.sellConditionComboBox.currentIndex())
        self.settings.setValue('marketBuyRadioButton', self.marketBuyRadioButton.isChecked())
        self.settings.setValue('limitBuyRadioButton', self.limitBuyRadioButton.isChecked())
        self.settings.setValue('marketSellRadioButton', self.marketSellRadioButton.isChecked())
        self.settings.setValue('limitSellRadioButton', self.limitSellRadioButton.isChecked())
        self.settings.setValue('stopLossCheckBox', self.stopLossCheckBox.isChecked())
        self.settings.setValue('trailingStopCheckBox', self.trailingStopCheckBox.isChecked())
        self.settings.setValue("limitBuySpinBox", self.limitBuySpinBox.value())
        self.settings.setValue("amendOrderSpinBox", self.amendOrderSpinBox.value())
        self.settings.setValue("stopLossDoubleSpinBox", self.stopLossDoubleSpinBox.value())
        self.settings.setValue("trailingStopDoubleSpinBox1", self.trailingStopDoubleSpinBox1.value())
        self.settings.setValue("trailingStopDoubleSpinBox2", self.trailingStopDoubleSpinBox2.value())
        self.settings.setValue("limitSellSpinBox", self.limitSellSpinBox.value())
        self.settings.setValue("maxAutoTradeCountSpinBox", self.maxAutoTradeCountSpinBox.value())
        self.settings.setValue('marketStartTimeEdit', self.marketStartTimeEdit.time().toString("HHmmss"))
        self.settings.setValue('marketEndTimeEdit', self.marketEndTimeEdit.time().toString("HHmmss"))


sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    logger.debug(f"exctype: {exctype}, value: {value}, traceback: {traceback}")
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = my_exception_hook

if __name__ == "__main__":
    tr_req_queue = Queue()
    tr_result_queue = Queue()
    order_tr_req_queue = Queue()
    websocket_req_queue = Queue()
    websocket_result_queue = Queue()

    tr_gen_process = Process(
        target=tr_general_req_func,
        args=(tr_req_queue, tr_result_queue),
        daemon=True,
    )
    tr_order_process = Process(
        target=tr_order_req_func,
        args=(order_tr_req_queue,),
        daemon=True,
    )
    tr_websocket_process = Process(
        target=run_websocket,
        args=(websocket_req_queue, websocket_result_queue),
        daemon=True,
    )

    tr_gen_process.start()
    tr_order_process.start()
    tr_websocket_process.start()

    app = QApplication(sys.argv)
    kiwoom_api = KiwoomAPI(
        tr_req_queue=tr_req_queue,
        tr_result_queue=tr_result_queue,
        order_tr_req_queue=order_tr_req_queue,
        websocket_req_queue=websocket_req_queue,
        websocket_result_queue=websocket_result_queue,
    )
    kiwoom_api.show()
    sys.exit(app.exec_())