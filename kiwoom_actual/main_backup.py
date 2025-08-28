import os
import sys
# 현재 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, 'utils'))
sys.path.append(os.path.join(current_dir, 'config'))
sys.path.append(os.path.join(current_dir, 'func'))

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
import sys
import datetime
import json
from multiprocessing import Process, Queue
from collections import defaultdict

# 로깅 시스템 임포트 (가장 먼저)
from utils.enhanced_logging import (log_trading, log_order, log_error, log_info, log_debug)

# 텔레그램 알림 시스템 임포트
from utils.telegram_notifier import initialize_telegram_notifier, get_telegram_notifier, send_telegram_alert
from config.config import TELEGRAM_CONFIG

# 데이터 매니저 임포트
from utils.data_manager import data_manager

import pandas as pd
from PyQt5.QtCore import Qt, QSettings, QTimer, QAbstractTableModel, QTime, QModelIndex
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QGridLayout, QGroupBox, QLabel,
                             QLineEdit, QPushButton, QComboBox, QSpinBox,
                             QDoubleSpinBox, QRadioButton, QCheckBox, QTimeEdit,
                             QTableView, QTabWidget, QSplitter, QSizePolicy, QDialog, QDialogButtonBox)
from func.tr_process_functions import tr_general_req_func, tr_order_req_func
from func.websocket_functions import run_websocket
from utils.utils import log_exceptions
from utils.data_manager import data_manager


class PandasModel(QAbstractTableModel):
    """PandasModel IndexError 수정"""

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
            if section < len(self._data.columns):
                return self._data.columns[section]
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            # IndexError 방지를 위한 범위 체크
            if section < len(self._data.index):
                return str(self._data.index[section])
            else:
                return str(section)  # 안전한 기본값 반환
        return None

    def setData(self, index, value, role):
        return False

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
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


class BuyConditionModel(QAbstractTableModel):
    """매수 조건식 테이블 모델 (수정됨)"""

    def __init__(self, data=None):
        super().__init__()
        if data is None:
            self._data = pd.DataFrame(columns=['조건명', '조건index', '시작시간', '종료시간', '활성화'])
        else:
            self._data = data

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._data.columns)

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                value = self._data.iloc[index.row(), index.column()]
                return str(value)
            elif role == Qt.TextAlignmentRole:
                return Qt.AlignCenter
            elif role == Qt.ForegroundRole:
                # 활성화 상태에 따른 색상 변경
                if self._data.columns[index.column()] == '활성화':
                    value = self._data.iloc[index.row(), index.column()]
                    if value == True:
                        return QColor(Qt.blue)
                    else:
                        return QColor(Qt.red)
        return None

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            headers = ['조건명', '조건index', '시작시간', '종료시간', '활성화']
            return headers[section]
        return None

    def flags(self, index):
        """셀 선택 가능하도록 플래그 설정"""
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def add_condition(self, condition_name, condition_index, start_time="09:00:00", end_time="15:30:00", active=True):
        """조건식 추가"""
        if condition_name not in self._data['조건명'].values:
            self.beginInsertRows(QModelIndex(), len(self._data), len(self._data))
            new_row = pd.DataFrame([{
                '조건명': condition_name,
                '조건index': condition_index,
                '시작시간': start_time,
                '종료시간': end_time,
                '활성화': active
            }])
            self._data = pd.concat([self._data, new_row], ignore_index=True)
            self.endInsertRows()
            return True
        return False

    def remove_condition(self, row):
        """조건식 삭제"""
        if 0 <= row < len(self._data):
            self.beginRemoveRows(QModelIndex(), row, row)
            self._data = self._data.drop(self._data.index[row]).reset_index(drop=True)
            self.endRemoveRows()
            return True
        return False

    def get_data(self):
        """데이터 반환"""
        return self._data.copy()

    def update_time(self, row, start_time, end_time):
        """시간 업데이트"""
        if 0 <= row < len(self._data):
            self._data.iloc[row, self._data.columns.get_loc('시작시간')] = start_time
            self._data.iloc[row, self._data.columns.get_loc('종료시간')] = end_time
            # 특정 셀 업데이트 신호
            start_index = self.index(row, self._data.columns.get_loc('시작시간'))
            end_index = self.index(row, self._data.columns.get_loc('종료시간'))
            self.dataChanged.emit(start_index, end_index)

    def toggle_active(self, row):
        """활성화 상태 토글"""
        if 0 <= row < len(self._data):
            current = self._data.iloc[row, self._data.columns.get_loc('활성화')]
            self._data.iloc[row, self._data.columns.get_loc('활성화')] = not current
            # 특정 셀 업데이트
            index = self.index(row, self._data.columns.get_loc('활성화'))
            self.dataChanged.emit(index, index)

    def get_condition_at_row(self, row):
        """특정 행의 조건식 정보 반환"""
        if 0 <= row < len(self._data):
            return self._data.iloc[row].to_dict()
        return None


