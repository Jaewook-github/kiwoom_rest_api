import os
import sys
# 현재 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, 'utils'))
sys.path.append(os.path.join(current_dir, 'config'))
sys.path.append(os.path.join(current_dir, 'func'))
sys.path.append(os.path.join(current_dir, 'data'))
sys.path.append(os.path.join(current_dir, 'logs'))

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

import time
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
        """메인 UI 초기화 - 안전한 버전 전환 시스템"""
        log_info("UI 초기화 시작")
        
        # UI 버전 설정 (쉬운 전환을 위해)
        UI_VERSION = "v2"  # "original" 또는 "v2"
        
        # 강제로 v2 실행 (디버그용)
        log_info("강제로 UI v2 로드 시도")
        self.init_ui_v2()
        log_info("UI v2 로드 완료")
        
        # try:
        #     if UI_VERSION == "v2":
        #         self.init_ui_v2()
        #         log_info("UI v2 로드 완료")
        #     else:
        #         self.init_ui_original()
        #         log_info("원본 UI 로드 완료")
        # except Exception as e:
        #     log_error(f"UI v2 로드 실패, 원본 UI로 폴백: {str(e)}")
        #     self.init_ui_original()

    def init_ui_original(self):
        """기존 UI 시스템 (백업용)"""
        log_info("원본 UI 초기화 시작")
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

        log_info("원본 UI 초기화 완료")

    def init_ui_v2(self):
        """새로운 탭 기반 UI 시스템"""
        log_info("탭 기반 UI v2 초기화 시작")
        self.setWindowTitle("키움증권 자동매매 프로그램 v2.0")
        self.setMinimumSize(1400, 900)
        self.resize(1600, 1000)

        # 메인 위젯 및 레이아웃
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)

        # 메인 탭 위젯 생성
        self.main_tab_widget = QTabWidget()
        self.main_tab_widget.setTabPosition(QTabWidget.North)
        self.main_tab_widget.setMovable(False)
        self.main_tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #c0c0c0;
                background-color: #fafafa;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #f0f0f0;
                border: 1px solid #c0c0c0;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 100px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom-color: white;
                color: #2196F3;
            }
            QTabBar::tab:hover {
                background-color: #e3f2fd;
            }
        """)

        # 탭들 생성
        self.create_control_tab()
        self.create_buy_settings_tab()
        self.create_sell_settings_tab()
        self.create_account_tab()
        self.create_trading_tab()
        self.create_sell_records_tab()
        self.create_log_tab()

        # 메인 레이아웃에 탭 위젯 추가
        main_layout.addWidget(self.main_tab_widget)

        # 매수 조건식 테이블 설정 (기존 호환성 유지)
        self.setup_buy_condition_table()

        log_info("탭 기반 UI v2 초기화 완료")

    def create_control_tab(self):
        """🎛️ 제어판 탭 생성"""
        control_tab = QWidget()
        layout = QVBoxLayout(control_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # === 핵심 제어 영역 ===
        core_group = QGroupBox("🚀 핵심 제어")
        core_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #2196F3;
                border-radius: 8px;
                margin-top: 1ex;
                background-color: #e3f2fd;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: #1976d2;
            }
        """)
        core_layout = QGridLayout(core_group)

        # 자동매매 제어 버튼들
        self.autoOnPushButton = QPushButton("🟢 자동매매 ON")
        self.autoOnPushButton.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                font-size: 12px;
                padding: 12px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.autoOnPushButton.clicked.connect(self.auto_trade_on)

        self.autoOffPushButton = QPushButton("🔴 자동매매 OFF")
        self.autoOffPushButton.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-weight: bold;
                font-size: 12px;
                padding: 12px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #c41411;
            }
        """)
        self.autoOffPushButton.clicked.connect(self.auto_trade_off)

        self.savePushButton = QPushButton("💾 설정 저장")
        self.savePushButton.setStyleSheet("""
            QPushButton {
                background-color: #ff9800;
                color: white;
                font-weight: bold;
                font-size: 12px;
                padding: 12px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #f57c00;
            }
            QPushButton:pressed {
                background-color: #ef6c00;
            }
        """)
        self.savePushButton.clicked.connect(self.save_settings)

        # 실시간 상태 표시
        status_label = QLabel("📊 실시간 상태")
        status_label.setStyleSheet("QLabel { font-weight: bold; color: #2196F3; }")
        
        self.realtime_status_label = QLabel("등록: 0/95 종목")
        self.realtime_status_label.setStyleSheet("""
            QLabel {
                background-color: #2196F3;
                color: white;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
        """)

        self.trading_status_label = QLabel("자동매매: 0/10 종목")
        self.trading_status_label.setStyleSheet("""
            QLabel {
                background-color: #673ab7;
                color: white;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
        """)

        # 핵심 제어 레이아웃
        core_layout.addWidget(self.autoOnPushButton, 0, 0)
        core_layout.addWidget(self.autoOffPushButton, 0, 1)
        core_layout.addWidget(self.savePushButton, 0, 2)
        core_layout.addWidget(status_label, 1, 0)
        core_layout.addWidget(self.realtime_status_label, 1, 1)
        core_layout.addWidget(self.trading_status_label, 1, 2)

        layout.addWidget(core_group)

        # === 설정 그리드 ===
        settings_container = QWidget()
        settings_grid = QGridLayout(settings_container)

        # 거래 시간 설정
        time_group = self.create_time_settings_group()
        settings_grid.addWidget(time_group, 0, 0)

        # 주문 관리 설정
        order_group = self.create_order_management_group()
        settings_grid.addWidget(order_group, 0, 1)

        # 당일 통계
        stats_group = self.create_daily_stats_group()
        settings_grid.addWidget(stats_group, 1, 0)

        # 알림 설정
        notification_group = self.create_notification_group()
        settings_grid.addWidget(notification_group, 1, 1)

        layout.addWidget(settings_container)

        # === 빠른 액션 버튼들 ===
        quick_actions_group = self.create_quick_actions_group()
        layout.addWidget(quick_actions_group)

        # === 시스템 상태 ===
        system_status_group = self.create_system_status_group()
        layout.addWidget(system_status_group)

        # 탭에 추가
        self.main_tab_widget.addTab(control_tab, "🎛️ 제어판")

    def create_time_settings_group(self):
        """거래 시간 설정 그룹"""
        group = QGroupBox("⏰ 거래 시간")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #4caf50;
                border-radius: 6px;
                margin-top: 1ex;
                background-color: #f1f8e9;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #2e7d32;
            }
        """)
        layout = QGridLayout(group)

        # 시작 시간
        layout.addWidget(QLabel("시작 시간:"), 0, 0)
        self.marketStartTimeEdit = QTimeEdit()
        self.marketStartTimeEdit.setTime(QTime(9, 0, 0))
        self.marketStartTimeEdit.setDisplayFormat("HH:mm:ss")
        self.marketStartTimeEdit.setStyleSheet("""
            QTimeEdit {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
        """)
        layout.addWidget(self.marketStartTimeEdit, 0, 1)

        # 종료 시간
        layout.addWidget(QLabel("종료 시간:"), 1, 0)
        self.marketEndTimeEdit = QTimeEdit()
        self.marketEndTimeEdit.setTime(QTime(15, 30, 0))
        self.marketEndTimeEdit.setDisplayFormat("HH:mm:ss")
        self.marketEndTimeEdit.setStyleSheet("""
            QTimeEdit {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
        """)
        layout.addWidget(self.marketEndTimeEdit, 1, 1)

        # 주의사항
        warning_label = QLabel("⚠️ 장 마감 30분 전 자동 정리매매")
        warning_label.setStyleSheet("QLabel { color: #666; font-size: 10px; }")
        layout.addWidget(warning_label, 2, 0, 1, 2)

        return group

    def create_order_management_group(self):
        """주문 관리 설정 그룹"""
        group = QGroupBox("⚡ 주문 관리")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ff9800;
                border-radius: 6px;
                margin-top: 1ex;
                background-color: #fff3e0;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #f57c00;
            }
        """)
        layout = QGridLayout(group)

        # 미체결 정정
        layout.addWidget(QLabel("미체결 정정:"), 0, 0)
        self.amendOrderSpinBox = QSpinBox()
        self.amendOrderSpinBox.setRange(0, 999)
        self.amendOrderSpinBox.setValue(60)
        self.amendOrderSpinBox.setSuffix("초")
        self.amendOrderSpinBox.setStyleSheet("""
            QSpinBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
        """)
        layout.addWidget(self.amendOrderSpinBox, 0, 1)

        # 최대 종목 수
        layout.addWidget(QLabel("최대 종목:"), 1, 0)
        self.maxAutoTradeCountSpinBox = QSpinBox()
        self.maxAutoTradeCountSpinBox.setRange(0, 95)
        self.maxAutoTradeCountSpinBox.setValue(10)
        self.maxAutoTradeCountSpinBox.setSuffix("종목")
        self.maxAutoTradeCountSpinBox.setStyleSheet("""
            QSpinBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
        """)
        layout.addWidget(self.maxAutoTradeCountSpinBox, 1, 1)

        # 알림 상태
        telegram_label = QLabel("📱 텔레그램 알림: 활성화")
        telegram_label.setStyleSheet("QLabel { color: #4caf50; font-size: 10px; font-weight: bold; }")
        layout.addWidget(telegram_label, 2, 0, 1, 2)

        return group

    def create_daily_stats_group(self):
        """당일 통계 그룹"""
        group = QGroupBox("📊 당일 실적")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #3f51b5;
                border-radius: 6px;
                margin-top: 1ex;
                background-color: #e8eaf6;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #3f51b5;
            }
        """)
        layout = QGridLayout(group)

        # 통계 라벨들
        self.daily_sell_count_label = QLabel("총 매도: 0건")
        self.daily_win_rate_label = QLabel("승률: 0%")
        self.daily_avg_profit_label = QLabel("평균수익: 0%")
        self.daily_total_profit_label = QLabel("총 수익: 0원")

        # 스타일 적용
        stat_style = """
            QLabel {
                padding: 4px;
                border-radius: 3px;
                background-color: white;
                border: 1px solid #ddd;
            }
        """
        for label in [self.daily_sell_count_label, self.daily_win_rate_label, 
                     self.daily_avg_profit_label, self.daily_total_profit_label]:
            label.setStyleSheet(stat_style)

        layout.addWidget(self.daily_sell_count_label, 0, 0)
        layout.addWidget(self.daily_win_rate_label, 0, 1)
        layout.addWidget(self.daily_avg_profit_label, 1, 0)
        layout.addWidget(self.daily_total_profit_label, 1, 1)

        return group

    def create_notification_group(self):
        """알림 설정 그룹"""
        group = QGroupBox("🔔 알림 설정")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #e91e63;
                border-radius: 6px;
                margin-top: 1ex;
                background-color: #fce4ec;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #c2185b;
            }
        """)
        layout = QVBoxLayout(group)

        # 알림 체크박스들
        notifications = [
            "매수 조건 편입 알림",
            "매수/매도 체결 알림", 
            "손절/트레일링 발동 알림",
            "재매수 차단 알림",
            "일일 실적 요약 알림"
        ]

        checkbox_style = """
            QCheckBox {
                font-size: 10px;
                color: #333;
            }
            QCheckBox::indicator {
                width: 13px;
                height: 13px;
            }
            QCheckBox::indicator:checked {
                background-color: #4caf50;
                border: 1px solid #4caf50;
            }
        """

        for notification in notifications:
            checkbox = QCheckBox(f"✅ {notification}")
            checkbox.setChecked(True)
            checkbox.setStyleSheet(checkbox_style)
            layout.addWidget(checkbox)

        return group

    def create_quick_actions_group(self):
        """빠른 액션 버튼들"""
        group = QGroupBox("🚀 빠른 액션")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #607d8b;
                border-radius: 6px;
                margin-top: 1ex;
                background-color: #f8f9fa;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #455a64;
            }
        """)
        layout = QGridLayout(group)

        # 빠른 액션 버튼들
        actions = [
            ("전체 조건 활성화", "#28a745", self.activate_all_conditions),
            ("전체 조건 비활성화", "#dc3545", self.deactivate_all_conditions),
            ("전량 매도", "#fd7e14", self.sell_all_stocks),
            ("로그 보기", "#6f42c1", self.show_logs),
            ("백업 생성", "#20c997", self.create_backup),
            ("설정 내보내기", "#0dcaf0", self.export_settings)
        ]

        button_style_template = """
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                opacity: 0.8;
            }}
        """

        for i, (text, color, callback) in enumerate(actions):
            button = QPushButton(text)
            button.setStyleSheet(button_style_template.format(color=color))
            if callback:
                button.clicked.connect(callback)
            layout.addWidget(button, i // 3, i % 3)

        return group

    def create_system_status_group(self):
        """시스템 상태 그룹"""
        group = QGroupBox("🖥️ 시스템 상태")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #0277bd;
                border-radius: 6px;
                margin-top: 1ex;
                background-color: #e1f5fe;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #0277bd;
            }
        """)
        layout = QVBoxLayout(group)

        # 연결 상태
        connection_layout = QHBoxLayout()
        
        # 상태 표시 스타일
        status_style = """
            QLabel {
                padding: 3px 8px;
                border-radius: 10px;
                font-size: 10px;
                font-weight: bold;
            }
        """
        
        # API 상태들
        api_status = QLabel("🟢 키움 API: 연결됨")
        api_status.setStyleSheet(status_style + "background-color: #c8e6c9; color: #2e7d32;")
        
        websocket_status = QLabel("🟢 웹소켓: 활성")
        websocket_status.setStyleSheet(status_style + "background-color: #c8e6c9; color: #2e7d32;")
        
        telegram_status = QLabel("🟢 텔레그램: 연결됨")
        telegram_status.setStyleSheet(status_style + "background-color: #c8e6c9; color: #2e7d32;")
        
        db_status = QLabel("🟡 데이터베이스: 동기화중")
        db_status.setStyleSheet(status_style + "background-color: #ffe0b2; color: #f57c00;")

        connection_layout.addWidget(api_status)
        connection_layout.addWidget(websocket_status)
        connection_layout.addWidget(telegram_status)
        connection_layout.addWidget(db_status)
        connection_layout.addStretch()

        layout.addLayout(connection_layout)

        # 시스템 정보
        system_info_layout = QHBoxLayout()
        
        uptime_label = QLabel("가동 시간: 0분")
        last_save_label = QLabel("마지막 저장: 시작")
        version_label = QLabel("버전: v2.0.1")
        
        info_style = "QLabel { color: #666; font-size: 10px; }"
        for label in [uptime_label, last_save_label, version_label]:
            label.setStyleSheet(info_style)
        
        system_info_layout.addWidget(uptime_label)
        system_info_layout.addWidget(last_save_label)
        system_info_layout.addWidget(version_label)
        system_info_layout.addStretch()

        layout.addLayout(system_info_layout)

        return group

    # 빠른 액션 버튼 콜백 함수들 (기본 구현)
    def activate_all_conditions(self):
        """모든 조건식 활성화"""
        log_info("모든 조건식 활성화 요청")
        # TODO: 구현 필요
        
    def deactivate_all_conditions(self):
        """모든 조건식 비활성화"""
        log_info("모든 조건식 비활성화 요청")
        # TODO: 구현 필요
        
    def sell_all_stocks(self):
        """전량 매도"""
        log_info("전량 매도 요청")
        # TODO: 구현 필요
        
    def show_logs(self):
        """로그 보기"""
        log_info("로그 보기 요청")
        # TODO: 구현 필요
        
    def create_backup(self):
        """백업 생성"""
        log_info("백업 생성 요청")
        # TODO: 구현 필요
        
    def export_settings(self):
        """설정 내보내기"""
        log_info("설정 내보내기 요청")
        # TODO: 구현 필요

    def create_buy_settings_tab(self):
        """💰 매수설정 탭 생성"""
        buy_tab = QWidget()
        layout = QVBoxLayout(buy_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # === 조건식 관리 그룹 ===
        condition_group = QGroupBox("📋 매수 조건식 관리")
        condition_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                margin-top: 1ex;
                background-color: #e8f5e9;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: #2e7d32;
            }
        """)
        condition_layout = QVBoxLayout(condition_group)

        # 조건식 선택 및 추가
        condition_control_layout = QHBoxLayout()
        condition_label = QLabel("매수 조건식 목록:")
        condition_label.setStyleSheet("QLabel { font-weight: bold; }")
        condition_control_layout.addWidget(condition_label)

        self.buyConditionComboBox = QComboBox()
        self.buyConditionComboBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.buyConditionComboBox.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
                font-size: 11px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                border: 2px solid #4CAF50;
                width: 6px;
                height: 6px;
            }
        """)
        condition_control_layout.addWidget(self.buyConditionComboBox)

        self.addConditionButton = QPushButton("➕ 조건식 추가")
        self.addConditionButton.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.addConditionButton.clicked.connect(self.add_buy_condition)
        condition_control_layout.addWidget(self.addConditionButton)

        condition_layout.addLayout(condition_control_layout)

        # 선택된 조건식 목록 테이블
        self.buyConditionTableView = QTableView()
        self.buyConditionTableView.setEditTriggers(QTableView.NoEditTriggers)
        self.buyConditionTableView.setMaximumHeight(200)
        self.buyConditionTableView.setStyleSheet("""
            QTableView {
                gridline-color: #ddd;
                background-color: white;
                alternate-background-color: #f5f5f5;
                selection-background-color: #e3f2fd;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 6px;
                border: none;
                font-weight: bold;
            }
        """)
        condition_layout.addWidget(self.buyConditionTableView)

        # 조건식 삭제 버튼
        remove_button_layout = QHBoxLayout()
        self.removeConditionButton = QPushButton("🗑️ 선택된 조건식 삭제")
        self.removeConditionButton.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #c41411;
            }
        """)
        self.removeConditionButton.clicked.connect(self.remove_buy_condition)
        remove_button_layout.addWidget(self.removeConditionButton)
        remove_button_layout.addStretch()
        condition_layout.addLayout(remove_button_layout)

        layout.addWidget(condition_group)

        # === 재매수 방지 설정 ===
        rebuy_group = QGroupBox("🚫 재매수 방지 설정")
        rebuy_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #ff9800;
                border-radius: 8px;
                margin-top: 1ex;
                background-color: #fff3e0;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: #f57c00;
            }
        """)
        rebuy_layout = QVBoxLayout(rebuy_group)

        # 기본 재매수 방지 체크박스
        self.preventSameDayRebuyCheckBox = QCheckBox("당일 매도 종목 재매수 방지")
        self.preventSameDayRebuyCheckBox.setChecked(True)
        self.preventSameDayRebuyCheckBox.setStyleSheet("""
            QCheckBox {
                font-weight: bold;
                font-size: 12px;
                color: #d32f2f;
                padding: 5px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:checked {
                background-color: #f44336;
                border: 2px solid #f44336;
            }
        """)
        rebuy_layout.addWidget(self.preventSameDayRebuyCheckBox)

        # 고급 옵션들
        advanced_layout = QVBoxLayout()

        # 손실 매도만 차단
        self.preventLossRebuyOnlyCheckBox = QCheckBox("손실 매도 종목만 재매수 방지")
        self.preventLossRebuyOnlyCheckBox.setToolTip("수익으로 매도한 종목은 재매수 허용")
        self.preventLossRebuyOnlyCheckBox.setStyleSheet("""
            QCheckBox {
                font-size: 11px;
                color: #333;
                padding: 3px;
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
            }
        """)
        advanced_layout.addWidget(self.preventLossRebuyOnlyCheckBox)

        # 같은 조건식만 차단
        self.preventSameConditionOnlyCheckBox = QCheckBox("같은 조건식으로만 재매수 방지")
        self.preventSameConditionOnlyCheckBox.setToolTip("다른 조건식으로는 재매수 허용")
        self.preventSameConditionOnlyCheckBox.setStyleSheet("""
            QCheckBox {
                font-size: 11px;
                color: #333;
                padding: 3px;
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
            }
        """)
        advanced_layout.addWidget(self.preventSameConditionOnlyCheckBox)

        # 시간 간격 설정
        timeout_layout = QHBoxLayout()
        timeout_layout.addWidget(QLabel("재매수 허용 시간 간격:"))
        self.rebuyTimeoutSpinBox = QSpinBox()
        self.rebuyTimeoutSpinBox.setRange(0, 480)
        self.rebuyTimeoutSpinBox.setValue(60)
        self.rebuyTimeoutSpinBox.setSuffix("분")
        self.rebuyTimeoutSpinBox.setToolTip("매도 후 설정한 시간이 지나면 재매수 허용")
        self.rebuyTimeoutSpinBox.setStyleSheet("""
            QSpinBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
        """)
        timeout_layout.addWidget(self.rebuyTimeoutSpinBox)
        timeout_layout.addStretch()
        advanced_layout.addLayout(timeout_layout)

        rebuy_layout.addLayout(advanced_layout)
        layout.addWidget(rebuy_group)

        # === 매수 금액 및 주문 방식 ===
        buy_settings_group = QGroupBox("💰 매수 금액 및 주문 방식")
        buy_settings_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #2196F3;
                border-radius: 8px;
                margin-top: 1ex;
                background-color: #e3f2fd;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: #1976d2;
            }
        """)
        buy_settings_layout = QVBoxLayout(buy_settings_group)

        # 매수 금액
        amount_layout = QHBoxLayout()
        amount_label = QLabel("매수 금액:")
        amount_label.setStyleSheet("QLabel { font-weight: bold; }")
        amount_layout.addWidget(amount_label)

        self.buyAmountLineEdit = QLineEdit("200,000")
        self.buyAmountLineEdit.setAlignment(Qt.AlignCenter)
        self.buyAmountLineEdit.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #2196F3;
                border-radius: 6px;
                background-color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit:focus {
                border-color: #1976d2;
                background-color: #f3e5f5;
            }
        """)
        self.buyAmountLineEdit.textChanged.connect(lambda: format_number(self.buyAmountLineEdit))
        amount_layout.addWidget(self.buyAmountLineEdit)
        amount_layout.addStretch()

        buy_settings_layout.addLayout(amount_layout)

        # 매수 주문 방식
        order_type_layout = QVBoxLayout()
        order_label = QLabel("주문 방식:")
        order_label.setStyleSheet("QLabel { font-weight: bold; margin-top: 10px; }")
        order_type_layout.addWidget(order_label)

        self.marketBuyRadioButton = QRadioButton("🚀 시장가 매수 (즉시 체결)")
        self.marketBuyRadioButton.setChecked(True)
        self.marketBuyRadioButton.setStyleSheet("""
            QRadioButton {
                font-size: 12px;
                font-weight: bold;
                color: #2196F3;
                padding: 5px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            QRadioButton::indicator:checked {
                background-color: #2196F3;
                border: 2px solid #2196F3;
            }
        """)
        order_type_layout.addWidget(self.marketBuyRadioButton)

        # 지정가 주문 설정
        limit_layout = QHBoxLayout()
        self.limitBuyRadioButton = QRadioButton("📊 현재가 대비")
        self.limitBuyRadioButton.setStyleSheet("""
            QRadioButton {
                font-size: 12px;
                color: #666;
                padding: 5px;
            }
        """)
        
        self.limitBuySpinBox = QSpinBox()
        self.limitBuySpinBox.setRange(-10, 10)
        self.limitBuySpinBox.setValue(0)
        self.limitBuySpinBox.setStyleSheet("""
            QSpinBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
        """)
        
        limit_desc = QLabel("호가로 지정가 주문")
        limit_desc.setStyleSheet("QLabel { color: #666; }")

        limit_layout.addWidget(self.limitBuyRadioButton)
        limit_layout.addWidget(self.limitBuySpinBox)
        limit_layout.addWidget(limit_desc)
        limit_layout.addStretch()
        
        order_type_layout.addLayout(limit_layout)
        buy_settings_layout.addLayout(order_type_layout)

        layout.addWidget(buy_settings_group)

        # 여백 추가
        layout.addStretch()

        # 탭에 추가
        self.main_tab_widget.addTab(buy_tab, "💰 매수설정")

    def create_sell_settings_tab(self):
        """📈 매도설정 탭 생성"""
        sell_tab = QWidget()
        layout = QVBoxLayout(sell_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # === 매도 조건식 설정 ===
        condition_group = QGroupBox("📊 매도 조건식")
        condition_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #9c27b0;
                border-radius: 8px;
                margin-top: 1ex;
                background-color: #f3e5f5;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: #7b1fa2;
            }
        """)
        condition_layout = QHBoxLayout(condition_group)

        condition_label = QLabel("매도 조건식:")
        condition_label.setStyleSheet("QLabel { font-weight: bold; }")
        condition_layout.addWidget(condition_label)

        self.sellConditionComboBox = QComboBox()
        self.sellConditionComboBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.sellConditionComboBox.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #9c27b0;
                border-radius: 4px;
                background-color: white;
                font-size: 12px;
                font-weight: bold;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                border: 2px solid #9c27b0;
                width: 6px;
                height: 6px;
            }
        """)
        condition_layout.addWidget(self.sellConditionComboBox)

        layout.addWidget(condition_group)

        # === 손절 설정 ===
        stop_loss_group = QGroupBox("🔻 손절 설정")
        stop_loss_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #f44336;
                border-radius: 8px;
                margin-top: 1ex;
                background-color: #ffebee;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: #d32f2f;
            }
        """)
        stop_loss_layout = QHBoxLayout(stop_loss_group)

        self.stopLossCheckBox = QCheckBox("평균단가 대비 현재 수익률이")
        self.stopLossCheckBox.setChecked(True)
        self.stopLossCheckBox.setStyleSheet("""
            QCheckBox {
                font-weight: bold;
                font-size: 12px;
                color: #d32f2f;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:checked {
                background-color: #f44336;
                border: 2px solid #f44336;
            }
        """)
        stop_loss_layout.addWidget(self.stopLossCheckBox)

        self.stopLossDoubleSpinBox = QDoubleSpinBox()
        self.stopLossDoubleSpinBox.setRange(-99.0, 99.0)
        self.stopLossDoubleSpinBox.setValue(-2.0)
        self.stopLossDoubleSpinBox.setSingleStep(0.1)
        self.stopLossDoubleSpinBox.setSuffix("%")
        self.stopLossDoubleSpinBox.setStyleSheet("""
            QDoubleSpinBox {
                padding: 8px;
                border: 2px solid #f44336;
                border-radius: 4px;
                background-color: white;
                font-size: 12px;
                font-weight: bold;
                color: #d32f2f;
            }
        """)
        stop_loss_layout.addWidget(self.stopLossDoubleSpinBox)

        stop_loss_desc = QLabel("이하로 내려가면 전량 매도 주문")
        stop_loss_desc.setStyleSheet("QLabel { font-weight: bold; color: #d32f2f; }")
        stop_loss_layout.addWidget(stop_loss_desc)
        stop_loss_layout.addStretch()

        layout.addWidget(stop_loss_group)

        # === 트레일링 스탑 설정 ===
        trailing_group = QGroupBox("📈 트레일링 스탑 설정")
        trailing_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                margin-top: 1ex;
                background-color: #e8f5e9;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: #2e7d32;
            }
        """)
        trailing_layout = QVBoxLayout(trailing_group)

        # 트레일링 발동 조건
        trailing_trigger_layout = QHBoxLayout()
        
        self.trailingStopCheckBox = QCheckBox("평균단가 대비 현재 수익률이")
        self.trailingStopCheckBox.setChecked(True)
        self.trailingStopCheckBox.setStyleSheet("""
            QCheckBox {
                font-weight: bold;
                font-size: 12px;
                color: #2e7d32;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border: 2px solid #4CAF50;
            }
        """)
        trailing_trigger_layout.addWidget(self.trailingStopCheckBox)

        self.trailingStopDoubleSpinBox1 = QDoubleSpinBox()
        self.trailingStopDoubleSpinBox1.setRange(-99.0, 99.0)
        self.trailingStopDoubleSpinBox1.setValue(2.0)
        self.trailingStopDoubleSpinBox1.setSingleStep(0.1)
        self.trailingStopDoubleSpinBox1.setSuffix("%")
        self.trailingStopDoubleSpinBox1.setStyleSheet("""
            QDoubleSpinBox {
                padding: 8px;
                border: 2px solid #4CAF50;
                border-radius: 4px;
                background-color: white;
                font-size: 12px;
                font-weight: bold;
                color: #2e7d32;
            }
        """)
        trailing_trigger_layout.addWidget(self.trailingStopDoubleSpinBox1)

        trailing_trigger_desc = QLabel("이상으로 올라가면 트레일링 발동")
        trailing_trigger_desc.setStyleSheet("QLabel { font-weight: bold; color: #2e7d32; }")
        trailing_trigger_layout.addWidget(trailing_trigger_desc)
        trailing_trigger_layout.addStretch()

        trailing_layout.addLayout(trailing_trigger_layout)

        # 트레일링 매도 조건
        trailing_sell_layout = QHBoxLayout()
        
        trailing_sell_prefix = QLabel("      ↳ 트레일링 발동 이후 고가 대비 등락률(%)이")
        trailing_sell_prefix.setStyleSheet("QLabel { color: #666; font-size: 11px; }")
        trailing_sell_layout.addWidget(trailing_sell_prefix)

        self.trailingStopDoubleSpinBox2 = QDoubleSpinBox()
        self.trailingStopDoubleSpinBox2.setRange(-99.0, 99.0)
        self.trailingStopDoubleSpinBox2.setValue(-1.0)
        self.trailingStopDoubleSpinBox2.setSingleStep(0.1)
        self.trailingStopDoubleSpinBox2.setSuffix("%")
        self.trailingStopDoubleSpinBox2.setStyleSheet("""
            QDoubleSpinBox {
                padding: 6px;
                border: 1px solid #4CAF50;
                border-radius: 4px;
                background-color: white;
                font-size: 11px;
                font-weight: bold;
                color: #2e7d32;
            }
        """)
        trailing_sell_layout.addWidget(self.trailingStopDoubleSpinBox2)

        trailing_sell_desc = QLabel("이하로 내려가면 전량 매도 주문")
        trailing_sell_desc.setStyleSheet("QLabel { color: #666; font-size: 11px; }")
        trailing_sell_layout.addWidget(trailing_sell_desc)
        trailing_sell_layout.addStretch()

        trailing_layout.addLayout(trailing_sell_layout)

        layout.addWidget(trailing_group)

        # === 매도 주문 방식 ===
        sell_order_group = QGroupBox("📤 매도 주문 방식")
        sell_order_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #ff9800;
                border-radius: 8px;
                margin-top: 1ex;
                background-color: #fff3e0;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: #f57c00;
            }
        """)
        sell_order_layout = QVBoxLayout(sell_order_group)

        self.marketSellRadioButton = QRadioButton("🚀 시장가 매도 (즉시 체결)")
        self.marketSellRadioButton.setChecked(True)
        self.marketSellRadioButton.setStyleSheet("""
            QRadioButton {
                font-size: 12px;
                font-weight: bold;
                color: #ff9800;
                padding: 5px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            QRadioButton::indicator:checked {
                background-color: #ff9800;
                border: 2px solid #ff9800;
            }
        """)
        sell_order_layout.addWidget(self.marketSellRadioButton)

        # 지정가 매도 설정
        limit_sell_layout = QHBoxLayout()
        
        self.limitSellRadioButton = QRadioButton("📊 현재가 대비")
        self.limitSellRadioButton.setStyleSheet("""
            QRadioButton {
                font-size: 12px;
                color: #666;
                padding: 5px;
            }
        """)
        
        self.limitSellSpinBox = QSpinBox()
        self.limitSellSpinBox.setRange(-10, 10)
        self.limitSellSpinBox.setValue(0)
        self.limitSellSpinBox.setStyleSheet("""
            QSpinBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
        """)
        
        limit_sell_desc = QLabel("호가로 지정가 주문")
        limit_sell_desc.setStyleSheet("QLabel { color: #666; }")

        limit_sell_layout.addWidget(self.limitSellRadioButton)
        limit_sell_layout.addWidget(self.limitSellSpinBox)
        limit_sell_layout.addWidget(limit_sell_desc)
        limit_sell_layout.addStretch()

        sell_order_layout.addLayout(limit_sell_layout)

        layout.addWidget(sell_order_group)

        # 여백 추가
        layout.addStretch()

        # 탭에 추가
        self.main_tab_widget.addTab(sell_tab, "📈 매도설정")

    def create_account_tab(self):
        """💼 계좌현황 탭 생성"""
        account_tab = QWidget()
        layout = QVBoxLayout(account_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # === 계좌 요약 정보 ===
        summary_group = QGroupBox("📊 계좌 요약")
        summary_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #1976d2;
                border-radius: 8px;
                margin-top: 1ex;
                background-color: #e3f2fd;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: #0d47a1;
            }
        """)
        summary_layout = QGridLayout(summary_group)

        # 계좌 요약 라벨들
        self.account_total_value_label = QLabel("총평가금액: 로딩중...")
        self.account_total_profit_label = QLabel("총수익률: 로딩중...")
        self.account_stock_count_label = QLabel("보유종목: 로딩중...")
        self.account_available_cash_label = QLabel("주문가능금액: 로딩중...")

        # 요약 라벨 스타일
        summary_style = """
            QLabel {
                padding: 8px;
                border-radius: 4px;
                background-color: white;
                border: 1px solid #ddd;
                font-size: 12px;
                font-weight: bold;
            }
        """
        
        self.account_total_value_label.setStyleSheet(summary_style + "color: #1976d2;")
        self.account_total_profit_label.setStyleSheet(summary_style + "color: #4caf50;")
        self.account_stock_count_label.setStyleSheet(summary_style + "color: #ff9800;")
        self.account_available_cash_label.setStyleSheet(summary_style + "color: #9c27b0;")

        summary_layout.addWidget(self.account_total_value_label, 0, 0)
        summary_layout.addWidget(self.account_total_profit_label, 0, 1)
        summary_layout.addWidget(self.account_stock_count_label, 1, 0)
        summary_layout.addWidget(self.account_available_cash_label, 1, 1)

        layout.addWidget(summary_group)

        # === 보유 종목 테이블 ===
        table_group = QGroupBox("📈 보유 종목 현황")
        table_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #4caf50;
                border-radius: 8px;
                margin-top: 1ex;
                background-color: #e8f5e9;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: #2e7d32;
            }
        """)
        table_layout = QVBoxLayout(table_group)

        # 테이블 도구 모음
        table_toolbar = QHBoxLayout()
        
        refresh_table_btn = QPushButton("🔄 새로고침")
        refresh_table_btn.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                padding: 6px 12px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        refresh_table_btn.clicked.connect(self.refresh_account_info)
        table_toolbar.addWidget(refresh_table_btn)

        export_btn = QPushButton("📊 엑셀 내보내기")
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196f3;
                color: white;
                padding: 6px 12px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
        """)
        export_btn.clicked.connect(self.export_account_info)
        table_toolbar.addWidget(export_btn)

        table_toolbar.addStretch()

        # 정렬 옵션
        sort_label = QLabel("정렬:")
        sort_label.setStyleSheet("QLabel { font-weight: bold; }")
        table_toolbar.addWidget(sort_label)

        self.account_sort_combo = QComboBox()
        self.account_sort_combo.addItems(["수익률 높은순", "수익률 낮은순", "보유금액 높은순", "종목명순"])
        self.account_sort_combo.setStyleSheet("""
            QComboBox {
                padding: 4px;
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: white;
                font-size: 10px;
            }
        """)
        self.account_sort_combo.currentTextChanged.connect(self.sort_account_table)
        table_toolbar.addWidget(self.account_sort_combo)

        table_layout.addLayout(table_toolbar)

        # 계좌 정보 테이블
        self.accountInfoTableView = QTableView()
        self.accountInfoTableView.setEditTriggers(QTableView.NoEditTriggers)
        self.accountInfoTableView.setSortingEnabled(True)
        self.accountInfoTableView.setAlternatingRowColors(True)
        self.accountInfoTableView.setSelectionBehavior(QTableView.SelectRows)
        self.accountInfoTableView.horizontalHeader().setStretchLastSection(True)
        self.accountInfoTableView.setStyleSheet("""
            QTableView {
                gridline-color: #ddd;
                background-color: white;
                alternate-background-color: #f8f9fa;
                selection-background-color: #e3f2fd;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #4caf50;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 11px;
            }
            QTableView::item {
                padding: 6px;
                border: none;
            }
            QTableView::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
        """)
        table_layout.addWidget(self.accountInfoTableView)

        layout.addWidget(table_group)

        # 탭에 추가
        self.main_tab_widget.addTab(account_tab, "💼 계좌현황")

    def refresh_account_info(self):
        """계좌 정보 새로고침"""
        log_info("계좌 정보 새로고침 요청")
        self.tr_req_queue.put(dict(action_id="계좌조회"))

    def export_account_info(self):
        """계좌 정보 엑셀 내보내기"""
        log_info("계좌 정보 엑셀 내보내기 요청")
        # TODO: 구현 필요

    def sort_account_table(self, sort_type):
        """계좌 테이블 정렬"""
        log_info(f"계좌 테이블 정렬: {sort_type}")
        # TODO: 구현 필요

    def create_trading_tab(self):
        """📊 매매현황 탭 생성"""
        trading_tab = QWidget()
        layout = QVBoxLayout(trading_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # === 실시간 매매 상태 ===
        status_group = QGroupBox("⚡ 실시간 매매 상태")
        status_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #ff9800;
                border-radius: 8px;
                margin-top: 1ex;
                background-color: #fff3e0;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: #f57c00;
            }
        """)
        status_layout = QGridLayout(status_group)

        # 실시간 상태 라벨들
        self.trading_realtime_count_label = QLabel("실시간 등록: 0/95")
        self.trading_active_count_label = QLabel("자동매매 활성: 0/10")
        self.trading_buy_wait_label = QLabel("매수 대기: 0건")
        self.trading_sell_wait_label = QLabel("매도 대기: 0건")

        # 상태 라벨 스타일
        status_style = """
            QLabel {
                padding: 8px;
                border-radius: 4px;
                background-color: white;
                border: 1px solid #ddd;
                font-size: 12px;
                font-weight: bold;
            }
        """
        
        self.trading_realtime_count_label.setStyleSheet(status_style + "color: #2196f3;")
        self.trading_active_count_label.setStyleSheet(status_style + "color: #4caf50;")
        self.trading_buy_wait_label.setStyleSheet(status_style + "color: #ff9800;")
        self.trading_sell_wait_label.setStyleSheet(status_style + "color: #9c27b0;")

        status_layout.addWidget(self.trading_realtime_count_label, 0, 0)
        status_layout.addWidget(self.trading_active_count_label, 0, 1)
        status_layout.addWidget(self.trading_buy_wait_label, 1, 0)
        status_layout.addWidget(self.trading_sell_wait_label, 1, 1)

        layout.addWidget(status_group)

        # === 종목 관리 도구 ===
        control_group = QGroupBox("🔧 종목 관리 도구")
        control_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #9c27b0;
                border-radius: 8px;
                margin-top: 1ex;
                background-color: #f3e5f5;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: #7b1fa2;
            }
        """)
        control_layout = QVBoxLayout(control_group)

        # 종목 편출 컨트롤
        pop_layout = QHBoxLayout()
        
        pop_label = QLabel("종목 편출:")
        pop_label.setStyleSheet("QLabel { font-weight: bold; }")
        pop_layout.addWidget(pop_label)

        self.popStockCodeLineEdit = QLineEdit("005930")
        self.popStockCodeLineEdit.setAlignment(Qt.AlignCenter)
        self.popStockCodeLineEdit.setMaximumWidth(100)
        self.popStockCodeLineEdit.setPlaceholderText("종목코드")
        self.popStockCodeLineEdit.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #9c27b0;
                border-radius: 4px;
                background-color: white;
                font-size: 12px;
                font-weight: bold;
            }
            QLineEdit:focus {
                border-color: #7b1fa2;
                background-color: #fce4ec;
            }
        """)
        pop_layout.addWidget(self.popStockCodeLineEdit)

        self.popPushButton = QPushButton("🗑️ 리스트 편출")
        self.popPushButton.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #c41411;
            }
        """)
        self.popPushButton.clicked.connect(self.pop_btn_clicked)
        pop_layout.addWidget(self.popPushButton)

        # 일괄 관리 버튼들
        batch_layout = QHBoxLayout()
        
        all_sell_btn = QPushButton("📤 전량 매도")
        all_sell_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff5722;
                color: white;
                padding: 6px 12px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #e64a19;
            }
        """)
        all_sell_btn.clicked.connect(self.sell_all_from_trading)
        batch_layout.addWidget(all_sell_btn)

        clear_all_btn = QPushButton("🧹 전체 정리")
        clear_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #607d8b;
                color: white;
                padding: 6px 12px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #546e7a;
            }
        """)
        clear_all_btn.clicked.connect(self.clear_all_trading)
        batch_layout.addWidget(clear_all_btn)

        pop_layout.addLayout(batch_layout)
        pop_layout.addStretch()

        control_layout.addLayout(pop_layout)
        layout.addWidget(control_group)

        # === 자동매매 현황 테이블 ===
        table_group = QGroupBox("📊 자동매매 현황")
        table_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #4caf50;
                border-radius: 8px;
                margin-top: 1ex;
                background-color: #e8f5e9;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: #2e7d32;
            }
        """)
        table_layout = QVBoxLayout(table_group)

        # 테이블 도구 모음
        table_toolbar = QHBoxLayout()
        
        refresh_trading_btn = QPushButton("🔄 새로고침")
        refresh_trading_btn.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                padding: 6px 12px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        refresh_trading_btn.clicked.connect(self.refresh_trading_status)
        table_toolbar.addWidget(refresh_trading_btn)

        # 필터 옵션
        filter_label = QLabel("필터:")
        filter_label.setStyleSheet("QLabel { font-weight: bold; }")
        table_toolbar.addWidget(filter_label)

        self.trading_filter_combo = QComboBox()
        self.trading_filter_combo.addItems(["전체", "매수 대기", "보유중", "매도 대기", "손익 종목만"])
        self.trading_filter_combo.setStyleSheet("""
            QComboBox {
                padding: 4px;
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: white;
                font-size: 10px;
            }
        """)
        self.trading_filter_combo.currentTextChanged.connect(self.filter_trading_table)
        table_toolbar.addWidget(self.trading_filter_combo)

        table_toolbar.addStretch()

        table_layout.addLayout(table_toolbar)

        # 자동매매 현황 테이블
        self.autoTradeInfoTableView = QTableView()
        self.autoTradeInfoTableView.setEditTriggers(QTableView.NoEditTriggers)
        self.autoTradeInfoTableView.setSortingEnabled(True)
        self.autoTradeInfoTableView.setAlternatingRowColors(True)
        self.autoTradeInfoTableView.setSelectionBehavior(QTableView.SelectRows)
        self.autoTradeInfoTableView.horizontalHeader().setStretchLastSection(True)
        self.autoTradeInfoTableView.setStyleSheet("""
            QTableView {
                gridline-color: #ddd;
                background-color: white;
                alternate-background-color: #f8f9fa;
                selection-background-color: #e8f5e9;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #4caf50;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 11px;
            }
            QTableView::item {
                padding: 6px;
                border: none;
            }
            QTableView::item:selected {
                background-color: #e8f5e9;
                color: #2e7d32;
            }
        """)
        table_layout.addWidget(self.autoTradeInfoTableView)

        layout.addWidget(table_group)

        # 탭에 추가
        self.main_tab_widget.addTab(trading_tab, "📊 매매현황")

    def sell_all_from_trading(self):
        """매매현황에서 전량 매도"""
        log_info("매매현황 전량 매도 요청")
        # TODO: 구현 필요

    def clear_all_trading(self):
        """매매현황 전체 정리"""
        log_info("매매현황 전체 정리 요청")
        # TODO: 구현 필요

    def refresh_trading_status(self):
        """매매 상태 새로고침"""
        log_info("매매 상태 새로고침")
        # TODO: 실시간 상태 라벨 업데이트

    def filter_trading_table(self, filter_type):
        """매매현황 테이블 필터링"""
        log_info(f"매매현황 테이블 필터링: {filter_type}")
        # TODO: 구현 필요

    def create_sell_records_tab(self):
        """📋 매도기록 탭 생성"""
        records_tab = QWidget()
        layout = QVBoxLayout(records_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # === 당일 매도 통계 ===
        stats_group = QGroupBox("📊 당일 매도 통계")
        stats_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #3f51b5;
                border-radius: 8px;
                margin-top: 1ex;
                background-color: #e8eaf6;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: #303f9f;
            }
        """)
        stats_layout = QVBoxLayout(stats_group)

        # 메인 통계 라벨
        self.soldStatsLabel = QLabel("당일 매도 통계: 로딩 중...")
        self.soldStatsLabel.setStyleSheet("""
            QLabel {
                padding: 12px;
                border-radius: 6px;
                background-color: white;
                border: 2px solid #3f51b5;
                font-size: 14px;
                font-weight: bold;
                color: #1976d2;
            }
        """)
        stats_layout.addWidget(self.soldStatsLabel)

        # 상세 통계 그리드
        detail_stats_layout = QGridLayout()

        # 상세 통계 라벨들
        self.sold_total_count_label = QLabel("총 매도: 0건")
        self.sold_win_count_label = QLabel("수익 매도: 0건")
        self.sold_loss_count_label = QLabel("손실 매도: 0건")
        self.sold_win_rate_label = QLabel("승률: 0%")
        self.sold_avg_profit_label = QLabel("평균수익률: 0%")
        self.sold_total_amount_label = QLabel("총 매도금액: 0원")

        # 상세 통계 스타일
        detail_style = """
            QLabel {
                padding: 6px;
                border-radius: 4px;
                background-color: white;
                border: 1px solid #ddd;
                font-size: 11px;
                font-weight: bold;
            }
        """

        self.sold_total_count_label.setStyleSheet(detail_style + "color: #3f51b5;")
        self.sold_win_count_label.setStyleSheet(detail_style + "color: #4caf50;")
        self.sold_loss_count_label.setStyleSheet(detail_style + "color: #f44336;")
        self.sold_win_rate_label.setStyleSheet(detail_style + "color: #ff9800;")
        self.sold_avg_profit_label.setStyleSheet(detail_style + "color: #9c27b0;")
        self.sold_total_amount_label.setStyleSheet(detail_style + "color: #607d8b;")

        detail_stats_layout.addWidget(self.sold_total_count_label, 0, 0)
        detail_stats_layout.addWidget(self.sold_win_count_label, 0, 1)
        detail_stats_layout.addWidget(self.sold_loss_count_label, 0, 2)
        detail_stats_layout.addWidget(self.sold_win_rate_label, 1, 0)
        detail_stats_layout.addWidget(self.sold_avg_profit_label, 1, 1)
        detail_stats_layout.addWidget(self.sold_total_amount_label, 1, 2)

        stats_layout.addLayout(detail_stats_layout)
        layout.addWidget(stats_group)

        # === 조건식별 성과 분석 ===
        condition_group = QGroupBox("📈 조건식별 성과 분석")
        condition_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #4caf50;
                border-radius: 8px;
                margin-top: 1ex;
                background-color: #e8f5e9;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: #2e7d32;
            }
        """)
        condition_layout = QHBoxLayout(condition_group)

        # 조건식 성과 요약 라벨들
        self.condition_performance_labels = {}
        for i in range(3):  # 최대 3개 조건식 표시
            label = QLabel(f"조건식{i+1}: 데이터 없음")
            label.setStyleSheet("""
                QLabel {
                    padding: 8px;
                    border-radius: 4px;
                    background-color: white;
                    border: 1px solid #ddd;
                    font-size: 10px;
                    font-weight: bold;
                    color: #2e7d32;
                }
            """)
            self.condition_performance_labels[f"condition_{i+1}"] = label
            condition_layout.addWidget(label)

        condition_layout.addStretch()
        layout.addWidget(condition_group)

        # === 매도기록 관리 도구 ===
        control_group = QGroupBox("🔧 매도기록 관리")
        control_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #ff9800;
                border-radius: 8px;
                margin-top: 1ex;
                background-color: #fff3e0;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: #f57c00;
            }
        """)
        control_layout = QHBoxLayout(control_group)

        # 새로고침 버튼
        refresh_sold_btn = QPushButton("🔄 통계 새로고침")
        refresh_sold_btn.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        refresh_sold_btn.clicked.connect(self.refresh_sold_stocks_stats)
        control_layout.addWidget(refresh_sold_btn)

        # 엑셀 내보내기 버튼
        export_sold_btn = QPushButton("📊 엑셀 내보내기")
        export_sold_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196f3;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
        """)
        export_sold_btn.clicked.connect(self.export_sold_records)
        control_layout.addWidget(export_sold_btn)

        # 데이터 초기화 버튼 (주의)
        clear_sold_btn = QPushButton("🗑️ 기록 초기화")
        clear_sold_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        clear_sold_btn.clicked.connect(self.clear_sold_records)
        control_layout.addWidget(clear_sold_btn)

        control_layout.addStretch()

        # 필터 옵션
        filter_label = QLabel("필터:")
        filter_label.setStyleSheet("QLabel { font-weight: bold; }")
        control_layout.addWidget(filter_label)

        self.sold_filter_combo = QComboBox()
        self.sold_filter_combo.addItems(["전체", "수익 매도만", "손실 매도만", "조건식별", "시간대별"])
        self.sold_filter_combo.setStyleSheet("""
            QComboBox {
                padding: 6px;
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: white;
                font-size: 10px;
            }
        """)
        self.sold_filter_combo.currentTextChanged.connect(self.filter_sold_records)
        control_layout.addWidget(self.sold_filter_combo)

        layout.addWidget(control_group)

        # === 매도기록 테이블 ===
        table_group = QGroupBox("📋 매도기록 상세")
        table_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #9c27b0;
                border-radius: 8px;
                margin-top: 1ex;
                background-color: #f3e5f5;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: #7b1fa2;
            }
        """)
        table_layout = QVBoxLayout(table_group)

        # 매도기록 테이블
        self.soldStocksTableView = QTableView()
        self.soldStocksTableView.setEditTriggers(QTableView.NoEditTriggers)
        self.soldStocksTableView.setSortingEnabled(True)
        self.soldStocksTableView.setAlternatingRowColors(True)
        self.soldStocksTableView.setSelectionBehavior(QTableView.SelectRows)
        self.soldStocksTableView.horizontalHeader().setStretchLastSection(True)
        self.soldStocksTableView.setStyleSheet("""
            QTableView {
                gridline-color: #ddd;
                background-color: white;
                alternate-background-color: #fafafa;
                selection-background-color: #f3e5f5;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #9c27b0;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 11px;
            }
            QTableView::item {
                padding: 6px;
                border: none;
            }
            QTableView::item:selected {
                background-color: #f3e5f5;
                color: #7b1fa2;
            }
        """)
        table_layout.addWidget(self.soldStocksTableView)

        layout.addWidget(table_group)

        # 탭에 추가
        self.main_tab_widget.addTab(records_tab, "📋 매도기록")

    def export_sold_records(self):
        """매도기록 엑셀 내보내기"""
        log_info("매도기록 엑셀 내보내기 요청")
        # TODO: 구현 필요

    def clear_sold_records(self):
        """매도기록 초기화 (주의)"""
        log_info("매도기록 초기화 요청")
        # TODO: 확인 다이얼로그 + 구현 필요

    def filter_sold_records(self, filter_type):
        """매도기록 테이블 필터링"""
        log_info(f"매도기록 필터링: {filter_type}")
        # TODO: 구현 필요

    def create_log_tab(self):
        """📝 로그/알림 탭 생성"""
        log_tab = QWidget()
        layout = QVBoxLayout(log_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # === 텔레그램 알림 설정 ===
        telegram_group = QGroupBox("📱 텔레그램 알림 설정")
        telegram_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #25d366;
                border-radius: 8px;
                margin-top: 1ex;
                background-color: #e8f5e8;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #25d366;
            }
        """)
        telegram_layout = QGridLayout(telegram_group)
        telegram_layout.setSpacing(10)

        # 텔레그램 설정 정보 표시
        info_label = QLabel("현재 텔레그램 설정:")
        info_label.setStyleSheet("font-weight: bold; color: #333;")
        telegram_layout.addWidget(info_label, 0, 0, 1, 2)

        # 봇 토큰 표시 (마스킹)
        try:
            token_display = TELEGRAM_CONFIG.get('bot_token', 'Not configured')
            if token_display and token_display != 'Not configured':
                masked_token = token_display[:10] + "..." + token_display[-5:] if len(token_display) > 15 else token_display
            else:
                masked_token = "설정되지 않음"
        except:
            masked_token = "설정되지 않음"
        
        bot_label = QLabel("봇 토큰:")
        bot_value = QLabel(masked_token)
        bot_value.setStyleSheet("color: #666; font-family: monospace;")
        telegram_layout.addWidget(bot_label, 1, 0)
        telegram_layout.addWidget(bot_value, 1, 1)

        # 채팅 ID 표시
        try:
            chat_id_display = str(TELEGRAM_CONFIG.get('chat_id', 'Not configured'))
        except:
            chat_id_display = "설정되지 않음"
        
        chat_label = QLabel("채팅 ID:")
        chat_value = QLabel(chat_id_display)
        chat_value.setStyleSheet("color: #666; font-family: monospace;")
        telegram_layout.addWidget(chat_label, 2, 0)
        telegram_layout.addWidget(chat_value, 2, 1)

        # 연결 테스트 버튼
        self.test_telegram_button = QPushButton("📡 연결 테스트")
        self.test_telegram_button.setStyleSheet("""
            QPushButton {
                background-color: #25d366;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #128c7e;
            }
            QPushButton:pressed {
                background-color: #075e54;
            }
        """)
        self.test_telegram_button.clicked.connect(self.test_telegram_connection)
        telegram_layout.addWidget(self.test_telegram_button, 3, 0, 1, 2)

        layout.addWidget(telegram_group)

        # === 알림 유형 설정 ===
        notification_group = QGroupBox("🔔 알림 유형 설정")
        notification_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #ff9800;
                border-radius: 8px;
                margin-top: 1ex;
                background-color: #fff3e0;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #ff9800;
            }
        """)
        notification_layout = QGridLayout(notification_group)
        notification_layout.setSpacing(10)

        # 알림 체크박스들 (기존 코드에서 사용되는 이름들 유지)
        self.notify_start_checkbox = QCheckBox("🚀 매매 시작/종료")
        self.notify_buy_checkbox = QCheckBox("💰 매수 주문")
        self.notify_sell_checkbox = QCheckBox("📈 매도 주문")
        self.notify_error_checkbox = QCheckBox("❌ 오류 발생")
        self.notify_summary_checkbox = QCheckBox("📊 일일 요약")

        checkboxes = [
            self.notify_start_checkbox,
            self.notify_buy_checkbox,
            self.notify_sell_checkbox,
            self.notify_error_checkbox,
            self.notify_summary_checkbox
        ]

        checkbox_style = """
            QCheckBox {
                font-size: 12px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #ccc;
                background-color: white;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #ff9800;
                background-color: #ff9800;
                border-radius: 3px;
            }
        """

        for i, checkbox in enumerate(checkboxes):
            checkbox.setStyleSheet(checkbox_style)
            checkbox.setChecked(True)  # 기본적으로 모든 알림 활성화
            row = i // 2
            col = i % 2
            notification_layout.addWidget(checkbox, row, col)

        layout.addWidget(notification_group)

        # === 실시간 로그 영역 ===
        log_group = QGroupBox("📋 실시간 시스템 로그")
        log_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #2196f3;
                border-radius: 8px;
                margin-top: 1ex;
                background-color: #e3f2fd;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #2196f3;
            }
        """)
        log_layout = QVBoxLayout(log_group)
        log_layout.setSpacing(10)

        # 로그 제어 버튼들
        log_controls = QHBoxLayout()
        
        self.clear_log_button = QPushButton("🧹 로그 클리어")
        self.save_log_button = QPushButton("💾 로그 저장")
        self.refresh_log_button = QPushButton("🔄 새로고침")

        button_style = """
            QPushButton {
                background-color: #2196f3;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """

        for button in [self.clear_log_button, self.save_log_button, self.refresh_log_button]:
            button.setStyleSheet(button_style)

        self.clear_log_button.clicked.connect(self.clear_realtime_log)
        self.save_log_button.clicked.connect(self.save_realtime_log)
        self.refresh_log_button.clicked.connect(self.refresh_realtime_log)

        log_controls.addWidget(self.clear_log_button)
        log_controls.addWidget(self.save_log_button)
        log_controls.addWidget(self.refresh_log_button)
        log_controls.addStretch()
        
        log_layout.addLayout(log_controls)

        # 실시간 로그 표시 영역
        from PyQt5.QtWidgets import QPlainTextEdit
        self.realtime_log_display = QPlainTextEdit()
        self.realtime_log_display.setReadOnly(True)
        self.realtime_log_display.setStyleSheet("""
            QPlainTextEdit {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
                padding: 8px;
            }
        """)
        self.realtime_log_display.setMaximumBlockCount(1000)  # 최대 1000줄 유지
        log_layout.addWidget(self.realtime_log_display)

        layout.addWidget(log_group)

        # === 시스템 정보 ===
        system_group = QGroupBox("ℹ️ 시스템 정보")
        system_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #9c27b0;
                border-radius: 8px;
                margin-top: 1ex;
                background-color: #f3e5f5;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #9c27b0;
            }
        """)
        system_layout = QGridLayout(system_group)
        system_layout.setSpacing(8)

        # 시스템 정보 라벨들
        version_label = QLabel("프로그램 버전:")
        version_value = QLabel("v2.0 (탭 기반 UI)")
        
        start_time_label = QLabel("시작 시간:")
        self.start_time_value = QLabel(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        uptime_label = QLabel("가동 시간:")
        self.uptime_value = QLabel("00:00:00")
        
        system_layout.addWidget(version_label, 0, 0)
        system_layout.addWidget(version_value, 0, 1)
        system_layout.addWidget(start_time_label, 1, 0)
        system_layout.addWidget(self.start_time_value, 1, 1)
        system_layout.addWidget(uptime_label, 2, 0)
        system_layout.addWidget(self.uptime_value, 2, 1)

        # 스타일 적용
        info_style = "color: #666; font-family: monospace;"
        version_value.setStyleSheet(info_style)
        self.start_time_value.setStyleSheet(info_style)
        self.uptime_value.setStyleSheet(info_style)

        layout.addWidget(system_group)

        # 레이아웃 비율 설정
        layout.setStretchFactor(telegram_group, 0)
        layout.setStretchFactor(notification_group, 0)
        layout.setStretchFactor(log_group, 1)  # 로그 영역이 가장 많은 공간 차지
        layout.setStretchFactor(system_group, 0)

        self.main_tab_widget.addTab(log_tab, "📝 로그/알림")

        # 로그 업데이트 타이머 설정
        self.log_update_timer = QTimer()
        self.log_update_timer.timeout.connect(self.update_realtime_log)
        self.log_update_timer.start(5000)  # 5초마다 업데이트

        # 가동시간 업데이트 타이머
        self.uptime_timer = QTimer()
        self.uptime_timer.timeout.connect(self.update_uptime)
        self.uptime_timer.start(1000)  # 1초마다 업데이트
        
        self.start_time = datetime.datetime.now()

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
        
        # 실시간 로그 업데이트
        if hasattr(self, 'add_realtime_log'):
            self.add_realtime_log("SUCCESS", "🚀 자동매매 시작")
        
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
        
        # 실시간 로그 업데이트
        if hasattr(self, 'add_realtime_log'):
            self.add_realtime_log("INFO", "⏹️ 자동매매 종료")
        
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
        
        # 인스턴스 변수로 저장
        self.account_info_dict = account_info_dict

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
        self.update_account_tab_labels()  # 탭 UI 라벨 업데이트
        self.has_init = True
        log_info("계좌정보 처리 완료")

    def update_account_tab_labels(self):
        """계좌현황 탭의 라벨들을 실제 데이터로 업데이트"""
        try:
            if hasattr(self, 'account_info_dict') and self.account_info_dict:
                # 총평가금액
                total_value = self.account_info_dict.get('총평가금액', 0)
                if hasattr(self, 'account_total_value_label'):
                    self.account_total_value_label.setText(f"총평가금액: {total_value:,}원")
                
                # 총수익률
                total_profit_rate = self.account_info_dict.get('총수익률', 0)
                if hasattr(self, 'account_total_profit_label'):
                    profit_color = "red" if total_profit_rate < 0 else "blue"
                    self.account_total_profit_label.setText(f"총수익률: {total_profit_rate:.2f}%")
                    self.account_total_profit_label.setStyleSheet(f"color: {profit_color}; font-weight: bold;")
                
                # 보유종목 수
                stock_count = len(self.account_info_df) if hasattr(self, 'account_info_df') else 0
                if hasattr(self, 'account_stock_count_label'):
                    self.account_stock_count_label.setText(f"보유종목: {stock_count}개")
                
                # 주문가능금액 (추정치)
                available_cash = self.account_info_dict.get('주문가능금액', 0)
                if hasattr(self, 'account_available_cash_label'):
                    self.account_available_cash_label.setText(f"주문가능금액: {available_cash:,}원")
                
                log_debug("계좌현황 탭 라벨 업데이트 완료")
            else:
                log_debug("계좌 정보가 아직 로드되지 않음")
        except Exception as e:
            log_error(f"계좌현황 탭 라벨 업데이트 실패: {str(e)}")

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

    # === 로그/알림 탭 관련 메서드들 ===
    def test_telegram_connection(self):
        """텔레그램 연결 테스트"""
        try:
            notifier = get_telegram_notifier()
            if notifier:
                # 테스트 메시지 전송
                test_message = "🔔 키움증권 자동매매 프로그램\n텔레그램 연결 테스트 성공!"
                notifier.send_message(test_message)
                self.add_realtime_log("INFO", "텔레그램 연결 테스트 성공")
                log_info("텔레그램 연결 테스트 성공")
            else:
                self.add_realtime_log("ERROR", "텔레그램 연결 실패 - notifier가 None")
                log_error("텔레그램 연결 실패 - notifier가 None")
        except Exception as e:
            self.add_realtime_log("ERROR", f"텔레그램 연결 테스트 실패: {str(e)}")
            log_error(f"텔레그램 연결 테스트 실패: {str(e)}")

    def clear_realtime_log(self):
        """실시간 로그 클리어"""
        self.realtime_log_display.clear()
        self.add_realtime_log("INFO", "로그가 클리어되었습니다")

    def save_realtime_log(self):
        """실시간 로그 저장"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"realtime_log_{timestamp}.txt"
            log_content = self.realtime_log_display.toPlainText()
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(log_content)
            
            self.add_realtime_log("INFO", f"로그가 {filename}에 저장되었습니다")
            log_info(f"실시간 로그 저장 완료: {filename}")
        except Exception as e:
            self.add_realtime_log("ERROR", f"로그 저장 실패: {str(e)}")
            log_error(f"로그 저장 실패: {str(e)}")

    def refresh_realtime_log(self):
        """실시간 로그 새로고침"""
        self.add_realtime_log("INFO", "로그 새로고침 완료")

    def add_realtime_log(self, level, message):
        """실시간 로그에 메시지 추가"""
        try:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            
            # 레벨별 이모지 설정
            if level == "ERROR":
                emoji = "❌"
            elif level == "WARNING":
                emoji = "⚠️"
            elif level == "INFO":
                emoji = "ℹ️"
            elif level == "SUCCESS":
                emoji = "✅"
            else:
                emoji = "📋"

            # 플레인 텍스트 형태로 로그 추가
            text_message = f"[{timestamp}] {emoji} {level}: {message}"
            
            if hasattr(self, 'realtime_log_display'):
                self.realtime_log_display.appendPlainText(text_message)
                
                # 스크롤을 맨 아래로 이동
                scrollbar = self.realtime_log_display.verticalScrollBar()
                scrollbar.setValue(scrollbar.maximum())
            
        except Exception as e:
            print(f"로그 추가 실패: {str(e)}")

    def update_realtime_log(self):
        """실시간 로그 업데이트 (주기적으로 호출)"""
        # 여기서는 시스템 상태 등을 주기적으로 로그에 추가할 수 있습니다
        pass

    def update_uptime(self):
        """가동시간 업데이트"""
        try:
            if hasattr(self, 'start_time') and hasattr(self, 'uptime_value'):
                uptime = datetime.datetime.now() - self.start_time
                hours, remainder = divmod(int(uptime.total_seconds()), 3600)
                minutes, seconds = divmod(remainder, 60)
                uptime_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                self.uptime_value.setText(uptime_str)
        except Exception as e:
            log_error(f"가동시간 업데이트 실패: {str(e)}")


sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    log_error(f"시스템 예외 발생 - exctype: {exctype}, value: {value}, traceback: {traceback}")
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = my_exception_hook

if __name__ == "__main__":
    def test_telegram_connection(self):
        """텔레그램 연결 테스트"""
        try:
            notifier = get_telegram_notifier()
            if notifier:
                # 테스트 메시지 전송
                test_message = "🔔 키움증권 자동매매 프로그램\n텔레그램 연결 테스트 성공!"
                notifier.send_message(test_message)
                self.add_realtime_log("INFO", "텔레그램 연결 테스트 성공")
                log_info("텔레그램 연결 테스트 성공")
            else:
                self.add_realtime_log("ERROR", "텔레그램 연결 실패 - notifier가 None")
                log_error("텔레그램 연결 실패 - notifier가 None")
        except Exception as e:
            self.add_realtime_log("ERROR", f"텔레그램 연결 테스트 실패: {str(e)}")
            log_error(f"텔레그램 연결 테스트 실패: {str(e)}")

    def clear_realtime_log(self):
        """실시간 로그 클리어"""
        self.realtime_log_display.clear()
        self.add_realtime_log("INFO", "로그가 클리어되었습니다")

    def save_realtime_log(self):
        """실시간 로그 저장"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"realtime_log_{timestamp}.txt"
            log_content = self.realtime_log_display.toPlainText()
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(log_content)
            
            self.add_realtime_log("INFO", f"로그가 {filename}에 저장되었습니다")
            log_info(f"실시간 로그 저장 완료: {filename}")
        except Exception as e:
            self.add_realtime_log("ERROR", f"로그 저장 실패: {str(e)}")
            log_error(f"로그 저장 실패: {str(e)}")

    def refresh_realtime_log(self):
        """실시간 로그 새로고침"""
        self.add_realtime_log("INFO", "로그 새로고침 완료")

    def add_realtime_log(self, level, message):
        """실시간 로그에 메시지 추가"""
        try:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            
            # 레벨별 색상 설정
            if level == "ERROR":
                color = "red"
                emoji = "❌"
            elif level == "WARNING":
                color = "orange"
                emoji = "⚠️"
            elif level == "INFO":
                color = "blue"
                emoji = "ℹ️"
            elif level == "SUCCESS":
                color = "green"
                emoji = "✅"
            else:
                color = "black"
                emoji = "📋"

            # HTML 형태로 로그 추가
            html_message = f'''
            <div style="margin: 2px 0;">
                <span style="color: #666; font-size: 10px;">[{timestamp}]</span>
                <span style="color: {color}; font-weight: bold;">{emoji} {level}</span>
                <span style="color: #333;"> {message}</span>
            </div>
            '''
            
            self.realtime_log_display.append(html_message)
            
            # 스크롤을 맨 아래로 이동
            scrollbar = self.realtime_log_display.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
            
        except Exception as e:
            print(f"로그 추가 실패: {str(e)}")

    def update_realtime_log(self):
        """실시간 로그 업데이트 (주기적으로 호출)"""
        # 여기서는 시스템 상태 등을 주기적으로 로그에 추가할 수 있습니다
        pass

    def update_uptime(self):
        """가동시간 업데이트"""
        try:
            if hasattr(self, 'start_time'):
                uptime = datetime.datetime.now() - self.start_time
                hours, remainder = divmod(int(uptime.total_seconds()), 3600)
                minutes, seconds = divmod(remainder, 60)
                uptime_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                self.uptime_value.setText(uptime_str)
        except Exception as e:
            log_error(f"가동시간 업데이트 실패: {str(e)}")

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