class TimeSettingDialog(QDialog):
    """시간 설정 다이얼로그"""

    def __init__(self, current_start="09:00:00", current_end="15:30:00", parent=None):
        super().__init__(parent)
        self.setWindowTitle("자동매매 시간 설정")
        self.setModal(True)
        self.resize(300, 150)

        layout = QVBoxLayout(self)

        # 시작 시간
        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("시작 시간:"))
        self.start_time_edit = QTimeEdit()
        self.start_time_edit.setTime(QTime.fromString(current_start, "HH:mm:ss"))
        self.start_time_edit.setDisplayFormat("HH:mm:ss")
        start_layout.addWidget(self.start_time_edit)
        layout.addLayout(start_layout)

        # 종료 시간
        end_layout = QHBoxLayout()
        end_layout.addWidget(QLabel("종료 시간:"))
        self.end_time_edit = QTimeEdit()
        self.end_time_edit.setTime(QTime.fromString(current_end, "HH:mm:ss"))
        self.end_time_edit.setDisplayFormat("HH:mm:ss")
        end_layout.addWidget(self.end_time_edit)
        layout.addLayout(end_layout)

        # 버튼
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_times(self):
        """설정된 시간 반환"""
        start = self.start_time_edit.time().toString("HH:mm:ss")
        end = self.end_time_edit.time().toString("HH:mm:ss")
        return start, end


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
        log_info("KiwoomAPI 메인 클래스 초기화 시작")

        self.tr_req_queue = tr_req_queue
        self.tr_result_queue = tr_result_queue
        self.order_tr_req_queue = order_tr_req_queue
        self.websocket_req_queue = websocket_req_queue
        self.websocket_result_queue = websocket_result_queue

        self.settings = QSettings('MyAPP20250501', 'myApp20250501')

        # 기존 데이터 초기화
        self.condition_df = pd.DataFrame(columns=["조건index", "조건명"])
        self.condition_name_to_index_dict = dict()
        self.condition_index_to_name_dict = dict()
        self.account_info_df = pd.DataFrame(columns=["종목명", "현재가", "매입가", "보유수량", "매매가능수량", "수익률(%)"])

        # 매수 조건식 관리 모델 초기화 (UI 초기화 전에 생성)
        self.buy_condition_model = BuyConditionModel()

        # === 당일 매도 종목 관리 시스템 (64GB 메모리 활용) ===
        self.today_date = datetime.datetime.now().strftime("%Y%m%d")

        # 1. 초고속 체크용 (0.1ms)
        self.today_sold_stocks = set()

        # 2. 상세 정보 저장용 (실시간 분석 가능)
        self.today_sold_details = {}

        # 3. 완전한 기록용 DataFrame (통계/차트용)
        self.today_sold_df = pd.DataFrame(columns=[
            "종목코드", "종목명", "매도시간", "매수조건식", "매도사유",
            "매입가", "매도가", "수익률", "보유기간", "매도금액"
        ])

        # 4. 조건식별 통계 (패턴 분석용)
        self.condition_performance = defaultdict(list)

        # 5. 시간대별 매도 패턴 (시각화용)
        self.hourly_sell_pattern = defaultdict(int)

        # 6. 당일 매도 종목 파일 로드 시도
        self.load_today_sold_stocks()

        # 데이터 매니저를 통한 실시간 트래킹 데이터 로드
        self.realtime_tracking_df = data_manager.load_realtime_tracking_df()

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

        # 조건식별 거래 상태 관리 딕셔너리 초기화
        self.condition_trading_status = {}

        self.init_ui()
        self.setup_timers()
        self.init_data()
        self.init_telegram()

        log_info("KiwoomAPI 메인 클래스 초기화 완료")

    def load_today_sold_stocks(self):
        """당일 매도 종목 데이터 로드"""
        try:
            # 데이터 매니저를 통해 파일에서 로드
            self.today_sold_df = data_manager.load_today_sold_data(self.today_date)

            # set과 dict 재구성
            for _, row in self.today_sold_df.iterrows():
                종목코드 = row["종목코드"]
                self.today_sold_stocks.add(종목코드)
                self.today_sold_details[종목코드] = {
                    "매도시간": row["매도시간"],
                    "수익률": row["수익률"],
                    "매도사유": row["매도사유"],
                    "매수조건식": row["매수조건식"],
                    "매입가": row["매입가"],
                    "매도가": row["매도가"]
                }

                # 조건식별 성과 재구성
                condition_name = row["매수조건식"]
                self.condition_performance[condition_name].append({
                    "종목코드": 종목코드,
                    "수익률": row["수익률"],
                    "시간": row["매도시간"]
                })

                # 시간대별 패턴 재구성
                hour = row["매도시간"].hour
                self.hourly_sell_pattern[hour] += 1

            log_info(f"당일 매도 종목 데이터 로드 성공: {len(self.today_sold_df)}건")

        except FileNotFoundError:
            log_info("당일 매도 종목 데이터 없음 - 새로 시작")
        except Exception as e:
            log_error(f"당일 매도 종목 데이터 로드 실패: {str(e)}")

    def should_prevent_rebuy(self, 종목코드, condition_name):
        """고급 재매수 차단 로직"""
        if not self.preventSameDayRebuyCheckBox.isChecked():
            return False

        if 종목코드 not in self.today_sold_details:
            return False

        prev_trade = self.today_sold_details[종목코드]

        # 옵션 1: 손실 매도만 차단
        if hasattr(self, 'preventLossRebuyOnlyCheckBox') and self.preventLossRebuyOnlyCheckBox.isChecked():
            return prev_trade["수익률"] < 0

        # 옵션 2: 같은 조건식만 차단
        if hasattr(self, 'preventSameConditionOnlyCheckBox') and self.preventSameConditionOnlyCheckBox.isChecked():
            return prev_trade["매수조건식"] == condition_name

        # 옵션 3: 시간 간격 체크
        if hasattr(self, 'rebuyTimeoutSpinBox'):
            time_diff = (datetime.datetime.now() - prev_trade["매도시간"]).seconds
            if time_diff < self.rebuyTimeoutSpinBox.value() * 60:  # 분 단위
                return True

        return True  # 기본: 모든 당일 매도 종목 차단

    def update_realtime_statistics(self):
        """실시간 통계 업데이트"""
        if len(self.today_sold_df) > 0:
            총매도건수 = len(self.today_sold_df)
            평균수익률 = self.today_sold_df["수익률"].mean()
            수익건수 = len(self.today_sold_df[self.today_sold_df["수익률"] > 0])
            손실건수 = len(self.today_sold_df[self.today_sold_df["수익률"] < 0])
            승률 = (수익건수 / 총매도건수 * 100) if 총매도건수 > 0 else 0

            log_trading(f"당일 매도 통계 - 총 {총매도건수}건, "
                        f"평균수익률: {평균수익률:+.2f}%, "
                        f"승률: {승률:.1f}% ({수익건수}/{총매도건수})")

    def get_condition_performance_summary(self):
        """조건식별 성과 요약"""
        summary = {}
        for condition_name, trades in self.condition_performance.items():
            if trades:
                avg_profit = sum(t["수익률"] for t in trades) / len(trades)
                win_rate = sum(1 for t in trades if t["수익률"] > 0) / len(trades) * 100
                summary[condition_name] = {
                    "거래수": len(trades),
                    "평균수익률": avg_profit,
                    "승률": win_rate
                }
        return summary

    def save_comprehensive_report(self):
        """종합 리포트 저장 (프로그램 종료 시)"""
        try:
            today = self.today_date

            # 1. 매도 상세 기록 - 데이터 매니저 사용
            if len(self.today_sold_df) > 0:
                data_manager.save_today_sold_data(self.today_sold_df, today)

            # 2. 조건식별 성과 - 데이터 매니저 사용
            performance = self.get_condition_performance_summary()
            if performance:
                data_manager.save_condition_performance(performance, today)

            # 3. 시간대별 패턴 - 데이터 매니저 사용
            data_manager.save_hourly_pattern(self.hourly_sell_pattern, today)

            # 4. 백업 생성
            data_manager.create_daily_backup(today)

        except Exception as e:
            log_error(f"종합 리포트 저장 실패: {str(e)}")

    def init_telegram(self):
        """텔레그램 알림 시스템 초기화"""
        try:
            if TELEGRAM_CONFIG.get('enabled', False):
                bot_token = TELEGRAM_CONFIG.get('bot_token')
                chat_id = TELEGRAM_CONFIG.get('chat_id')

                if bot_token and bot_token != "YOUR_BOT_TOKEN_HERE" and chat_id and chat_id != "YOUR_CHAT_ID_HERE":
                    self.telegram_notifier = initialize_telegram_notifier(bot_token, chat_id, TELEGRAM_CONFIG)

                    # 연결 테스트
                    if self.telegram_notifier.test_connection():
                        log_info("텔레그램 알림 시스템 초기화 및 연결 테스트 성공")
                    else:
                        log_error("텔레그램 연결 테스트 실패")
                        self.telegram_notifier = None
                else:
                    log_info("텔레그램 봇 토큰 또는 채팅 ID가 설정되지 않음")
                    self.telegram_notifier = None
            else:
                log_info("텔레그램 알림이 비활성화됨")
                self.telegram_notifier = None
        except Exception as e:
            log_error(f"텔레그램 알림 시스템 초기화 실패: {str(e)}")
            self.telegram_notifier = None

    def init_ui(self):
        log_info("UI 초기화 시작")
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

        # 매수 조건식 테이블 설정
        self.setup_buy_condition_table()

        log_info("UI 초기화 완료")

    def setup_buy_condition_table(self):
        """매수 조건식 테이블 설정"""
        # 테이블 모델 설정
        self.buyConditionTableView.setModel(self.buy_condition_model)

        # 테이블 설정
        self.buyConditionTableView.setSelectionBehavior(QTableView.SelectRows)  # 행 단위 선택
        self.buyConditionTableView.setSelectionMode(QTableView.SingleSelection)  # 단일 선택
        self.buyConditionTableView.setAlternatingRowColors(True)  # 교대로 행 색상 변경

        # 헤더 설정
        header = self.buyConditionTableView.horizontalHeader()
        header.setStretchLastSection(True)
        header.resizeSection(0, 150)  # 조건명 열 너비
        header.resizeSection(1, 80)  # 조건index 열 너비
        header.resizeSection(2, 80)  # 시작시간 열 너비
        header.resizeSection(3, 80)  # 종료시간 열 너비
        header.resizeSection(4, 60)  # 활성화 열 너비

        # 더블클릭 이벤트 연결
        self.buyConditionTableView.doubleClicked.connect(self.edit_condition_time)

        # 우클릭 메뉴 추가 (선택사항)
        self.buyConditionTableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.buyConditionTableView.customContextMenuRequested.connect(self.show_condition_context_menu)

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

        # 매수 조건식 리스트 (다중 선택 가능)
        condition_label = QLabel("매수 조건식 목록:")
        layout.addWidget(condition_label)

        # 조건식 추가/삭제 컨트롤
        condition_control_layout = QHBoxLayout()
        self.buyConditionComboBox = QComboBox()
        self.buyConditionComboBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        condition_control_layout.addWidget(self.buyConditionComboBox)

        self.addConditionButton = QPushButton("조건식 추가")
        self.addConditionButton.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 5px; }")
        self.addConditionButton.clicked.connect(self.add_buy_condition)
        condition_control_layout.addWidget(self.addConditionButton)

        layout.addLayout(condition_control_layout)

        # 선택된 조건식 목록 테이블
        self.buyConditionTableView = QTableView()
        self.buyConditionTableView.setEditTriggers(QTableView.NoEditTriggers)
        self.buyConditionTableView.setMaximumHeight(200)
        layout.addWidget(self.buyConditionTableView)

        # 조건식 삭제 버튼
        remove_button_layout = QHBoxLayout()
        self.removeConditionButton = QPushButton("선택된 조건식 삭제")
        self.removeConditionButton.setStyleSheet(
            "QPushButton { background-color: #f44336; color: white; padding: 5px; }")
        self.removeConditionButton.clicked.connect(self.remove_buy_condition)
        remove_button_layout.addWidget(self.removeConditionButton)
        remove_button_layout.addStretch()
        layout.addLayout(remove_button_layout)

        # === 당일 매도 종목 재매수 방지 설정 ===
        rebuy_group = QGroupBox("재매수 방지 설정")
        rebuy_layout = QVBoxLayout(rebuy_group)

        # 기본 재매수 방지 체크박스
        self.preventSameDayRebuyCheckBox = QCheckBox("당일 매도 종목 재매수 방지")
        self.preventSameDayRebuyCheckBox.setChecked(True)
        self.preventSameDayRebuyCheckBox.setStyleSheet("QCheckBox { font-weight: bold; color: #d32f2f; }")
        rebuy_layout.addWidget(self.preventSameDayRebuyCheckBox)

        # 고급 옵션들
        advanced_layout = QVBoxLayout()

        # 손실 매도만 차단
        self.preventLossRebuyOnlyCheckBox = QCheckBox("손실 매도 종목만 재매수 방지")
        self.preventLossRebuyOnlyCheckBox.setToolTip("수익으로 매도한 종목은 재매수 허용")
        advanced_layout.addWidget(self.preventLossRebuyOnlyCheckBox)

        # 같은 조건식만 차단
        self.preventSameConditionOnlyCheckBox = QCheckBox("같은 조건식으로만 재매수 방지")
        self.preventSameConditionOnlyCheckBox.setToolTip("다른 조건식으로는 재매수 허용")
        advanced_layout.addWidget(self.preventSameConditionOnlyCheckBox)

        # 시간 간격 설정
        timeout_layout = QHBoxLayout()
        timeout_layout.addWidget(QLabel("재매수 허용 시간 간격:"))
        self.rebuyTimeoutSpinBox = QSpinBox()
        self.rebuyTimeoutSpinBox.setRange(0, 480)
        self.rebuyTimeoutSpinBox.setValue(60)
        self.rebuyTimeoutSpinBox.setSuffix("분")
        self.rebuyTimeoutSpinBox.setToolTip("매도 후 설정한 시간이 지나면 재매수 허용")
        timeout_layout.addWidget(self.rebuyTimeoutSpinBox)
        timeout_layout.addStretch()
        advanced_layout.addLayout(timeout_layout)

        rebuy_layout.addLayout(advanced_layout)
        layout.addWidget(rebuy_group)

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

        # === 당일 매도 종목 현황 탭 추가 ===
        sold_stocks_tab = QWidget()
        sold_stocks_layout = QVBoxLayout(sold_stocks_tab)

        # 통계 정보
        stats_layout = QHBoxLayout()
        self.soldStatsLabel = QLabel("당일 매도 통계: 로딩 중...")
        self.soldStatsLabel.setStyleSheet("QLabel { font-weight: bold; color: #1976d2; }")
        stats_layout.addWidget(self.soldStatsLabel)
        stats_layout.addStretch()

        # 새로고침 버튼
        refresh_button = QPushButton("새로고침")
        refresh_button.clicked.connect(self.refresh_sold_stocks_stats)
        stats_layout.addWidget(refresh_button)

        sold_stocks_layout.addLayout(stats_layout)

        # 당일 매도 종목 테이블
        self.soldStocksTableView = QTableView()
        self.soldStocksTableView.setEditTriggers(QTableView.NoEditTriggers)
        self.soldStocksTableView.setSortingEnabled(True)
        self.soldStocksTableView.horizontalHeader().setStretchLastSection(True)
        sold_stocks_layout.addWidget(self.soldStocksTableView)

        tab_widget.addTab(sold_stocks_tab, "당일 매도 현황")

        return tab_widget

    def refresh_sold_stocks_stats(self):
        """당일 매도 종목 통계 새로고침"""
        try:
            if len(self.today_sold_df) > 0:
                총매도건수 = len(self.today_sold_df)
                평균수익률 = self.today_sold_df["수익률"].mean()
                수익건수 = len(self.today_sold_df[self.today_sold_df["수익률"] > 0])
                승률 = (수익건수 / 총매도건수 * 100) if 총매도건수 > 0 else 0
                총매도금액 = self.today_sold_df["매도금액"].sum()

                stats_text = (f"당일 매도 통계: 총 {총매도건수}건 | "
                              f"평균수익률: {평균수익률:+.2f}% | "
                              f"승률: {승률:.1f}% | "
                              f"총매도금액: {총매도금액:,.0f}원")

                self.soldStatsLabel.setText(stats_text)

                # 테이블 업데이트
                if hasattr(self, 'soldStocksTableView'):
                    display_df = self.today_sold_df.copy()
                    display_df["매도시간"] = display_df["매도시간"].dt.strftime("%H:%M:%S")
                    display_df["수익률"] = display_df["수익률"].apply(lambda x: f"{x:+.2f}%")
                    display_df["매도금액"] = display_df["매도금액"].apply(lambda x: f"{x:,.0f}원")

                    model = PandasModel(display_df)
                    self.soldStocksTableView.setModel(model)
                    self.soldStocksTableView.resizeColumnsToContents()
            else:
                self.soldStatsLabel.setText("당일 매도 통계: 매도 기록 없음")
                # 빈 테이블 표시
                empty_df = pd.DataFrame(columns=["종목코드", "종목명", "매도시간", "수익률", "매도사유"])
                model = PandasModel(empty_df)
                self.soldStocksTableView.setModel(model)

        except Exception as e:
            log_error(f"당일 매도 통계 새로고침 실패: {str(e)}")
            self.soldStatsLabel.setText("당일 매도 통계: 오류 발생")

    def setup_timers(self):
        log_info("타이머 설정 시작")
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

        # 당일 매도 통계 업데이트 타이머
        self.timer7 = QTimer()
        self.timer7.timeout.connect(self.refresh_sold_stocks_stats)
        self.timer7.start(30000)  # 30초마다 업데이트

        log_info("타이머 설정 완료")

    def init_data(self):
        log_info("데이터 초기화 시작")
        self.init_time()
        self.load_settings()

        self.websocket_req_queue.put(dict(action_id="조건검색식리스트"))
        self.tr_req_queue.put(dict(action_id="계좌조회"))

        log_info("데이터 초기화 완료")

    # 기존 메서드들은 그대로 유지
    @log_exceptions
    def check_valid_time(self):
        """각 조건식별 유효 시간 확인"""
        condition_data = self.buy_condition_model.get_data()
        current_time = datetime.datetime.now().time()

        for idx, row in condition_data.iterrows():
            condition_name = row['조건명']
            start_time = datetime.datetime.strptime(row['시작시간'], "%H:%M:%S").time()
            end_time = datetime.datetime.strptime(row['종료시간'], "%H:%M:%S").time()
            is_active = row['활성화']

            # 시간 범위 내에 있고 활성화된 조건식인지 확인
            is_valid_time = start_time <= current_time <= end_time and is_active

            # 조건식별 거래 가능 상태 업데이트 (필요시 딕셔너리로 관리)
            if not hasattr(self, 'condition_trading_status'):
                self.condition_trading_status = {}

            prev_status = self.condition_trading_status.get(condition_name, None)
            self.condition_trading_status[condition_name] = is_valid_time

            # 상태 변경 시 로그
            if prev_status != is_valid_time:
                if is_valid_time:
                    log_trading(f"조건식 거래시간 시작: {condition_name} ({row['시작시간']} ~ {row['종료시간']})")
                else:
                    log_trading(f"조건식 거래시간 종료: {condition_name}")

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
                    log_debug(f"종목코드: {종목코드} 기본정보 부재!")
                    continue
                order_time = datetime.datetime.now().replace(
                    hour=int(주문접수시간[:-4]),
                    minute=int(주문접수시간[-4:-2]),
                    second=int(주문접수시간[-2:]),
                )
                if now_time > order_time and (now_time - order_time).seconds > self.amendOrderSpinBox.value():
                    log_order(f"미체결 정정주문 발생 - 종목: {종목코드}, 주문번호: {order_num}, 미체결시간: {(now_time - order_time).seconds}초")
                    if 매수매도구분 == "매수":
                        주문가격 = basic_info_dict["상한가"]
                    elif 매수매도구분 == "매도":
                        주문가격 = basic_info_dict["하한가"]
                    else:
                        log_debug(f"매수매도구분: {매수매도구분} continue!")
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
                log_error(f"미체결 주문 확인 중 에러: {str(e)}", exception=True)
        self.timer5.start(1000)

    def save_pickle(self):
        self.timer4.stop()
        try:
            are_equal = self.realtime_tracking_df.equals(self.last_saved_realtime_tracking_df)
            if not are_equal:
                # 데이터 매니저를 통해 저장
                data_manager.save_realtime_tracking_df(self.realtime_tracking_df)
                self.last_saved_realtime_tracking_df = self.realtime_tracking_df.copy(deep=True)
                log_debug("실시간 트래킹 데이터 저장 완료")
        except Exception as e:
            log_error(f"데이터 저장 중 에러: {str(e)}", exception=True)
        self.timer4.start(5000)

    @log_exceptions
    def add_buy_condition(self):
        """매수 조건식 추가 (수정됨)"""
        condition_name = self.buyConditionComboBox.currentText()
        if not condition_name or condition_name not in self.condition_name_to_index_dict:
            log_info("유효하지 않은 조건식이 선택됨")
            return

        condition_index = self.condition_name_to_index_dict[condition_name]

        # 시간 설정 다이얼로그 표시
        dialog = TimeSettingDialog(parent=self)
        if dialog.exec_() == QDialog.Accepted:
            start_time, end_time = dialog.get_times()

            if self.buy_condition_model.add_condition(condition_name, condition_index, start_time, end_time):
                log_info(f"매수 조건식 추가: {condition_name} ({start_time} ~ {end_time})")
                # 테이블 새로고침
                self.buyConditionTableView.resizeColumnsToContents()
                self.buyConditionTableView.update()
            else:
                log_info(f"이미 추가된 조건식: {condition_name}")

    @log_exceptions
    def remove_buy_condition(self):
        """선택된 매수 조건식 삭제 (수정됨)"""
        selection_model = self.buyConditionTableView.selectionModel()
        if not selection_model.hasSelection():
            log_info("삭제할 조건식이 선택되지 않음")
            return

        selected_indexes = selection_model.selectedRows()
        if not selected_indexes:
            log_info("선택된 행이 없음")
            return

        row = selected_indexes[0].row()
        condition_info = self.buy_condition_model.get_condition_at_row(row)

        if condition_info:
            condition_name = condition_info['조건명']
            if self.buy_condition_model.remove_condition(row):
                log_info(f"매수 조건식 삭제: {condition_name}")
                # 테이블 새로고침
                self.buyConditionTableView.update()
            else:
                log_error(f"조건식 삭제 실패: {condition_name}")
        else:
            log_error("조건식 정보를 가져올 수 없음")

    @log_exceptions
    def edit_condition_time(self, index):
        """조건식 시간 설정 편집 (수정됨)"""
        if not index.isValid():
            return

        row = index.row()
        condition_info = self.buy_condition_model.get_condition_at_row(row)

        if not condition_info:
            log_error("조건식 정보를 가져올 수 없음")
            return

        current_start = condition_info['시작시간']
        current_end = condition_info['종료시간']
        condition_name = condition_info['조건명']

        dialog = TimeSettingDialog(current_start, current_end, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            start_time, end_time = dialog.get_times()
            self.buy_condition_model.update_time(row, start_time, end_time)
            log_info(f"조건식 시간 변경: {condition_name} ({start_time} ~ {end_time})")

    @log_exceptions
    def show_condition_context_menu(self, position):
        """조건식 테이블 우클릭 메뉴 (선택사항)"""
        from PyQt5.QtWidgets import QMenu, QAction

        if not self.buyConditionTableView.indexAt(position).isValid():
            return

        menu = QMenu()

        # 시간 편집 액션
        edit_action = QAction("시간 편집", self)
        edit_action.triggered.connect(lambda: self.edit_condition_time(self.buyConditionTableView.indexAt(position)))
        menu.addAction(edit_action)

        # 활성화/비활성화 토글 액션
        row = self.buyConditionTableView.indexAt(position).row()
        condition_info = self.buy_condition_model.get_condition_at_row(row)
        if condition_info:
            is_active = condition_info['활성화']
            toggle_text = "비활성화" if is_active else "활성화"
            toggle_action = QAction(toggle_text, self)
            toggle_action.triggered.connect(lambda: self.toggle_condition_active(row))
            menu.addAction(toggle_action)

        # 삭제 액션
        menu.addSeparator()
        delete_action = QAction("삭제", self)
        delete_action.triggered.connect(self.remove_buy_condition)
        menu.addAction(delete_action)

        menu.exec_(self.buyConditionTableView.mapToGlobal(position))

    @log_exceptions
    def toggle_condition_active(self, row):
        """조건식 활성화 상태 토글"""
        condition_info = self.buy_condition_model.get_condition_at_row(row)
        if condition_info:
            self.buy_condition_model.toggle_active(row)
            condition_name = condition_info['조건명']
            new_status = "활성화" if not condition_info['활성화'] else "비활성화"
            log_info(f"조건식 상태 변경: {condition_name} -> {new_status}")

    @log_exceptions
    def pop_btn_clicked(self):
        target_code = self.popStockCodeLineEdit.text().replace(" ", "")
        if target_code in self.realtime_tracking_df.index:
            self.realtime_tracking_df.drop(target_code, inplace=True)
            log_trading(f"종목 수동 편출: {target_code}")
        else:
            log_debug(f"편출 대상 종목 없음: {target_code}")
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
            log_error(f"테이블 모델 업데이트 중 에러: {str(e)}", exception=True)
        self.timer3.start(1000)

    @log_exceptions
    def auto_trade_on(self):
        """자동매매 시작"""
        log_trading("자동매매 시작 요청")
        self.autoOnPushButton.setEnabled(False)
        self.autoOffPushButton.setEnabled(True)

        # 매수 조건식들 실시간 등록
        condition_data = self.buy_condition_model.get_data()
        active_conditions = condition_data[condition_data['활성화'] == True]

        for _, row in active_conditions.iterrows():
            condition_name = row['조건명']
            condition_index = row['조건index']

            self.websocket_req_queue.put(
                dict(
                    action_id="조건검색실시간등록",
                    조건index=condition_index,
                )
            )
            log_trading(f"매수 조건식 실시간 등록: {condition_name}")

        # 매도 조건식 등록
        sell_condition = self.sellConditionComboBox.currentText()
        if sell_condition:
            self.websocket_req_queue.put(
                dict(
                    action_id="조건검색실시간등록",
                    조건index=self.condition_name_to_index_dict[sell_condition],
                )
            )
            log_trading(f"매도 조건식 실시간 등록: {sell_condition}")

        self.is_no_transaction = False
        self.marketStartTimeEdit.setEnabled(False)
        self.marketEndTimeEdit.setEnabled(False)
        self.timer6.start(1000)

        log_trading("자동매매 시작 완료")

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
        log_info(
            f"거래시간 설정: {self.market_start_time.strftime('%H:%M:%S')} ~ {self.market_end_time.strftime('%H:%M:%S')}")

    @log_exceptions
    def auto_trade_off(self):
        """자동매매 종료"""
        log_trading("자동매매 종료 요청")
        self.autoOnPushButton.setEnabled(True)
        self.autoOffPushButton.setEnabled(False)

        # 매수 조건식들 실시간 해제
        condition_data = self.buy_condition_model.get_data()
        for _, row in condition_data.iterrows():
            condition_name = row['조건명']
            condition_index = row['조건index']

            self.websocket_req_queue.put(
                dict(
                    action_id="조건검색실시간해제",
                    조건index=condition_index,
                )
            )
            log_trading(f"매수 조건식 실시간 해제: {condition_name}")

        # 매도 조건식 해제
        sell_condition = self.sellConditionComboBox.currentText()
        if sell_condition:
            self.websocket_req_queue.put(
                dict(
                    action_id="조건검색실시간해제",
                    조건index=self.condition_name_to_index_dict[sell_condition],
                )
            )
            log_trading(f"매도 조건식 실시간 해제: {sell_condition}")

        self.is_no_transaction = True
        self.marketStartTimeEdit.setEnabled(True)
        self.marketEndTimeEdit.setEnabled(True)
        self.timer6.stop()

        log_trading("자동매매 종료 완료")

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
            log_debug(f"실시간 등록: {stock_code} (현재 등록수: {self.current_realtime_count})")

    @log_exceptions
    def on_receive_account_info(self, data):
        log_info("계좌정보 처리 시작")
        df = data['df']
        account_info_dict = data['account_info_dict']

        if len(df) > 0:
            self.account_info_df = df[["종목코드", "종목명", "현재가", "매입가", "보유수량", "매매가능수량", "수익률(%)"]]
            self.account_info_df.set_index("종목코드", inplace=True)

            log_trading(f"보유종목 현황 - 총 {len(self.account_info_df)}개 종목")

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

            log_trading(
                f"계좌 요약 - 총평가금액: {account_info_dict.get('총평가금액', 0):,}원, 총수익률: {account_info_dict.get('총수익률', 0):.2f}%")

        if not self.has_init:
            for stock_code, row in self.realtime_tracking_df.copy(deep=True).iterrows():
                if stock_code not in self.account_info_df.index:
                    self.realtime_tracking_df.drop(stock_code, inplace=True)
                    log_trading(f"미보유 종목 트래킹 해제: {stock_code}")

        self.update_pandas_models()
        self.has_init = True
        log_info("계좌정보 처리 완료")

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

                    log_debug(f"주식기본정보 수신: {basic_info_dict['종목명']}({종목코드})")

                    if 종목코드 in self.realtime_tracking_df.index and self.realtime_tracking_df.at[
                        종목코드, "매수주문여부"] == False:
                        condition_name = self.realtime_tracking_df.at[종목코드, "매수조건식명"]
                        log_trading(f"매수주문 진행: {basic_info_dict['종목명']}({종목코드}) - {condition_name}")

                        현재가 = basic_info_dict["현재가"]
                        종목명 = basic_info_dict["종목명"]
                        self.realtime_tracking_df.at[종목코드, "종목명"] = 종목명
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
                            log_trading(f"매수주문 실패 - 주문수량 부족: {종목코드}, 수량: {주문수량}", level="WARNING")
                            self.timer2.start(100)
                            return

                        # 텔레그램 알림: 매수 조건 편입
                        try:
                            send_telegram_alert('buy_condition',
                                                stock_code=종목코드,
                                                stock_name=종목명,
                                                condition_name=condition_name,
                                                current_price=현재가,
                                                buy_amount=주문금액,
                                                expected_quantity=주문수량
                                                )
                        except Exception as e:
                            log_error(f"텔레그램 매수 조건 알림 전송 실패: {str(e)}")

                        log_trading(f"매수주문 상세 - 종목: {종목코드}, 현재가: {현재가:,}, 주문가격: {주문가격}, 주문수량: {주문수량:,}주")

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
            log_error(f"TR 결과 처리 중 에러: {str(e)}", exception=True)
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
        """주문 결과 처리 (당일 매도 종목 기록 추가)"""
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
        주문가격 = data['주문가격']

        if 주문상태 == "접수" and 종목코드 in self.realtime_tracking_df.index:
            self.order_info_df.loc[주문번호] = {
                "주문접수시간": 주문및체결시간, "종목코드": 종목코드, "주문수량": 주문수량, "매수매도구분": 주문구분,
            }
            log_order(f"주문접수 - {종목명}({종목코드}), 주문번호: {주문번호}, 구분: {주문구분}")

            # 텔레그램 알림: 주문 접수 (condition_name 정의 수정)
            condition_name = "Unknown"  # 기본값 설정
            if 종목코드 in self.realtime_tracking_df.index:
                condition_name = self.realtime_tracking_df.at[종목코드, "매수조건식명"] or "Unknown"

            try:
                if 주문구분 in ("매수", "매수정정"):
                    send_telegram_alert('buy_order',
                                        stock_code=종목코드,
                                        stock_name=종목명,
                                        condition_name=condition_name,
                                        order_price=주문가격 if 주문가격 else 0,
                                        order_quantity=주문수량,
                                        order_no=주문번호,
                                        is_market_order=(주문가격 is None or 주문가격 == 0)
                                        )
                elif 주문구분 in ("매도", "매도정정"):
                    매도사유 = "Unknown"
                    매입가 = 0
                    현재가 = 0
                    예상수익률 = 0

                    if 종목코드 in self.realtime_tracking_df.index:
                        매도사유 = self.realtime_tracking_df.at[종목코드, "매도사유"] or "조건식"
                        매입가 = self.realtime_tracking_df.at[종목코드, "매입가"] or 0
                        현재가 = 주문가격 if 주문가격 else self.realtime_tracking_df.at[종목코드, "현재가"] or 0
                        예상수익률 = ((현재가 - 매입가) / 매입가 * 100) if 매입가 > 0 else 0

                    send_telegram_alert('sell_order',
                                        stock_code=종목코드,
                                        stock_name=종목명,
                                        buy_condition=condition_name,
                                        sell_reason=매도사유,
                                        order_price=주문가격 if 주문가격 else 0,
                                        order_quantity=주문수량,
                                        order_no=주문번호,
                                        expected_profit_rate=예상수익률,
                                        is_market_order=(주문가격 is None or 주문가격 == 0)
                                        )
            except Exception as e:
                log_error(f"텔레그램 주문 접수 알림 전송 실패: {str(e)}")

        if 주문상태 == "체결" and 미체결수량 == 0 and 주문번호 in self.order_info_df.index:
            log_order(f"주문체결완료 - 주문번호: {주문번호}")
            self.order_info_df.drop(주문번호, inplace=True)

        if 주문상태 == "체결" and data['주문구분'] in ("매수", "매수정정"):
            if 종목코드 in self.account_info_df.index:
                보유수량 = self.account_info_df.at[종목코드, "보유수량"]
                매입가 = self.account_info_df.at[종목코드, "매입가"]
                new_매입가 = round((매입가 * 보유수량 + 단위체결가 * 단위체결량) / (보유수량 + 단위체결량), 1)
                self.account_info_df.at[종목코드, "보유수량"] = 보유수량 + 단위체결량
                self.account_info_df.at[종목코드, "매매가능수량"] += 단위체결량
                self.account_info_df.at[종목코드, "매입가"] = new_매입가

                log_trading(f"매수체결 - {종목명}({종목코드}), 체결가: {단위체결가:,}, 체결량: {단위체결량:,}주, 평균단가: {new_매입가:,}")

                if 종목코드 in self.realtime_tracking_df.index:
                    self.realtime_tracking_df.at[종목코드, "매입가"] = new_매입가
                    condition_name = self.realtime_tracking_df.at[종목코드, "매수조건식명"] or "Unknown"

                    # 텔레그램 알림: 매수 체결 완료
                    try:
                        send_telegram_alert('buy_filled',
                                            stock_code=종목코드,
                                            stock_name=종목명,
                                            condition_name=condition_name,
                                            filled_price=단위체결가,
                                            filled_quantity=단위체결량,
                                            filled_amount=단위체결가 * 단위체결량,
                                            avg_price=new_매입가
                                            )
                    except Exception as e:
                        log_error(f"텔레그램 매수 체결 알림 전송 실패: {str(e)}")

            else:
                self.account_info_df.loc[종목코드] = {
                    "종목명": 종목명,
                    "현재가": 단위체결가,
                    "매입가": 단위체결가,
                    "보유수량": 단위체결량,
                    "매매가능수량": 단위체결량,
                    "수익률(%)": -self.transaction_cost,
                }

                log_trading(f"신규매수체결 - {종목명}({종목코드}), 체결가: {단위체결가:,}, 체결량: {단위체결량:,}주")

                if 종목코드 in self.realtime_tracking_df.index:
                    self.realtime_tracking_df.at[종목코드, "매입가"] = 단위체결가
                    self.realtime_tracking_df.at[종목코드, "수익률(%)"] = -self.transaction_cost
                    condition_name = self.realtime_tracking_df.at[종목코드, "매수조건식명"] or "Unknown"

                    # 텔레그램 알림: 신규 매수 체결 완료
                    try:
                        send_telegram_alert('buy_filled',
                                            stock_code=종목코드,
                                            stock_name=종목명,
                                            condition_name=condition_name,
                                            filled_price=단위체결가,
                                            filled_quantity=단위체결량,
                                            filled_amount=단위체결가 * 단위체결량,
                                            avg_price=단위체결가
                                            )
                    except Exception as e:
                        log_error(f"텔레그램 신규 매수 체결 알림 전송 실패: {str(e)}")

        elif 주문상태 == "체결" and data['주문구분'] in ("매도", "매도정정"):
            if 종목코드 in self.account_info_df.index:
                self.account_info_df.at[종목코드, "보유수량"] -= 단위체결량
                self.account_info_df.at[종목코드, "매매가능수량"] -= 단위체결량
                보유수량 = self.account_info_df.at[종목코드, "보유수량"]

                log_trading(f"매도체결 - {종목명}({종목코드}), 체결가: {단위체결가:,}, 체결량: {단위체결량:,}주, 잔여: {보유수량:,}주")

                # 텔레그램 알림: 매도 체결 완료 (수정)
                condition_name = "Unknown"
                매도사유 = "Unknown"
                매입가 = 0
                예상수익률 = 0

                if 종목코드 in self.realtime_tracking_df.index:
                    condition_name = self.realtime_tracking_df.at[종목코드, "매수조건식명"] or "Unknown"
                    매도사유 = self.realtime_tracking_df.at[종목코드, "매도사유"] or "조건식"
                    매입가 = self.realtime_tracking_df.at[종목코드, "매입가"] or 0
                    예상수익률 = ((단위체결가 - 매입가) / 매입가 * 100) if 매입가 > 0 else 0

                try:
                    send_telegram_alert('sell_filled',
                                        stock_code=종목코드,
                                        stock_name=종목명,
                                        buy_condition=condition_name,
                                        sell_reason=매도사유,
                                        filled_price=단위체결가,
                                        filled_quantity=단위체결량,
                                        filled_amount=단위체결가 * 단위체결량,
                                        profit_rate=예상수익률
                                        )
                except Exception as e:
                    log_error(f"텔레그램 매도 체결 알림 전송 실패: {str(e)}")

                if 보유수량 <= 0:
                    # === 당일 매도 종목 기록 (핵심 기능 추가) ===
                    매도시간 = datetime.datetime.now()
                    매수조건식 = "Unknown"
                    수익률 = 예상수익률

                    if 종목코드 in self.realtime_tracking_df.index:
                        매수조건식 = self.realtime_tracking_df.at[종목코드, "매수조건식명"] or "Unknown"
                        매입가 = self.realtime_tracking_df.at[종목코드, "매입가"] or 0
                        수익률 = ((단위체결가 - 매입가) / 매입가 * 100) if 매입가 > 0 else 0

                    # 1. 초고속 체크용 set에 추가
                    self.today_sold_stocks.add(종목코드)

                    # 2. 상세 정보 dict에 추가
                    self.today_sold_details[종목코드] = {
                        "매도시간": 매도시간,
                        "수익률": 수익률,
                        "매도사유": 매도사유,
                        "매수조건식": 매수조건식,
                        "매입가": 매입가,
                        "매도가": 단위체결가
                    }

                    # 3. 완전한 기록 DataFrame에 추가
                    self.today_sold_df.loc[len(self.today_sold_df)] = {
                        "종목코드": 종목코드,
                        "종목명": 종목명,
                        "매도시간": 매도시간,
                        "매수조건식": 매수조건식,
                        "매도사유": 매도사유,
                        "매입가": 매입가,
                        "매도가": 단위체결가,
                        "수익률": 수익률,
                        "매도금액": 단위체결가 * 단위체결량
                    }

                    # 4. 조건식별 성과 분석에 추가
                    self.condition_performance[매수조건식].append({
                        "종목코드": 종목코드,
                        "수익률": 수익률,
                        "시간": 매도시간
                    })

                    # 5. 시간대별 패턴 분석에 추가
                    hour = 매도시간.hour
                    self.hourly_sell_pattern[hour] += 1

                    # 6. 당일 매도 기록 저장 - 데이터 매니저 사용
                    try:
                        data_manager.save_today_sold_data(self.today_sold_df, self.today_date)
                    except Exception as e:
                        log_error(f"당일 매도 기록 저장 실패: {str(e)}")

                    # 7. 실시간 통계 업데이트
                    self.update_realtime_statistics()

                    log_trading(f"당일 매도 종목 기록 완료: {종목명}({종목코드}) - {매수조건식}, 수익률: {수익률:+.2f}%")

                    # 기존 삭제 로직
                    self.account_info_df.drop(종목코드, inplace=True)
                    if 종목코드 in self.realtime_tracking_df.index:
                        self.realtime_tracking_df.drop(종목코드, inplace=True)
                        log_trading(f"매도완료 트래킹 해제: {종목명}({종목코드})")
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
        log_info(f"조건검색식 리스트 로드 완료: {len(self.condition_df)}개")

    @log_exceptions
    def on_receive_realtime_condition_event(self, data):
        """실시간 조건식 이벤트 처리 (재매수 방지 기능 추가)"""
        조건식idx = data['조건식idx']
        종목코드 = data['종목코드']
        편입편출 = data['편입편출']

        # 해당 조건식 정보 찾기
        condition_data = self.buy_condition_model.get_data()
        matching_condition = condition_data[condition_data['조건index'] == 조건식idx]

        if len(matching_condition) == 0:
            # 매도 조건식인지 확인
            sell_condition = self.sellConditionComboBox.currentText()
            if sell_condition and self.condition_name_to_index_dict.get(sell_condition) == 조건식idx:
                # 기존 매도 로직 실행
                self.handle_sell_condition_event(data)
            return

        condition_row = matching_condition.iloc[0]
        condition_name = condition_row['조건명']

        # 조건식별 거래 시간 확인
        if not hasattr(self, 'condition_trading_status'):
            self.condition_trading_status = {}

        is_trading_time = self.condition_trading_status.get(condition_name, False)

        # === 당일 매도 종목 재매수 방지 체크 (핵심 기능) ===
        if 편입편출 == "I" and self.should_prevent_rebuy(종목코드, condition_name):
            prev_info = self.today_sold_details.get(종목코드, {})
            매도시간 = prev_info.get("매도시간", "Unknown")
            수익률 = prev_info.get("수익률", 0)
            매도사유 = prev_info.get("매도사유", "Unknown")
            이전조건식 = prev_info.get("매수조건식", "Unknown")

            time_str = 매도시간.strftime('%H:%M:%S') if isinstance(매도시간, datetime.datetime) else str(매도시간)

            log_trading(f"당일 매도 종목 재매수 차단: {종목코드} - {condition_name} "
                        f"(이전 매도: {time_str}, 수익률: {수익률:+.2f}%, "
                        f"매도사유: {매도사유}, 이전조건식: {이전조건식})")

            # 텔레그램 알림: 재매수 차단
            try:
                send_telegram_alert('buy_condition',
                                    stock_code=종목코드,
                                    stock_name=f"재매수차단_{종목코드}",
                                    condition_name=f"[차단]{condition_name}",
                                    current_price=0,
                                    buy_amount=0,
                                    expected_quantity=0
                                    )
            except Exception as e:
                log_error(f"텔레그램 재매수 차단 알림 전송 실패: {str(e)}")

            return  # 매수 진행하지 않음

        # 매수 조건 확인 (기존 로직)
        if all([
            self.current_realtime_count < self.max_realtime_count,
            편입편출 == "I",
            is_trading_time,  # 조건식별 거래 시간 확인
            not self.is_no_transaction,
            len(self.realtime_tracking_df) < self.maxAutoTradeCountSpinBox.value(),
            종목코드 not in self.account_info_df.index,
            종목코드 not in self.realtime_tracking_df.index,
        ]):
            log_trading(f"매수 조건식 편입: {종목코드} - {condition_name}")

            # 기본 정보 요청
            self.register_realtime_info(종목코드)
            self.tr_req_queue.put(
                dict(
                    action_id="주식기본정보",
                    종목코드=종목코드,
                )
            )

            # 실시간 트래킹 데이터에 조건식 정보 포함하여 추가
            self.realtime_tracking_df.loc[종목코드] = {
                "종목명": None,
                "현재가": None,
                "매입가": None,
                "수익률(%)": None,
                "트레일링 발동 여부": False,
                "트레일링 발동 후 고가": None,
                "매수주문여부": False,
                "매도주문여부": False,
                "매수조건식명": condition_name,
                "매수조건식index": 조건식idx,
                "매도조건식명": None,
                "매도사유": None
            }

    def handle_sell_condition_event(self, data):
        """매도 조건 이벤트 처리"""
        조건식idx = data['조건식idx']
        종목코드 = data['종목코드']
        편입편출 = data['편입편출']

        if all([
            종목코드 in self.realtime_tracking_df.index and self.realtime_tracking_df.at[종목코드, "매수주문여부"] == True,
            종목코드 in self.realtime_tracking_df.index and self.realtime_tracking_df.at[종목코드, "매도주문여부"] == False,
            self.condition_name_to_index_dict[self.sellConditionComboBox.currentText()] == 조건식idx,
            편입편출 == "I",
            not self.is_no_transaction,
        ]):
            sell_condition_name = self.condition_index_to_name_dict.get(조건식idx, f"조건식{조건식idx}")
            buy_condition_name = self.realtime_tracking_df.at[종목코드, "매수조건식명"]
            종목명 = self.realtime_tracking_df.at[종목코드, "종목명"] or 종목코드
            현재가 = self.realtime_tracking_df.at[종목코드, "현재가"] or 0
            수익률 = self.realtime_tracking_df.at[종목코드, "수익률(%)"] or 0

            # 매도 조건식 정보 업데이트
            self.realtime_tracking_df.at[종목코드, "매도조건식명"] = sell_condition_name
            self.realtime_tracking_df.at[종목코드, "매도사유"] = "조건식"

            log_trading(f"매도 조건식 편입 - 조건부 매도: {종목명}({종목코드}) - {sell_condition_name}")

            # 텔레그램 알림: 매도 조건 발동
            try:
                send_telegram_alert('sell_condition',
                                    stock_code=종목코드,
                                    stock_name=종목명,
                                    buy_condition=buy_condition_name,
                                    sell_condition=sell_condition_name,
                                    current_price=현재가,
                                    profit_rate=수익률
                                    )
            except Exception as e:
                log_error(f"텔레그램 매도 조건 알림 전송 실패: {str(e)}")

            self.sell_order(종목코드)

    def sell_order(self, 종목코드):
        if 종목코드 not in self.account_info_df.index:
            log_trading(f"매도주문 실패 - 미보유 종목: {종목코드}", level="WARNING")
            return

        self.realtime_tracking_df.at[종목코드, "매도주문여부"] = True
        종목명 = self.account_info_df.at[종목코드, "종목명"]
        시장가여부 = self.marketSellRadioButton.isChecked()
        주문가격 = ''
        주문수량 = self.account_info_df.at[종목코드, "매매가능수량"]
        현재가 = self.account_info_df.at[종목코드, "현재가"]

        if not 시장가여부:
            틱단위 = self.get_tick_size(현재가)
            주문가격 = self.get_order_price(현재가 + self.limitSellSpinBox.value() * 틱단위)

        log_trading(f"매도주문 진행 - {종목명}({종목코드}), 현재가: {현재가:,}, 주문수량: {주문수량:,}주, 시장가: {시장가여부}")

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
        종목명 = self.realtime_tracking_df.at[종목코드, "종목명"] or 종목코드

        if 트레일링발동여부 and not pd.isnull(트레일링발동후고가):
            트레일링발동후고가 = max(트레일링발동후고가, 현재가)
            self.realtime_tracking_df.at[종목코드, "트레일링 발동 후 고가"] = 트레일링발동후고가

        # 손절 조건 확인
        if 매도주문여부 == False and self.stopLossCheckBox.isChecked() and 수익률 < self.stopLossDoubleSpinBox.value():
            buy_condition_name = self.realtime_tracking_df.at[종목코드, "매수조건식명"]
            self.realtime_tracking_df.at[종목코드, "매도사유"] = "손절"

            log_trading(f"손절 발동 - {종목명}({종목코드}), 수익률: {수익률:.2f}% < {self.stopLossDoubleSpinBox.value()}%")

            # 텔레그램 알림: 손절 발동
            try:
                send_telegram_alert('stop_loss',
                                    stock_code=종목코드,
                                    stock_name=종목명,
                                    buy_condition=buy_condition_name,
                                    current_price=현재가,
                                    profit_rate=수익률,
                                    stop_loss_rate=self.stopLossDoubleSpinBox.value()
                                    )
            except Exception as e:
                log_error(f"텔레그램 손절 알림 전송 실패: {str(e)}")

            self.sell_order(종목코드)

        # 트레일링 스탑 발동 조건
        if all([
            트레일링발동여부 == False,
            매도주문여부 == False,
            self.trailingStopCheckBox.isChecked(),
            수익률 >= self.trailingStopDoubleSpinBox1.value(),
        ]):
            buy_condition_name = self.realtime_tracking_df.at[종목코드, "매수조건식명"]

            log_trading(f"트레일링 스탑 발동 - {종목명}({종목코드}), 수익률: {수익률:.2f}% >= {self.trailingStopDoubleSpinBox1.value()}%")

            # 텔레그램 알림: 트레일링 스탑 발동
            try:
                send_telegram_alert('trailing_stop',
                                    stock_code=종목코드,
                                    stock_name=종목명,
                                    buy_condition=buy_condition_name,
                                    current_price=현재가,
                                    profit_rate=수익률,
                                    trailing_rate=self.trailingStopDoubleSpinBox1.value(),
                                    high_price=현재가
                                    )
            except Exception as e:
                log_error(f"텔레그램 트레일링 스탑 알림 전송 실패: {str(e)}")

            self.realtime_tracking_df.at[종목코드, "트레일링 발동 후 고가"] = 현재가
            self.realtime_tracking_df.at[종목코드, "트레일링 발동 여부"] = True

        # 트레일링 스탑 매도 조건
        if all([
            트레일링발동여부 == True,
            매도주문여부 == False,
            not pd.isnull(트레일링발동후고가) and (현재가 - 트레일링발동후고가) / 트레일링발동후고가 * 100 < self.trailingStopDoubleSpinBox2.value(),
        ]):
            buy_condition_name = self.realtime_tracking_df.at[종목코드, "매수조건식명"]
            self.realtime_tracking_df.at[종목코드, "매도사유"] = "트레일링"
            하락률 = (현재가 - 트레일링발동후고가) / 트레일링발동후고가 * 100

            log_trading(
                f"트레일링 스탑 매도 - {종목명}({종목코드}), 고가대비 하락률: {하락률:.2f}% < {self.trailingStopDoubleSpinBox2.value()}%")

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
            log_error(f"웹소켓 결과 처리 중 에러: {str(e)}", exception=True)
        self.timer1.start(10)

    @log_exceptions
    def load_settings(self, is_init=True):
        """설정 로드 (재매수 방지 설정 추가)"""
        log_info("설정 로드 시작")

        # 기존 설정들
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

        # === 재매수 방지 설정 로드 ===
        self.preventSameDayRebuyCheckBox.setChecked(
            self.settings.value('preventSameDayRebuyCheckBox', defaultValue=True, type=bool))

        if hasattr(self, 'preventLossRebuyOnlyCheckBox'):
            self.preventLossRebuyOnlyCheckBox.setChecked(
                self.settings.value('preventLossRebuyOnlyCheckBox', defaultValue=False, type=bool))

        if hasattr(self, 'preventSameConditionOnlyCheckBox'):
            self.preventSameConditionOnlyCheckBox.setChecked(
                self.settings.value('preventSameConditionOnlyCheckBox', defaultValue=False, type=bool))

        if hasattr(self, 'rebuyTimeoutSpinBox'):
            self.rebuyTimeoutSpinBox.setValue(
                self.settings.value("rebuyTimeoutSpinBox", 60, int))

        # 매수 조건식 설정 로드
        try:
            buy_conditions_json = self.settings.value('buyConditions', '[]', type=str)
            import json
            buy_conditions_data = json.loads(buy_conditions_json)

            # BuyConditionModel에 데이터 로드
            if buy_conditions_data:
                conditions_df = pd.DataFrame(buy_conditions_data)
                self.buy_condition_model = BuyConditionModel(conditions_df)
                self.buyConditionTableView.setModel(self.buy_condition_model)
                self.buyConditionTableView.resizeColumnsToContents()
                log_info(f"매수 조건식 설정 로드: {len(buy_conditions_data)}개")
        except Exception as e:
            log_error(f"매수 조건식 설정 로드 실패: {str(e)}")
            self.buy_condition_model = BuyConditionModel()
            self.buyConditionTableView.setModel(self.buy_condition_model)

        if not is_init:
            self.sellConditionComboBox.setCurrentIndex(self.settings.value('sellConditionComboBox', 0, type=int))

        self.marketStartTimeEdit.setTime(
            QTime.fromString(self.settings.value('marketStartTimeEdit', "090000"), "HHmmss"))
        self.marketEndTimeEdit.setTime(QTime.fromString(self.settings.value('marketEndTimeEdit', "153000"), "HHmmss"))

        log_info("설정 로드 완료")

    @log_exceptions
    def save_settings(self):
        """설정 저장 (재매수 방지 설정 추가)"""
        log_info("설정 저장 시작")

        # 기존 설정들
        self.settings.setValue('buyAmountLineEdit', self.buyAmountLineEdit.text())
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

        # === 재매수 방지 설정 저장 ===
        self.settings.setValue('preventSameDayRebuyCheckBox', self.preventSameDayRebuyCheckBox.isChecked())

        if hasattr(self, 'preventLossRebuyOnlyCheckBox'):
            self.settings.setValue('preventLossRebuyOnlyCheckBox', self.preventLossRebuyOnlyCheckBox.isChecked())

        if hasattr(self, 'preventSameConditionOnlyCheckBox'):
            self.settings.setValue('preventSameConditionOnlyCheckBox',
                                   self.preventSameConditionOnlyCheckBox.isChecked())

        if hasattr(self, 'rebuyTimeoutSpinBox'):
            self.settings.setValue("rebuyTimeoutSpinBox", self.rebuyTimeoutSpinBox.value())

        # 매수 조건식 설정 저장
        try:
            conditions_data = self.buy_condition_model.get_data()
            import json
            conditions_json = json.dumps(conditions_data.to_dict('records'), ensure_ascii=False)
            self.settings.setValue('buyConditions', conditions_json)
            log_info(f"매수 조건식 설정 저장: {len(conditions_data)}개")
        except Exception as e:
            log_error(f"매수 조건식 설정 저장 실패: {str(e)}")

        log_info("설정 저장 완료")

    def closeEvent(self, event):
        """프로그램 종료 시 종합 리포트 저장"""
        try:
            log_info("프로그램 종료 - 종합 리포트 저장 시작")
            self.save_comprehensive_report()

            # 텔레그램 알림 시스템 종료
            try:
                notifier = get_telegram_notifier()
                if notifier:
                    notifier.stop()
                    log_info("텔레그램 알림 시스템 종료 완료")
            except Exception as e:
                log_error(f"텔레그램 시스템 종료 중 에러: {str(e)}")

            log_info("프로그램 정상 종료")
            event.accept()
        except Exception as e:
            log_error(f"프로그램 종료 중 에러: {str(e)}")
            event.accept()


sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    log_error(f"시스템 예외 발생 - exctype: {exctype}, value: {value}, traceback: {traceback}")
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = my_exception_hook

if __name__ == "__main__":
    log_info("프로그램 시작")

    tr_req_queue = Queue()
    tr_result_queue = Queue()
    order_tr_req_queue = Queue()
    websocket_req_queue = Queue()
    websocket_result_queue = Queue()

    log_info("프로세스 시작")
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

    log_info("모든 프로세스 시작 완료")

    app = QApplication(sys.argv)
    kiwoom_api = KiwoomAPI(
        tr_req_queue=tr_req_queue,
        tr_result_queue=tr_result_queue,
        order_tr_req_queue=order_tr_req_queue,
        websocket_req_queue=websocket_req_queue,
        websocket_result_queue=websocket_result_queue,
    )
    kiwoom_api.show()

    log_info("GUI 애플리케이션 시작")

    try:
        sys.exit(app.exec_())
    except Exception as e:
        log_error(f"애플리케이션 실행 중 에러: {str(e)}", exception=True)
    finally:
        # 종료 시 종합 리포트 저장
        try:
            if 'kiwoom_api' in locals():
                kiwoom_api.save_comprehensive_report()
        except Exception as e:
            log_error(f"종료 시 리포트 저장 실패: {str(e)}")

        # 텔레그램 알림 시스템 종료
        try:
            notifier = get_telegram_notifier()
            if notifier:
                notifier.stop()
                log_info("텔레그램 알림 시스템 종료 완료")
        except Exception as e:
            log_error(f"텔레그램 시스템 종료 중 에러: {str(e)}")