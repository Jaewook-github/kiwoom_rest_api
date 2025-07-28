import os
import sys
import time
import datetime
from collections import deque
from multiprocessing import Process, Queue

from loguru import logger
import pandas as pd
from PyQt5.QtCore import Qt, QSettings, QTimer, QAbstractTableModel, QTime, pyqtSignal, QAbstractListModel
from PyQt5.QtGui import QColor, QFont, QPalette, QIcon
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QGroupBox, QLabel, QLineEdit, QPushButton, QSpinBox, QDoubleSpinBox,
    QCheckBox, QRadioButton, QComboBox, QTableView, QTimeEdit, QTabWidget,
    QMessageBox, QSplitter, QFrame, QProgressBar, QTextEdit, QScrollArea,
    QButtonGroup, QFormLayout, QStatusBar, QMenuBar, QAction, QSizePolicy,
    QListWidget, QListWidgetItem, QDialog, QDialogButtonBox, QHeaderView,
    QFileDialog
)

# 커스텀 모듈 import (실제 환경에서는 해당 파일들이 있어야 함)
from tr_process_functions import tr_general_req_func, tr_order_req_func
from websocket_functions import run_websocket
from utils import log_exceptions

# 상수 정의
MAX_REALTIME_COUNT = 95
TRANSACTION_COST = 0.18
DEFAULT_AMEND_TIME = 60



class ConditionScheduleModel(QAbstractTableModel):
    """조건식 스케줄 테이블 모델"""

    def __init__(self, schedules):
        super().__init__()
        self.schedules = schedules
        self.headers = ["조건식명", "시작시간", "종료시간", "활성화"]

    def rowCount(self, parent=None):
        return len(self.schedules)

    def columnCount(self, parent=None):
        return len(self.headers)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]
        return None

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()
        schedule = list(self.schedules.values())[row]
        condition_name = list(self.schedules.keys())[row]

        if role == Qt.DisplayRole:
            if col == 0:  # 조건식명
                return condition_name
            elif col == 1:  # 시작시간
                return schedule.get('start_time', '09:00:00')
            elif col == 2:  # 종료시간
                return schedule.get('end_time', '15:30:00')
            elif col == 3:  # 활성화
                return "✓" if schedule.get('enabled', True) else "✗"
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        elif role == Qt.CheckStateRole and col == 3:
            return Qt.Checked if schedule.get('enabled', True) else Qt.Unchecked

        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable

        # 시간 컬럼들은 편집 가능
        if index.column() in [1, 2]:
            flags |= Qt.ItemIsEditable
        elif index.column() == 3:  # 활성화 컬럼
            flags |= Qt.ItemIsUserCheckable

        return flags

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False

        row = index.row()
        col = index.column()
        condition_name = list(self.schedules.keys())[row]

        if role == Qt.EditRole:
            if col == 1:  # 시작시간
                try:
                    # 시간 형식 검증
                    datetime.datetime.strptime(str(value), '%H:%M:%S')
                    self.schedules[condition_name]['start_time'] = str(value)
                    self.dataChanged.emit(index, index)
                    return True
                except ValueError:
                    return False
            elif col == 2:  # 종료시간
                try:
                    datetime.datetime.strptime(str(value), '%H:%M:%S')
                    self.schedules[condition_name]['end_time'] = str(value)
                    self.dataChanged.emit(index, index)
                    return True
                except ValueError:
                    return False
        elif role == Qt.CheckStateRole and col == 3:
            self.schedules[condition_name]['enabled'] = (value == Qt.Checked)
            self.dataChanged.emit(index, index)
            return True

        return False

    def update_data(self, schedules):
        self.beginResetModel()
        self.schedules = schedules
        self.endResetModel()

    def get_data(self):
        return self.schedules


class ConditionTimeDialog(QDialog):
    """조건식별 시간 설정 다이얼로그"""

    def __init__(self, condition_schedules, parent=None):
        super().__init__(parent)
        self.condition_schedules = condition_schedules.copy()
        self.setup_ui()
        self.load_schedules()

    def setup_ui(self):
        self.setWindowTitle("조건식별 매매시간 설정")
        self.setModal(True)
        self.resize(600, 400)

        layout = QVBoxLayout(self)

        # 설명 라벨
        info_label = QLabel("각 조건식별로 매매 시작/종료 시간을 설정하세요.")
        info_label.setStyleSheet("color: #666; font-size: 12px; margin-bottom: 10px;")
        layout.addWidget(info_label)

        # 테이블 위젯
        self.table_widget = QTableView()
        self.table_model = ConditionScheduleModel(self.condition_schedules)
        self.table_widget.setModel(self.table_model)

        # 테이블 설정
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setSelectionBehavior(QTableView.SelectRows)
        header = self.table_widget.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)

        layout.addWidget(self.table_widget)

        # 버튼 박스
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def load_schedules(self):
        """기존 스케줄 로드"""
        self.table_model.update_data(self.condition_schedules)

    def get_schedules(self):
        """설정된 스케줄 반환"""
        return self.table_model.get_data()


# ==========================================
# 🔧 기존 FlexibleSellConditionWidget 클래스를 이것으로 교체하세요!
# ==========================================

import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QListWidget, QListWidgetItem, QRadioButton,
    QButtonGroup, QDialog, QMessageBox
)


class FlexibleSellConditionWidget(QWidget):
    """개선된 유연한 매도 조건 위젯 (완전한 버전)"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.condition_schedules = {}  # 조건식별 시간 스케줄
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # 타이틀 및 시간 설정 버튼
        title_layout = QHBoxLayout()

        title_label = QLabel("📊 조건식 관리")
        title_label.setStyleSheet("""
            QLabel {
                font-weight: bold; 
                font-size: 16px;
                color: #2196F3;
                padding: 5px;
            }
        """)
        title_layout.addWidget(title_label)

        # 개선된 시간 설정 버튼
        self.time_setting_button = QPushButton("⏰ 쉬운 시간 설정")
        self.time_setting_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #FF9800, stop:1 #F57C00);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #F57C00, stop:1 #E65100);
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                transform: translateY(1px);
            }
        """)
        self.time_setting_button.clicked.connect(self.open_time_setting_dialog)
        title_layout.addWidget(self.time_setting_button)

        # 상태 표시 라벨
        self.status_label = QLabel("⏰ 시간 설정: 기본값 (09:00~15:30)")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #666;
                font-size: 11px;
                padding: 3px;
                background-color: #f0f0f0;
                border-radius: 4px;
            }
        """)
        title_layout.addWidget(self.status_label)

        title_layout.addStretch()
        layout.addLayout(title_layout)

        # 매수 조건식 그룹 (개선된 디자인)
        buy_group = QGroupBox("🔵 매수 조건식 (최소 3개 선택)")
        buy_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #4CAF50;
                border-radius: 10px;
                margin-top: 1ex;
                padding-top: 15px;
                background-color: #f8fff8;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
                background-color: white;
                color: #4CAF50;
                font-size: 13px;
            }
        """)
        buy_layout = QVBoxLayout(buy_group)

        self.buy_condition_list = QListWidget()
        self.buy_condition_list.setSelectionMode(QListWidget.MultiSelection)
        self.buy_condition_list.setMaximumHeight(130)
        self.buy_condition_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #e8f5e8;
                border-radius: 6px;
                background-color: white;
                selection-background-color: #4CAF50;
                selection-color: white;
                font-size: 11px;
            }
            QListWidget::item {
                padding: 6px;
                border-bottom: 1px solid #f0f0f0;
            }
            QListWidget::item:hover {
                background-color: #e8f5e8;
            }
            QListWidget::item:selected {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
            }
        """)
        buy_layout.addWidget(self.buy_condition_list)

        layout.addWidget(buy_group)

        # 매도 조건식 그룹 (개선된 디자인)
        sell_group = QGroupBox("🔴 매도 조건식 설정")
        sell_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #FF5722;
                border-radius: 10px;
                margin-top: 1ex;
                padding-top: 15px;
                background-color: #fff8f8;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
                background-color: white;
                color: #FF5722;
                font-size: 13px;
            }
        """)
        sell_layout = QVBoxLayout(sell_group)

        # 매도 방식 선택 (개선된 라디오버튼)
        self.sell_mode_group = QButtonGroup()

        self.auto_sell_only_radio = QRadioButton("🤖 자동 매도만 사용 (스탑로스 + 트레일링스탑)")
        self.auto_sell_only_radio.setChecked(True)  # 기본값
        self.auto_sell_only_radio.setStyleSheet("""
            QRadioButton {
                font-weight: bold; 
                color: #2196F3;
                spacing: 8px;
                padding: 5px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }
            QRadioButton::indicator:checked {
                background-color: #2196F3;
                border: 2px solid #1976D2;
                border-radius: 8px;
            }
        """)

        self.condition_sell_radio = QRadioButton("⚙️ 조건식 매도 + 자동 매도 (최소 1개 선택)")
        self.condition_sell_radio.setStyleSheet("""
            QRadioButton {
                font-weight: bold;
                color: #FF9800;
                spacing: 8px;
                padding: 5px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }
            QRadioButton::indicator:checked {
                background-color: #FF9800;
                border: 2px solid #F57C00;
                border-radius: 8px;
            }
        """)

        self.sell_mode_group.addButton(self.auto_sell_only_radio)
        self.sell_mode_group.addButton(self.condition_sell_radio)

        sell_layout.addWidget(self.auto_sell_only_radio)
        sell_layout.addWidget(self.condition_sell_radio)

        # 조건식 매도 리스트 (개선된 디자인)
        self.sell_condition_list = QListWidget()
        self.sell_condition_list.setSelectionMode(QListWidget.MultiSelection)
        self.sell_condition_list.setMaximumHeight(110)
        self.sell_condition_list.setEnabled(False)  # 초기에는 비활성화
        self.sell_condition_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #ffe8e8;
                border-radius: 6px;
                background-color: white;
                selection-background-color: #FF5722;
                selection-color: white;
                font-size: 11px;
            }
            QListWidget::item {
                padding: 6px;
                border-bottom: 1px solid #f0f0f0;
            }
            QListWidget::item:hover {
                background-color: #ffe8e8;
            }
            QListWidget::item:selected {
                background-color: #FF5722;
                color: white;
                font-weight: bold;
            }
            QListWidget:disabled {
                background-color: #f5f5f5;
                color: #999;
            }
        """)
        sell_layout.addWidget(self.sell_condition_list)

        layout.addWidget(sell_group)

        # 선택된 조건식 표시 (개선된 디자인)
        self.selected_info_label = QLabel("📋 선택된 조건식: 매수 0개, 매도 방식: 자동매도")
        self.selected_info_label.setStyleSheet("""
            QLabel {
                color: #666; 
                font-size: 12px;
                font-weight: bold;
                padding: 8px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #f0f8ff, stop:1 #e3f2fd);
                border: 1px solid #2196F3;
                border-radius: 6px;
                margin: 5px 0px;
            }
        """)
        layout.addWidget(self.selected_info_label)

        # 시그널 연결
        self.buy_condition_list.itemSelectionChanged.connect(self.update_selection_info)
        self.sell_condition_list.itemSelectionChanged.connect(self.update_selection_info)
        self.auto_sell_only_radio.toggled.connect(self.on_sell_mode_changed)
        self.condition_sell_radio.toggled.connect(self.on_sell_mode_changed)

    def on_sell_mode_changed(self):
        """매도 방식 변경 시 호출"""
        if self.auto_sell_only_radio.isChecked():
            self.sell_condition_list.setEnabled(False)
            self.sell_condition_list.clearSelection()
            self.sell_condition_list.setStyleSheet("""
                QListWidget {
                    border: 2px solid #e0e0e0;
                    border-radius: 6px;
                    background-color: #f5f5f5;
                    color: #999;
                    font-size: 11px;
                }
                QListWidget::item {
                    padding: 6px;
                    color: #999;
                }
            """)
        else:
            self.sell_condition_list.setEnabled(True)
            self.sell_condition_list.setStyleSheet("""
                QListWidget {
                    border: 2px solid #ffe8e8;
                    border-radius: 6px;
                    background-color: white;
                    selection-background-color: #FF5722;
                    selection-color: white;
                    font-size: 11px;
                }
                QListWidget::item {
                    padding: 6px;
                    border-bottom: 1px solid #f0f0f0;
                }
                QListWidget::item:hover {
                    background-color: #ffe8e8;
                }
                QListWidget::item:selected {
                    background-color: #FF5722;
                    color: white;
                    font-weight: bold;
                }
            """)

        self.update_selection_info()

    def update_condition_list(self, conditions_df):
        """조건식 리스트 업데이트"""
        self.buy_condition_list.clear()
        self.sell_condition_list.clear()

        if conditions_df is not None and not conditions_df.empty:
            for _, row in conditions_df.iterrows():
                condition_name = row['조건명']

                # 매수 리스트에 추가
                buy_item = QListWidgetItem(f"📈 {condition_name}")
                buy_item.setData(Qt.UserRole, row['조건index'])
                self.buy_condition_list.addItem(buy_item)

                # 매도 리스트에 추가
                sell_item = QListWidgetItem(f"📉 {condition_name}")
                sell_item.setData(Qt.UserRole, row['조건index'])
                self.sell_condition_list.addItem(sell_item)

                # 기본 스케줄 설정
                if condition_name not in self.condition_schedules:
                    self.condition_schedules[condition_name] = {
                        'start_time': '09:00:00',
                        'end_time': '15:30:00',
                        'enabled': True
                    }

        self.update_time_status_display()

    def get_selected_buy_conditions(self):
        """선택된 매수 조건식 반환"""
        selected = []
        for item in self.buy_condition_list.selectedItems():
            # 이모지 제거
            name = item.text().replace("📈 ", "")
            selected.append({
                'name': name,
                'index': item.data(Qt.UserRole)
            })
        return selected

    def get_selected_sell_conditions(self):
        """선택된 매도 조건식 반환"""
        if self.auto_sell_only_radio.isChecked():
            return []  # 자동매도만 사용

        selected = []
        for item in self.sell_condition_list.selectedItems():
            # 이모지 제거
            name = item.text().replace("📉 ", "")
            selected.append({
                'name': name,
                'index': item.data(Qt.UserRole)
            })
        return selected

    def is_auto_sell_only_mode(self):
        """자동매도 전용 모드인지 확인"""
        return self.auto_sell_only_radio.isChecked()

    def update_selection_info(self):
        """선택 정보 업데이트 (개선된 메시지)"""
        buy_count = len(self.buy_condition_list.selectedItems())

        if self.auto_sell_only_radio.isChecked():
            sell_info = "🤖 자동매도 (스탑로스 + 트레일링스탑)"
            self.selected_info_label.setText(f"📋 선택: 매수 {buy_count}개, 매도: {sell_info}")
        else:
            sell_count = len(self.sell_condition_list.selectedItems())
            sell_info = f"⚙️ 조건식 {sell_count}개 + 자동매도"
            self.selected_info_label.setText(f"📋 선택: 매수 {buy_count}개, 매도: {sell_info}")

        # 색상 및 스타일 설정
        if buy_count < 3:
            self.selected_info_label.setStyleSheet("""
                QLabel {
                    color: #d32f2f; 
                    font-size: 12px;
                    font-weight: bold;
                    padding: 8px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 #ffebee, stop:1 #ffcdd2);
                    border: 2px solid #f44336;
                    border-radius: 6px;
                    margin: 5px 0px;
                }
            """)
        elif not self.auto_sell_only_radio.isChecked() and len(self.sell_condition_list.selectedItems()) < 1:
            self.selected_info_label.setStyleSheet("""
                QLabel {
                    color: #f57c00; 
                    font-size: 12px;
                    font-weight: bold;
                    padding: 8px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 #fff8e1, stop:1 #ffecb3);
                    border: 2px solid #ff9800;
                    border-radius: 6px;
                    margin: 5px 0px;
                }
            """)
        else:
            self.selected_info_label.setStyleSheet("""
                QLabel {
                    color: #2e7d32; 
                    font-size: 12px;
                    font-weight: bold;
                    padding: 8px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 #e8f5e8, stop:1 #c8e6c9);
                    border: 2px solid #4caf50;
                    border-radius: 6px;
                    margin: 5px 0px;
                }
            """)

    def validate_selection(self):
        """선택 검증 (개선된 메시지)"""
        buy_count = len(self.buy_condition_list.selectedItems())

        if buy_count < 3:
            QMessageBox.warning(
                self, "⚠️ 선택 오류",
                f"매수 조건식을 최소 3개 이상 선택해주세요.\n\n"
                f"현재 선택: {buy_count}개\n"
                f"필요: 3개 이상\n\n"
                f"💡 팁: 다양한 조건식을 선택하면 더 안정적인 매매가 가능합니다."
            )
            return False

        # 조건식 매도 모드인 경우 최소 1개 선택 확인
        if self.condition_sell_radio.isChecked():
            sell_count = len(self.sell_condition_list.selectedItems())
            if sell_count < 1:
                QMessageBox.warning(
                    self, "⚠️ 선택 오류",
                    f"조건식 매도 모드에서는 매도 조건식을 최소 1개 이상 선택해주세요.\n\n"
                    f"현재 선택: {sell_count}개\n"
                    f"필요: 1개 이상\n\n"
                    f"💡 또는 '자동 매도만 사용' 모드를 선택하세요."
                )
                return False

        return True

    def open_time_setting_dialog(self):
        """쉬운 시간 설정 다이얼로그 열기"""
        try:
            # 이 부분을 actual 파일 이름에 맞게 수정하세요
            from easy_time_setting import EasyTimeSettingDialog

            dialog = EasyTimeSettingDialog(self.condition_schedules, self)
            if dialog.exec_() == QDialog.Accepted:
                result = dialog.get_schedules()
                if result:
                    self.condition_schedules = result
                    self.update_time_status_display()

                    # 설정 완료 알림
                    active_count = sum(1 for schedule in result.values() if schedule['enabled'])
                    total_count = len(result)
                    QMessageBox.information(
                        self, "✅ 설정 완료",
                        f"시간 설정이 완료되었습니다!\n\n"
                        f"📊 활성화된 조건식: {active_count}/{total_count}개\n"
                        f"💾 설정은 자동으로 저장됩니다.\n\n"
                        f"💡 이제 자동매매를 시작할 수 있습니다!"
                    )
        except ImportError as e:
            QMessageBox.warning(
                self, "⚠️ 모듈 오류",
                f"시간 설정 위젯을 불러올 수 없습니다.\n"
                f"오류: {str(e)}\n\n"
                f"📁 easy_time_setting.py 파일을 같은 폴더에 저장했는지 확인해주세요."
            )
        except Exception as e:
            QMessageBox.critical(
                self, "❌ 오류 발생",
                f"시간 설정 중 오류가 발생했습니다:\n{str(e)}"
            )

    def update_time_status_display(self):
        """⭐ 누락된 메서드 - 시간 설정 상태 표시 업데이트"""
        if not self.condition_schedules:
            self.status_label.setText("⏰ 시간 설정: 기본값 (09:00~15:30)")
            self.status_label.setStyleSheet("""
                QLabel {
                    color: #666;
                    font-size: 11px;
                    padding: 3px 8px;
                    background-color: #f0f0f0;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                }
            """)
            return

        active_count = sum(1 for schedule in self.condition_schedules.values() if schedule['enabled'])
        total_count = len(self.condition_schedules)

        if active_count == 0:
            self.status_label.setText("⏰ 시간 설정: 모든 조건식 비활성화 (24시간)")
            self.status_label.setStyleSheet("""
                QLabel {
                    color: #f44336;
                    font-size: 11px;
                    font-weight: bold;
                    padding: 4px 8px;
                    background-color: #ffebee;
                    border: 1px solid #f44336;
                    border-radius: 4px;
                }
            """)
        elif active_count == total_count:
            # 모든 조건식이 같은 시간인지 확인
            times = set()
            for schedule in self.condition_schedules.values():
                if schedule['enabled']:
                    times.add((schedule['start_time'], schedule['end_time']))

            if len(times) == 1:
                start, end = list(times)[0]
                start_display = start[:5]  # HH:MM 형식으로
                end_display = end[:5]
                self.status_label.setText(f"⏰ 시간 설정: 전체 통일 ({start_display}~{end_display})")
            else:
                self.status_label.setText(f"⏰ 시간 설정: 개별 설정 (활성화 {active_count}/{total_count}개)")

            self.status_label.setStyleSheet("""
                QLabel {
                    color: #4caf50;
                    font-size: 11px;
                    font-weight: bold;
                    padding: 4px 8px;
                    background-color: #e8f5e8;
                    border: 1px solid #4caf50;
                    border-radius: 4px;
                }
            """)
        else:
            self.status_label.setText(f"⏰ 시간 설정: 부분 활성화 ({active_count}/{total_count}개)")
            self.status_label.setStyleSheet("""
                QLabel {
                    color: #ff9800;
                    font-size: 11px;
                    font-weight: bold;
                    padding: 4px 8px;
                    background-color: #fff8e1;
                    border: 1px solid #ff9800;
                    border-radius: 4px;
                }
            """)

    def get_condition_schedules(self):
        """조건식별 스케줄 반환"""
        return self.condition_schedules

    def is_condition_active_now(self, condition_name):
        """현재 시간에 해당 조건식이 활성화되어 있는지 확인"""
        if condition_name not in self.condition_schedules:
            return True

        schedule = self.condition_schedules[condition_name]
        if not schedule.get('enabled', True):
            return False

        now = datetime.datetime.now().time()
        start_time = datetime.datetime.strptime(schedule['start_time'], '%H:%M:%S').time()
        end_time = datetime.datetime.strptime(schedule['end_time'], '%H:%M:%S').time()

        return start_time <= now <= end_time


class PandasModel(QAbstractTableModel):
    """Pandas DataFrame을 위한 테이블 모델"""

    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0] if not self._data.empty else 0

    def columnCount(self, parent=None):
        return self._data.shape[1] if not self._data.empty else 0

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or self._data.empty:
            return None

        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            if isinstance(value, float):
                return f"{value:.2f}"
            return str(value)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        elif role == Qt.ForegroundRole:
            if self._data.columns[index.column()] in ("수익률(%)", "전일대비(%)"):
                try:
                    value = self._data.iloc[index.row(), index.column()]
                    if isinstance(value, str) and "," in value:
                        value = float(value.replace(",", ""))
                    if float(value) < 0:
                        return QColor(Qt.blue)
                    elif float(value) > 0:
                        return QColor(Qt.red)
                except (ValueError, TypeError):
                    pass
        return None

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if not self._data.empty and section < len(self._data.columns):
                return self._data.columns[section]
        elif orientation == Qt.Vertical and role == Qt.DisplayRole:
            if not self._data.empty and section < len(self._data.index):
                return str(self._data.index[section])
        return None

    def update_data(self, data):
        self.beginResetModel()
        self._data = data
        self.endResetModel()


class ModernGroupBox(QGroupBox):
    """모던한 스타일의 GroupBox"""

    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                background-color: white;
                border-radius: 4px;
            }
        """)


class StatusWidget(QWidget):
    """상태 표시 위젯"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # 연결 상태
        self.connection_label = QLabel("연결: 대기중")
        self.connection_label.setStyleSheet("color: orange; font-weight: bold;")

        # 자동매매 상태
        self.auto_trade_label = QLabel("자동매매: 중지")
        self.auto_trade_label.setStyleSheet("color: red; font-weight: bold;")

        # 매도 방식 표시
        self.sell_mode_label = QLabel("매도: 자동매도")
        self.sell_mode_label.setStyleSheet("color: #2196F3; font-weight: bold;")

        # 활성 조건식 수
        self.active_conditions_label = QLabel("활성 조건식: 0/0")

        # 실시간 등록 종목 수
        self.realtime_count_label = QLabel("실시간: 0/95")

        # 현재 시간
        self.time_label = QLabel(datetime.datetime.now().strftime("%H:%M:%S"))

        layout.addWidget(QLabel("상태:"))
        layout.addWidget(self.connection_label)
        layout.addWidget(QLabel("|"))
        layout.addWidget(self.auto_trade_label)
        layout.addWidget(QLabel("|"))
        layout.addWidget(self.sell_mode_label)
        layout.addWidget(QLabel("|"))
        layout.addWidget(self.active_conditions_label)
        layout.addWidget(QLabel("|"))
        layout.addWidget(self.realtime_count_label)
        layout.addStretch()
        layout.addWidget(self.time_label)

        # 시간 업데이트 타이머
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        self.time_label.setText(datetime.datetime.now().strftime("%H:%M:%S"))

    def set_connection_status(self, connected):
        if connected:
            self.connection_label.setText("연결: 완료")
            self.connection_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.connection_label.setText("연결: 실패")
            self.connection_label.setStyleSheet("color: red; font-weight: bold;")

    def set_auto_trade_status(self, active):
        if active:
            self.auto_trade_label.setText("자동매매: 실행중")
            self.auto_trade_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.auto_trade_label.setText("자동매매: 중지")
            self.auto_trade_label.setStyleSheet("color: red; font-weight: bold;")

    def set_sell_mode(self, is_auto_only, sell_condition_count=0):
        if is_auto_only:
            self.sell_mode_label.setText("매도: 자동매도")
            self.sell_mode_label.setStyleSheet("color: #2196F3; font-weight: bold;")
        else:
            self.sell_mode_label.setText(f"매도: 조건식{sell_condition_count}개+자동")
            self.sell_mode_label.setStyleSheet("color: #FF9800; font-weight: bold;")

    def set_active_conditions(self, active_count, total_count):
        self.active_conditions_label.setText(f"활성 조건식: {active_count}/{total_count}")
        if active_count == 0:
            self.active_conditions_label.setStyleSheet("color: red; font-weight: bold;")
        else:
            self.active_conditions_label.setStyleSheet("color: green; font-weight: bold;")

    def set_realtime_count(self, current, maximum):
        self.realtime_count_label.setText(f"실시간: {current}/{maximum}")
        if current >= maximum * 0.9:
            self.realtime_count_label.setStyleSheet("color: red; font-weight: bold;")
        elif current >= maximum * 0.7:
            self.realtime_count_label.setStyleSheet("color: orange; font-weight: bold;")
        else:
            self.realtime_count_label.setStyleSheet("color: black;")


def format_number(text_edit):
    """숫자 포맷팅 (천 단위 콤마 추가)"""
    plain_number = text_edit.text().replace(",", "")

    try:
        formatted_number = f"{int(plain_number):,}"
    except ValueError:
        formatted_number = ""

    cursor_pos = text_edit.cursorPosition()
    text_edit.setText(formatted_number)
    text_edit.setCursorPosition(cursor_pos)


class KiwoomAPI(QMainWindow):
    """키움증권 자동매매 시스템 메인 클래스"""

    # 시그널 정의
    status_updated = pyqtSignal(str)
    data_updated = pyqtSignal()

    def __init__(
            self,
            tr_req_queue=None,
            tr_result_queue=None,
            order_tr_req_queue=None,
            websocket_req_queue=None,
            websocket_result_queue=None,
    ):
        super().__init__()

        # Queue 설정
        self.tr_req_queue = tr_req_queue
        self.tr_result_queue = tr_result_queue
        self.order_tr_req_queue = order_tr_req_queue
        self.websocket_req_queue = websocket_req_queue
        self.websocket_result_queue = websocket_result_queue

        # 데이터 초기화
        self.init_data()

        # UI 설정
        self.setup_ui()
        self.setup_connections()
        self.setup_timers()

        # 설정 로드
        self.settings = QSettings('KiwoomAutoTrade', 'MainApp')
        self.load_settings()

        # 초기 요청
        self.init_requests()

        self.show()

    def init_data(self):
        """데이터 초기화"""
        self.condition_df = pd.DataFrame(columns=["조건index", "조건명"])
        self.condition_name_to_index_dict = dict()
        self.condition_index_to_name_dict = dict()
        self.account_info_df = pd.DataFrame(columns=["종목명", "현재가", "매입가", "보유수량", "매매가능수량", "수익률(%)"])

        # 실시간 트래킹 데이터 로드
        try:
            self.realtime_tracking_df = pd.read_pickle("realtime_tracking_df.pkl")
        except FileNotFoundError:
            self.realtime_tracking_df = pd.DataFrame(
                columns=["종목명", "현재가", "매입가", "수익률(%)", "트레일링 발동 여부", "트레일링 발동 후 고가", "매수주문여부", "매도주문여부", "진입조건식"]
            )

        self.last_saved_realtime_tracking_df = self.realtime_tracking_df.copy(deep=True)
        self.stock_code_to_basic_info_dict = dict()
        self.order_info_df = pd.DataFrame(columns=["주문접수시간", "종목코드", "주문수량", "매수매도구분", "발생조건식"])
        self.realtime_registered_codes_set = set()
        self.amend_ordered_num_set = set()

        # 상수 설정
        self.transaction_cost = TRANSACTION_COST
        self.current_realtime_count = 0
        self.max_realtime_count = MAX_REALTIME_COUNT
        self.is_no_transaction = True
        self.has_init = False

        # 다중 조건식 관련
        self.active_buy_conditions = []
        self.active_sell_conditions = []
        self.is_auto_sell_only = True  # 기본값: 자동매도만 사용

    def setup_ui(self):
        """UI 설정"""
        self.setWindowTitle("키움증권 자동매매 시스템 v2.2 (유연한 매도조건)")
        self.setGeometry(100, 100, 1500, 1000)

        # 메뉴바 설정
        self.setup_menubar()

        # 상태바 설정
        self.status_widget = StatusWidget()
        self.statusBar().addPermanentWidget(self.status_widget)

        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 메인 레이아웃
        main_layout = QVBoxLayout(central_widget)

        # 탭 위젯 생성
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # 각 탭 생성
        self.create_trading_tab()
        self.create_account_tab()
        self.create_settings_tab()
        self.create_log_tab()

        # 스타일 적용
        self.apply_modern_style()

    def setup_menubar(self):
        """메뉴바 설정"""
        menubar = self.menuBar()

        # 파일 메뉴
        file_menu = menubar.addMenu('파일(&F)')

        # 설정 저장
        save_action = QAction('설정 저장(&S)', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_settings)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        # 종료
        exit_action = QAction('종료(&X)', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 도구 메뉴
        tools_menu = menubar.addMenu('도구(&T)')

        # 데이터 초기화
        reset_action = QAction('데이터 초기화(&R)', self)
        reset_action.triggered.connect(self.reset_data)
        tools_menu.addAction(reset_action)

    def create_trading_tab(self):
        """자동매매 탭 생성"""
        trading_widget = QWidget()
        layout = QVBoxLayout(trading_widget)

        # 상단: 컨트롤 패널
        control_panel = self.create_control_panel()
        layout.addWidget(control_panel)

        # 하단: 스플리터로 나누어진 테이블들
        splitter = QSplitter(Qt.Vertical)

        # 실시간 트래킹 테이블
        tracking_group = ModernGroupBox("실시간 트래킹")
        tracking_layout = QVBoxLayout(tracking_group)

        self.autoTradeInfoTableView = QTableView()
        self.autoTradeInfoTableView.setAlternatingRowColors(True)
        tracking_layout.addWidget(self.autoTradeInfoTableView)

        splitter.addWidget(tracking_group)

        # 주문 정보 테이블
        order_group = ModernGroupBox("주문 정보")
        order_layout = QVBoxLayout(order_group)

        self.orderInfoTableView = QTableView()
        self.orderInfoTableView.setAlternatingRowColors(True)
        order_layout.addWidget(self.orderInfoTableView)

        splitter.addWidget(order_group)

        # 비율 설정
        splitter.setSizes([600, 200])
        layout.addWidget(splitter)

        self.tab_widget.addTab(trading_widget, "자동매매")

    def create_control_panel(self):
        """컨트롤 패널 생성"""
        control_widget = QWidget()
        main_layout = QHBoxLayout(control_widget)

        # 좌측: 자동매매 컨트롤
        auto_trade_group = ModernGroupBox("자동매매 제어")
        auto_trade_layout = QVBoxLayout(auto_trade_group)

        # 자동매매 버튼
        button_layout = QHBoxLayout()
        self.autoOnPushButton = QPushButton("자동매매 시작")
        self.autoOnPushButton.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)

        self.autoOffPushButton = QPushButton("자동매매 중지")
        self.autoOffPushButton.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.autoOffPushButton.setEnabled(False)

        button_layout.addWidget(self.autoOnPushButton)
        button_layout.addWidget(self.autoOffPushButton)
        auto_trade_layout.addLayout(button_layout)

        # 유연한 매도 조건 위젯
        self.flexible_sell_widget = FlexibleSellConditionWidget()
        auto_trade_layout.addWidget(self.flexible_sell_widget)

        main_layout.addWidget(auto_trade_group)

        # 중앙: 매수/매도 설정
        trade_settings_group = ModernGroupBox("매수/매도 설정")
        trade_settings_layout = QVBoxLayout(trade_settings_group)

        # 매수 설정
        buy_group = QGroupBox("매수 설정")
        buy_layout = QFormLayout(buy_group)

        self.buyAmountLineEdit = QLineEdit("200,000")
        self.buyAmountLineEdit.setPlaceholderText("매수 금액 입력")

        # 매수 방식 선택
        buy_type_widget = QWidget()
        buy_type_layout = QHBoxLayout(buy_type_widget)
        buy_type_layout.setContentsMargins(0, 0, 0, 0)

        self.buy_button_group = QButtonGroup()
        self.marketBuyRadioButton = QRadioButton("시장가")
        self.limitBuyRadioButton = QRadioButton("지정가")
        self.marketBuyRadioButton.setChecked(True)

        self.buy_button_group.addButton(self.marketBuyRadioButton)
        self.buy_button_group.addButton(self.limitBuyRadioButton)

        buy_type_layout.addWidget(self.marketBuyRadioButton)
        buy_type_layout.addWidget(self.limitBuyRadioButton)

        self.limitBuySpinBox = QSpinBox()
        self.limitBuySpinBox.setRange(-10, 10)
        self.limitBuySpinBox.setSuffix(" 틱")

        buy_layout.addRow("매수 금액:", self.buyAmountLineEdit)
        buy_layout.addRow("매수 방식:", buy_type_widget)
        buy_layout.addRow("지정가 틱:", self.limitBuySpinBox)

        trade_settings_layout.addWidget(buy_group)

        # 매도 설정
        sell_group = QGroupBox("매도 설정")
        sell_layout = QFormLayout(sell_group)

        # 매도 방식 선택
        sell_type_widget = QWidget()
        sell_type_layout = QHBoxLayout(sell_type_widget)
        sell_type_layout.setContentsMargins(0, 0, 0, 0)

        self.sell_button_group = QButtonGroup()
        self.marketSellRadioButton = QRadioButton("시장가")
        self.limitSellRadioButton = QRadioButton("지정가")
        self.marketSellRadioButton.setChecked(True)

        self.sell_button_group.addButton(self.marketSellRadioButton)
        self.sell_button_group.addButton(self.limitSellRadioButton)

        sell_type_layout.addWidget(self.marketSellRadioButton)
        sell_type_layout.addWidget(self.limitSellRadioButton)

        self.limitSellSpinBox = QSpinBox()
        self.limitSellSpinBox.setRange(-10, 10)
        self.limitSellSpinBox.setSuffix(" 틱")

        sell_layout.addRow("매도 방식:", sell_type_widget)
        sell_layout.addRow("지정가 틱:", self.limitSellSpinBox)

        trade_settings_layout.addWidget(sell_group)

        main_layout.addWidget(trade_settings_group)

        # 우측: 리스크 관리
        risk_group = ModernGroupBox("리스크 관리 (자동매도)")
        risk_layout = QVBoxLayout(risk_group)

        # 자동매도 안내
        info_label = QLabel("💡 자동매도는 항상 활성화됩니다")
        info_label.setStyleSheet(
            "color: #2196F3; font-weight: bold; background-color: #e3f2fd; padding: 8px; border-radius: 4px;")
        risk_layout.addWidget(info_label)

        # 스탑로스
        self.stopLossCheckBox = QCheckBox("스탑로스 사용")
        self.stopLossCheckBox.setChecked(True)
        self.stopLossDoubleSpinBox = QDoubleSpinBox()
        self.stopLossDoubleSpinBox.setRange(-10.0, 0.0)
        self.stopLossDoubleSpinBox.setValue(-2.0)
        self.stopLossDoubleSpinBox.setSuffix(" %")

        stoploss_layout = QHBoxLayout()
        stoploss_layout.addWidget(self.stopLossCheckBox)
        stoploss_layout.addWidget(self.stopLossDoubleSpinBox)

        # 트레일링 스탑
        self.trailingStopCheckBox = QCheckBox("트레일링 스탑 사용")
        self.trailingStopCheckBox.setChecked(True)

        trailing_widget = QWidget()
        trailing_layout = QFormLayout(trailing_widget)

        self.trailingStopDoubleSpinBox1 = QDoubleSpinBox()
        self.trailingStopDoubleSpinBox1.setRange(0.0, 10.0)
        self.trailingStopDoubleSpinBox1.setValue(2.0)
        self.trailingStopDoubleSpinBox1.setSuffix(" %")

        self.trailingStopDoubleSpinBox2 = QDoubleSpinBox()
        self.trailingStopDoubleSpinBox2.setRange(-5.0, 0.0)
        self.trailingStopDoubleSpinBox2.setValue(-1.0)
        self.trailingStopDoubleSpinBox2.setSuffix(" %")

        trailing_layout.addRow("발동 수익률:", self.trailingStopDoubleSpinBox1)
        trailing_layout.addRow("청산 하락률:", self.trailingStopDoubleSpinBox2)

        # 기타 설정
        other_layout = QFormLayout()

        self.maxAutoTradeCountSpinBox = QSpinBox()
        self.maxAutoTradeCountSpinBox.setRange(1, 50)
        self.maxAutoTradeCountSpinBox.setValue(10)

        self.amendOrderSpinBox = QSpinBox()
        self.amendOrderSpinBox.setRange(10, 300)
        self.amendOrderSpinBox.setValue(60)
        self.amendOrderSpinBox.setSuffix(" 초")

        other_layout.addRow("최대 보유종목:", self.maxAutoTradeCountSpinBox)
        other_layout.addRow("정정주문 시간:", self.amendOrderSpinBox)

        risk_layout.addLayout(stoploss_layout)
        risk_layout.addWidget(self.trailingStopCheckBox)
        risk_layout.addWidget(trailing_widget)
        risk_layout.addLayout(other_layout)

        # 저장 버튼
        self.savePushButton = QPushButton("설정 저장")
        self.savePushButton.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        risk_layout.addWidget(self.savePushButton)

        main_layout.addWidget(risk_group)

        return control_widget

    def create_account_tab(self):
        """계좌 정보 탭 생성"""
        account_widget = QWidget()
        layout = QVBoxLayout(account_widget)

        # 계좌 정보 그룹
        account_group = ModernGroupBox("계좌 보유 현황")
        account_layout = QVBoxLayout(account_group)

        self.accountInfoTableView = QTableView()
        self.accountInfoTableView.setAlternatingRowColors(True)
        account_layout.addWidget(self.accountInfoTableView)

        layout.addWidget(account_group)

        self.tab_widget.addTab(account_widget, "계좌 정보")

    def create_settings_tab(self):
        """설정 탭 생성"""
        settings_widget = QWidget()
        layout = QVBoxLayout(settings_widget)

        scroll_area = QScrollArea()
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # API 설정 그룹
        api_group = ModernGroupBox("API 설정")
        api_layout = QFormLayout(api_group)

        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.Password)
        self.api_secret_edit = QLineEdit()
        self.api_secret_edit.setEchoMode(QLineEdit.Password)
        self.api_url_edit = QLineEdit()

        api_layout.addRow("API Key:", self.api_key_edit)
        api_layout.addRow("API Secret:", self.api_secret_edit)
        api_layout.addRow("API URL:", self.api_url_edit)

        scroll_layout.addWidget(api_group)

        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        self.tab_widget.addTab(settings_widget, "설정")

    def create_log_tab(self):
        """로그 탭 생성"""
        log_widget = QWidget()
        layout = QVBoxLayout(log_widget)

        # 로그 텍스트 에디터
        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)
        self.log_text_edit.setFont(QFont("Consolas", 9))

        # 로그 제어 버튼
        log_control_layout = QHBoxLayout()

        self.clear_log_button = QPushButton("로그 지우기")
        self.save_log_button = QPushButton("로그 저장")

        log_control_layout.addWidget(self.clear_log_button)
        log_control_layout.addWidget(self.save_log_button)
        log_control_layout.addStretch()

        layout.addWidget(self.log_text_edit)
        layout.addLayout(log_control_layout)

        self.tab_widget.addTab(log_widget, "로그")

    def apply_modern_style(self):
        """모던한 스타일 적용"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background-color: white;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #e9e9e9;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #2196F3;
            }
            QTableView {
                gridline-color: #e0e0e0;
                selection-background-color: #e3f2fd;
                border: 1px solid #cccccc;
                border-radius: 4px;
            }
            QTableView::item {
                padding: 8px;
            }
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QTimeEdit {
                padding: 6px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                background-color: white;
            }
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus, QTimeEdit:focus {
                border: 2px solid #2196F3;
            }
            QListWidget {
                border: 1px solid #cccccc;
                border-radius: 4px;
                background-color: white;
                selection-background-color: #e3f2fd;
            }
            QListWidget::item {
                padding: 4px;
                border-bottom: 1px solid #f0f0f0;
            }
            QListWidget::item:selected {
                background-color: #2196F3;
                color: white;
            }
            QCheckBox {
                spacing: 8px;
            }
            QRadioButton {
                spacing: 8px;
            }
        """)

    def setup_connections(self):
        """시그널/슬롯 연결"""
        # 버튼 연결
        self.autoOnPushButton.clicked.connect(self.auto_trade_on)
        self.autoOffPushButton.clicked.connect(self.auto_trade_off)
        self.savePushButton.clicked.connect(self.save_settings)

        # 텍스트 편집 연결
        self.buyAmountLineEdit.textChanged.connect(lambda: format_number(self.buyAmountLineEdit))

        # 로그 버튼 연결
        self.clear_log_button.clicked.connect(self.clear_log)
        self.save_log_button.clicked.connect(self.save_log)

        # 체크박스 연결
        self.stopLossCheckBox.toggled.connect(self.stopLossDoubleSpinBox.setEnabled)
        self.trailingStopCheckBox.toggled.connect(self.update_trailing_stop_enabled)

        # 라디오버튼 연결
        self.limitBuyRadioButton.toggled.connect(self.limitBuySpinBox.setEnabled)
        self.limitSellRadioButton.toggled.connect(self.limitSellSpinBox.setEnabled)

        # 매도 모드 변경 연결
        self.flexible_sell_widget.auto_sell_only_radio.toggled.connect(self.on_sell_mode_changed)

    def setup_timers(self):
        """타이머 설정"""
        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.receive_websocket_result)
        self.timer1.start(10)  # 0.01초

        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.receive_tr_result)
        self.timer2.start(100)  # 0.1초

        self.timer3 = QTimer()
        self.timer3.timeout.connect(self.update_pandas_models)
        self.timer3.start(1000)  # 1초

        self.timer4 = QTimer()
        self.timer4.timeout.connect(self.save_pickle)
        self.timer4.start(5000)  # 5초

        self.timer5 = QTimer()
        self.timer5.timeout.connect(self.check_amend_orders)
        self.timer5.start(1000)  # 1초

        self.timer6 = QTimer()
        self.timer6.timeout.connect(self.check_valid_time)
        self.timer6.start(1000)  # 1초

        # 조건식 활성 상태 체크 타이머
        self.timer7 = QTimer()
        self.timer7.timeout.connect(self.update_active_conditions)
        self.timer7.start(60000)  # 1분마다

    def init_requests(self):
        """초기 요청"""
        if self.websocket_req_queue:
            self.websocket_req_queue.put(dict(action_id="조건검색식리스트"))
        if self.tr_req_queue:
            self.tr_req_queue.put(dict(action_id="계좌조회"))

    def on_sell_mode_changed(self):
        """매도 모드 변경 시 상태바 업데이트"""
        self.is_auto_sell_only = self.flexible_sell_widget.is_auto_sell_only_mode()
        sell_condition_count = len(self.flexible_sell_widget.get_selected_sell_conditions())

        self.status_widget.set_sell_mode(self.is_auto_sell_only, sell_condition_count)

    @log_exceptions
    def auto_trade_on(self):
        """자동매매 시작"""
        try:
            # 조건식 선택 검증
            if not self.flexible_sell_widget.validate_selection():
                return

            self.autoOnPushButton.setEnabled(False)
            self.autoOffPushButton.setEnabled(True)

            # 상태 업데이트
            self.status_widget.set_auto_trade_status(True)

            # 선택된 조건식들 가져오기
            self.active_buy_conditions = self.flexible_sell_widget.get_selected_buy_conditions()
            self.active_sell_conditions = self.flexible_sell_widget.get_selected_sell_conditions()
            self.is_auto_sell_only = self.flexible_sell_widget.is_auto_sell_only_mode()

            # 매수 조건식 실시간 등록
            for condition in self.active_buy_conditions:
                if self.flexible_sell_widget.is_condition_active_now(condition['name']):
                    if self.websocket_req_queue:
                        self.websocket_req_queue.put(
                            dict(
                                action_id="조건검색실시간등록",
                                조건index=condition['index'],
                            )
                        )
                    self.add_log(f"매수 조건식 '{condition['name']}' 실시간 등록")

            # 매도 조건식 실시간 등록 (조건식 모드인 경우만)
            if not self.is_auto_sell_only:
                for condition in self.active_sell_conditions:
                    if self.flexible_sell_widget.is_condition_active_now(condition['name']):
                        if self.websocket_req_queue:
                            self.websocket_req_queue.put(
                                dict(
                                    action_id="조건검색실시간등록",
                                    조건index=condition['index'],
                                )
                            )
                        self.add_log(f"매도 조건식 '{condition['name']}' 실시간 등록")

            self.is_no_transaction = False

            # 상태바 업데이트
            self.update_active_conditions()
            self.status_widget.set_sell_mode(self.is_auto_sell_only, len(self.active_sell_conditions))

            if self.is_auto_sell_only:
                self.add_log(f"자동매매 시작 - 매수조건 {len(self.active_buy_conditions)}개, 매도: 자동매도만")
            else:
                self.add_log(
                    f"자동매매 시작 - 매수조건 {len(self.active_buy_conditions)}개, 매도조건 {len(self.active_sell_conditions)}개 + 자동매도")

        except Exception as e:
            logger.exception(f"자동매매 시작 중 오류: {e}")
            self.add_log(f"자동매매 시작 실패: {str(e)}")

    @log_exceptions
    def auto_trade_off(self):
        """자동매매 중지"""
        try:
            self.autoOnPushButton.setEnabled(True)
            self.autoOffPushButton.setEnabled(False)

            # 상태 업데이트
            self.status_widget.set_auto_trade_status(False)

            # 매수 조건식 실시간 해제
            for condition in self.active_buy_conditions:
                if self.websocket_req_queue:
                    self.websocket_req_queue.put(
                        dict(
                            action_id="조건검색실시간해제",
                            조건index=condition['index'],
                        )
                    )
                self.add_log(f"매수 조건식 '{condition['name']}' 실시간 해제")

            # 매도 조건식 실시간 해제 (조건식 모드였던 경우만)
            if not self.is_auto_sell_only:
                for condition in self.active_sell_conditions:
                    if self.websocket_req_queue:
                        self.websocket_req_queue.put(
                            dict(
                                action_id="조건검색실시간해제",
                                조건index=condition['index'],
                            )
                        )
                    self.add_log(f"매도 조건식 '{condition['name']}' 실시간 해제")

            self.is_no_transaction = True

            # 활성 조건식 초기화
            self.active_buy_conditions = []
            self.active_sell_conditions = []

            # 상태 업데이트
            self.status_widget.set_active_conditions(0, 0)
            self.status_widget.set_sell_mode(True, 0)  # 기본값으로 리셋

            self.add_log("자동매매가 중지되었습니다.")

        except Exception as e:
            logger.exception(f"자동매매 중지 중 오류: {e}")
            self.add_log(f"자동매매 중지 실패: {str(e)}")

    @log_exceptions
    def on_receive_realtime_condition_event(self, data):
        """실시간 조건검색 이벤트 처리"""
        try:
            조건식idx = data['조건식idx']
            종목코드 = data['종목코드']
            편입편출 = data['편입편출']

            # 해당 조건식이 현재 활성화된 조건식인지 확인
            is_buy_condition = any(condition['index'] == 조건식idx for condition in self.active_buy_conditions)
            is_sell_condition = any(condition['index'] == 조건식idx for condition in self.active_sell_conditions)

            # 조건식명 찾기
            condition_name = self.condition_index_to_name_dict.get(조건식idx, f"조건식_{조건식idx}")

            # 매수 조건 체크
            if is_buy_condition and all([
                self.current_realtime_count < self.max_realtime_count,
                편입편출 == "I",
                not self.is_no_transaction,
                len(self.realtime_tracking_df) < self.maxAutoTradeCountSpinBox.value(),
                종목코드 not in self.account_info_df.index,
                종목코드 not in self.realtime_tracking_df.index,
                self.flexible_sell_widget.is_condition_active_now(condition_name),
            ]):
                self.register_realtime_info(종목코드)
                if self.tr_req_queue:
                    self.tr_req_queue.put(
                        dict(
                            action_id="주식기본정보",
                            종목코드=종목코드,
                        )
                    )

                # 진입 조건식 정보 추가
                if 종목코드 not in self.realtime_tracking_df.index:
                    self.realtime_tracking_df.loc[종목코드] = {
                        "종목명": "",
                        "현재가": None,
                        "매입가": None,
                        "수익률(%)": None,
                        "트레일링 발동 여부": False,
                        "트레일링 발동 후 고가": None,
                        "매수주문여부": False,
                        "매도주문여부": False,
                        "진입조건식": condition_name,
                    }

                self.add_log(f"매수 신호: {종목코드} (조건식: {condition_name})")

            # 매도 조건 체크 (조건식 매도 모드인 경우만)
            elif not self.is_auto_sell_only and is_sell_condition and all([
                종목코드 in self.realtime_tracking_df.index,
                self.realtime_tracking_df.at[종목코드, "매수주문여부"] == True,
                self.realtime_tracking_df.at[종목코드, "매도주문여부"] == False,
                편입편출 == "I",
                not self.is_no_transaction,
                self.flexible_sell_widget.is_condition_active_now(condition_name),
            ]):
                self.sell_order(종목코드, sell_reason=f"조건식: {condition_name}")
                self.add_log(f"매도 신호: {종목코드} (조건식: {condition_name})")

        except Exception as e:
            logger.exception(f"실시간 조건검색 이벤트 처리 중 오류: {e}")

    def sell_order(self, 종목코드, sell_reason="일반매도"):
        """매도 주문"""
        try:
            if 종목코드 not in self.account_info_df.index:
                self.add_log(f"매도 실패: {종목코드} - 보유종목이 아님")
                return

            self.realtime_tracking_df.at[종목코드, "매도주문여부"] = True

            시장가여부 = self.marketSellRadioButton.isChecked()
            주문가격 = ''
            주문수량 = self.account_info_df.at[종목코드, "매매가능수량"]
            현재가 = self.account_info_df.at[종목코드, "현재가"]

            if not 시장가여부:
                틱단위 = self.get_tick_size(현재가)
                주문가격 = self.get_order_price(현재가 + self.limitSellSpinBox.value() * 틱단위)

            if self.order_tr_req_queue:
                self.order_tr_req_queue.put(
                    dict(
                        action_id="매도주문",
                        종목코드=종목코드,
                        주문수량=주문수량,
                        주문가격=주문가격,
                        시장가여부=시장가여부,
                    )
                )

            order_type = "시장가" if 시장가여부 else f"지정가({주문가격})"
            self.add_log(f"매도 주문: {종목코드} {주문수량}주 {order_type} - {sell_reason}")

        except Exception as e:
            logger.exception(f"매도 주문 중 오류: {e}")
            self.add_log(f"매도 주문 실패: {종목코드} - {str(e)}")

    def on_realtime_tracking_df_update(self, 종목코드, 현재가, 수익률):
        """실시간 트래킹 데이터 업데이트 (자동매도 로직)"""
        try:
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

            # 자동매도 로직 (항상 활성화)

            # 스탑로스 체크
            if 매도주문여부 == False and self.stopLossCheckBox.isChecked() and 수익률 < self.stopLossDoubleSpinBox.value():
                self.sell_order(종목코드, sell_reason=f"스탑로스 ({수익률:.2f}%)")
                return

            # 트레일링 스탑 발동 체크
            if all([
                트레일링발동여부 == False,
                매도주문여부 == False,
                self.trailingStopCheckBox.isChecked(),
                수익률 >= self.trailingStopDoubleSpinBox1.value(),
            ]):
                self.realtime_tracking_df.at[종목코드, "트레일링 발동 후 고가"] = 현재가
                self.realtime_tracking_df.at[종목코드, "트레일링 발동 여부"] = True
                self.add_log(f"트레일링 스탑 발동: {종목코드} 수익률 {수익률:.2f}%")

            # 트레일링 스탑 청산 체크
            if all([
                트레일링발동여부 == True,
                매도주문여부 == False,
                not pd.isnull(트레일링발동후고가),
                (현재가 - 트레일링발동후고가) / 트레일링발동후고가 * 100 < self.trailingStopDoubleSpinBox2.value(),
            ]):
                하락률 = (현재가 - 트레일링발동후고가) / 트레일링발동후고가 * 100
                self.sell_order(종목코드, sell_reason=f"트레일링 스탑 ({하락률:.2f}%)")
                return

        except Exception as e:
            logger.exception(f"실시간 트래킹 업데이트 중 오류: {e}")

    def update_active_conditions(self):
        """활성 조건식 수 업데이트"""
        if not hasattr(self, 'active_buy_conditions') or not hasattr(self, 'active_sell_conditions'):
            return

        active_buy_count = sum(1 for condition in self.active_buy_conditions
                               if self.flexible_sell_widget.is_condition_active_now(condition['name']))

        if self.is_auto_sell_only:
            active_sell_count = 0
            total_conditions = len(self.active_buy_conditions)
            active_conditions = active_buy_count
        else:
            active_sell_count = sum(1 for condition in self.active_sell_conditions
                                    if self.flexible_sell_widget.is_condition_active_now(condition['name']))
            total_conditions = len(self.active_buy_conditions) + len(self.active_sell_conditions)
            active_conditions = active_buy_count + active_sell_count

        self.status_widget.set_active_conditions(active_conditions, total_conditions)

    def on_receive_condition_list(self, data):
        """조건검색식 리스트 수신"""
        try:
            self.condition_df = data['df']
            self.condition_name_to_index_dict = dict(zip(self.condition_df['조건명'], self.condition_df['조건index']))
            self.condition_index_to_name_dict = dict(zip(self.condition_df['조건index'], self.condition_df['조건명']))

            # 유연한 매도 조건 위젯 업데이트
            self.flexible_sell_widget.update_condition_list(self.condition_df)

            self.load_settings(is_init=False)
            self.add_log(f"조건검색식 로드 완료: {len(self.condition_df)}개")

        except Exception as e:
            logger.exception(f"조건검색식 리스트 처리 중 오류: {e}")

    def execute_buy_order(self, 종목코드, basic_info_dict):
        """매수 주문 실행"""
        try:
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
                self.add_log(f"매수 주문 실패: {종목코드} - 주문수량 부족")
                return

            # 진입 조건식 정보 추가
            진입조건식 = self.realtime_tracking_df.at[
                종목코드, "진입조건식"] if 종목코드 in self.realtime_tracking_df.index else "Unknown"

            if self.order_tr_req_queue:
                self.order_tr_req_queue.put(
                    dict(
                        action_id="매수주문",
                        종목코드=종목코드,
                        주문수량=주문수량,
                        주문가격=주문가격,
                        시장가여부=시장가여부,
                    )
                )

            order_type = "시장가" if 시장가여부 else f"지정가({주문가격})"
            self.add_log(f"매수 주문: {종목코드} {주문수량}주 {order_type} (진입: {진입조건식})")

        except Exception as e:
            logger.exception(f"매수 주문 실행 중 오류: {e}")
            self.add_log(f"매수 주문 실행 실패: {종목코드} - {str(e)}")

    def add_log(self, message):
        """로그 추가"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.log_text_edit.append(log_entry)

        # 스크롤을 최하단으로 이동
        scrollbar = self.log_text_edit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def update_trailing_stop_enabled(self, enabled):
        """트레일링 스탑 활성화 상태 업데이트"""
        self.trailingStopDoubleSpinBox1.setEnabled(enabled)
        self.trailingStopDoubleSpinBox2.setEnabled(enabled)

    def clear_log(self):
        """로그 지우기"""
        self.log_text_edit.clear()

    def save_log(self):
        """로그 저장"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "로그 저장", f"trading_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "Text files (*.txt);;All files (*.*)"
        )

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.log_text_edit.toPlainText())
                self.add_log(f"로그가 저장되었습니다: {filename}")
            except Exception as e:
                self.add_log(f"로그 저장 실패: {str(e)}")

    def reset_data(self):
        """데이터 초기화"""
        reply = QMessageBox.question(
            self, "데이터 초기화",
            "모든 트래킹 데이터를 초기화하시겠습니까?\n이 작업은 되돌릴 수 없습니다.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.realtime_tracking_df = pd.DataFrame(
                columns=["종목명", "현재가", "매입가", "수익률(%)", "트레일링 발동 여부", "트레일링 발동 후 고가", "매수주문여부", "매도주문여부", "진입조건식"]
            )
            self.order_info_df = pd.DataFrame(columns=["주문접수시간", "종목코드", "주문수량", "매수매도구분", "발생조건식"])
            self.realtime_registered_codes_set.clear()
            self.amend_ordered_num_set.clear()
            self.add_log("모든 데이터가 초기화되었습니다.")

    @log_exceptions
    def load_settings(self, is_init=True):
        """설정 로드"""
        try:
            self.buyAmountLineEdit.setText(self.settings.value("buyAmountLineEdit", defaultValue="200,000", type=str))
            self.marketBuyRadioButton.setChecked(
                self.settings.value("marketBuyRadioButton", defaultValue=True, type=bool))
            self.limitBuyRadioButton.setChecked(
                self.settings.value("limitBuyRadioButton", defaultValue=False, type=bool))
            self.marketSellRadioButton.setChecked(
                self.settings.value("marketSellRadioButton", defaultValue=True, type=bool))
            self.limitSellRadioButton.setChecked(
                self.settings.value("limitSellRadioButton", defaultValue=False, type=bool))
            self.stopLossCheckBox.setChecked(self.settings.value("stopLossCheckBox", defaultValue=True, type=bool))
            self.trailingStopCheckBox.setChecked(
                self.settings.value("trailingStopCheckBox", defaultValue=True, type=bool))
            self.limitBuySpinBox.setValue(self.settings.value("limitBuySpinBox", 0, int))
            self.amendOrderSpinBox.setValue(self.settings.value("amendOrderSpinBox", DEFAULT_AMEND_TIME, int))
            self.maxAutoTradeCountSpinBox.setValue(self.settings.value("maxAutoTradeCountSpinBox", 10, int))
            self.limitSellSpinBox.setValue(self.settings.value("limitSellSpinBox", 0, int))
            self.stopLossDoubleSpinBox.setValue(self.settings.value("stopLossDoubleSpinBox", -2.0, float))
            self.trailingStopDoubleSpinBox1.setValue(self.settings.value("trailingStopDoubleSpinBox1", 2.0, float))
            self.trailingStopDoubleSpinBox2.setValue(self.settings.value("trailingStopDoubleSpinBox2", -1.0, float))

            # 매도 모드 설정 복원
            auto_sell_only = self.settings.value("auto_sell_only_mode", True, type=bool)
            if auto_sell_only:
                self.flexible_sell_widget.auto_sell_only_radio.setChecked(True)
            else:
                self.flexible_sell_widget.condition_sell_radio.setChecked(True)

            # 추가 설정
            self.api_key_edit.setText(self.settings.value("api_key", "", type=str))
            self.api_secret_edit.setText(self.settings.value("api_secret", "", type=str))
            self.api_url_edit.setText(self.settings.value("api_url", "", type=str))

            # 조건식 선택 상태 복원
            if not is_init and hasattr(self, 'flexible_sell_widget'):
                # 매수 조건식 선택 복원
                buy_selections = self.settings.value("selected_buy_conditions", [], type=list)
                for i in range(self.flexible_sell_widget.buy_condition_list.count()):
                    item = self.flexible_sell_widget.buy_condition_list.item(i)
                    if item.text() in buy_selections:
                        item.setSelected(True)

                # 매도 조건식 선택 복원 (조건식 모드인 경우만)
                if not auto_sell_only:
                    sell_selections = self.settings.value("selected_sell_conditions", [], type=list)
                    for i in range(self.flexible_sell_widget.sell_condition_list.count()):
                        item = self.flexible_sell_widget.sell_condition_list.item(i)
                        if item.text() in sell_selections:
                            item.setSelected(True)

                # 조건식별 시간 스케줄 복원
                saved_schedules = self.settings.value("condition_schedules", {}, type=dict)
                if saved_schedules:
                    self.flexible_sell_widget.condition_schedules.update(saved_schedules)

        except Exception as e:
            logger.exception(f"설정 로드 중 오류: {e}")
            self.add_log(f"설정 로드 실패: {str(e)}")

    @log_exceptions
    def save_settings(self):
        """설정 저장"""
        try:
            # 기본 설정
            self.settings.setValue('buyAmountLineEdit', self.buyAmountLineEdit.text())
            self.settings.setValue('marketBuyRadioButton', self.marketBuyRadioButton.isChecked())
            self.settings.setValue('limitBuyRadioButton', self.limitBuyRadioButton.isChecked())
            self.settings.setValue('marketSellRadioButton', self.marketSellRadioButton.isChecked())
            self.settings.setValue('limitSellRadioButton', self.limitSellRadioButton.isChecked())
            self.settings.setValue('stopLossCheckBox', self.stopLossCheckBox.isChecked())
            self.settings.setValue('trailingStopCheckBox', self.trailingStopCheckBox.isChecked())
            self.settings.setValue('limitBuySpinBox', self.limitBuySpinBox.value())
            self.settings.setValue('amendOrderSpinBox', self.amendOrderSpinBox.value())
            self.settings.setValue('stopLossDoubleSpinBox', self.stopLossDoubleSpinBox.value())
            self.settings.setValue('trailingStopDoubleSpinBox1', self.trailingStopDoubleSpinBox1.value())
            self.settings.setValue('trailingStopDoubleSpinBox2', self.trailingStopDoubleSpinBox2.value())
            self.settings.setValue('limitSellSpinBox', self.limitSellSpinBox.value())
            self.settings.setValue('maxAutoTradeCountSpinBox', self.maxAutoTradeCountSpinBox.value())

            # 매도 모드 설정 저장
            self.settings.setValue('auto_sell_only_mode', self.flexible_sell_widget.is_auto_sell_only_mode())

            # 추가 설정
            self.settings.setValue('api_key', self.api_key_edit.text())
            self.settings.setValue('api_secret', self.api_secret_edit.text())
            self.settings.setValue('api_url', self.api_url_edit.text())

            # 조건식 선택 상태 저장
            buy_selections = [item.text() for item in self.flexible_sell_widget.buy_condition_list.selectedItems()]
            sell_selections = [item.text() for item in self.flexible_sell_widget.sell_condition_list.selectedItems()]

            self.settings.setValue('selected_buy_conditions', buy_selections)
            self.settings.setValue('selected_sell_conditions', sell_selections)

            # 조건식별 시간 스케줄 저장
            self.settings.setValue('condition_schedules', self.flexible_sell_widget.condition_schedules)

            self.add_log("설정이 저장되었습니다.")
            QMessageBox.information(self, "설정 저장",
                                    f"설정이 성공적으로 저장되었습니다.\n매도방식: {'자동매도만' if self.flexible_sell_widget.is_auto_sell_only_mode() else '조건식+자동매도'}")

        except Exception as e:
            logger.exception(f"설정 저장 중 오류: {e}")
            self.add_log(f"설정 저장 실패: {str(e)}")
            QMessageBox.warning(self, "설정 저장 실패", f"설정 저장에 실패했습니다:\n{str(e)}")

    @staticmethod
    def get_order_price(now_price):
        """호가 단위에 맞는 주문가격 계산"""
        now_price = int(now_price)
        if now_price < 2000:
            return now_price
        elif 2000 <= now_price < 5000:
            return now_price - now_price % 5
        elif 5000 <= now_price < 20000:
            return now_price - now_price % 10
        elif 20000 <= now_price < 50000:
            return now_price - now_price % 50
        elif 50000 <= now_price < 200000:
            return now_price - now_price % 100
        elif 200000 <= now_price < 500000:
            return now_price - now_price % 500
        else:
            return now_price - now_price % 1000

    @staticmethod
    def get_tick_size(now_price):
        """호가 단위 계산"""
        now_price = int(now_price)
        if now_price < 2000:
            return 1
        elif 2000 <= now_price < 5000:
            return 5
        elif 5000 <= now_price < 20000:
            return 10
        elif 20000 <= now_price < 50000:
            return 50
        elif 50000 <= now_price < 200000:
            return 100
        elif 200000 <= now_price < 500000:
            return 500
        else:
            return 1000

    def register_realtime_info(self, stock_code):
        """실시간 정보 등록"""
        if stock_code not in self.realtime_registered_codes_set:
            self.realtime_registered_codes_set.add(stock_code)
            if self.websocket_req_queue:
                self.websocket_req_queue.put(
                    dict(
                        action_id="실시간등록",
                        종목코드=stock_code,
                    )
                )
            self.current_realtime_count += 1

    def receive_tr_result(self):
        """TR 결과 수신"""
        self.timer2.stop()
        try:
            if self.tr_result_queue and not self.tr_result_queue.empty():
                data = self.tr_result_queue.get()
                if data['action_id'] == "계좌조회":
                    self.on_receive_account_info(data)
                elif data['action_id'] == "주식기본정보":
                    self.on_receive_stock_info(data)
        except Exception as e:
            logger.exception(f"TR 결과 처리 중 오류: {e}")
        finally:
            self.timer2.start(100)

    def receive_websocket_result(self):
        """웹소켓 결과 수신"""
        self.timer1.stop()
        try:
            if self.websocket_result_queue and not self.websocket_result_queue.empty():
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
            logger.exception(f"웹소켓 결과 처리 중 오류: {e}")
        finally:
            self.timer1.start(10)

    def on_receive_account_info(self, data):
        """계좌 정보 수신 처리"""
        try:
            df = data['df']
            if len(df) > 0:
                self.account_info_df = df[["종목코드", "종목명", "현재가", "매입가", "보유수량", "매매가능수량", "수익률(%)"]]
                self.account_info_df.set_index("종목코드", inplace=True)

                for stock_code, row in self.account_info_df.iterrows():
                    self.register_realtime_info(stock_code)

                    if self.stock_code_to_basic_info_dict.get(stock_code) is None:
                        if self.tr_req_queue:
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

                self.add_log(f"계좌 정보 업데이트: {len(df)}개 종목")
                self.status_widget.set_connection_status(True)

            if not self.has_init:
                for stock_code, row in self.realtime_tracking_df.copy(deep=True).iterrows():
                    if stock_code not in self.account_info_df.index:
                        self.realtime_tracking_df.drop(stock_code, inplace=True)

            self.has_init = True

        except Exception as e:
            logger.exception(f"계좌 정보 처리 중 오류: {e}")
            self.add_log(f"계좌 정보 처리 실패: {str(e)}")

    def on_receive_stock_info(self, data):
        """주식 기본정보 수신 처리"""
        try:
            basic_info_dict = data['basic_info_dict']
            종목코드 = data['종목코드']
            self.stock_code_to_basic_info_dict[종목코드] = basic_info_dict

            if 종목코드 in self.realtime_tracking_df.index and self.realtime_tracking_df.at[종목코드, "매수주문여부"] == False:
                self.execute_buy_order(종목코드, basic_info_dict)

        except Exception as e:
            logger.exception(f"주식 기본정보 처리 중 오류: {e}")

    def on_receive_realtime_tick(self, data):
        """실시간 시세 수신"""
        try:
            종목코드 = data['종목코드']
            현재가 = data['현재가']

            if 종목코드 in self.account_info_df.index:
                self.account_info_df.at[종목코드, "현재가"] = 현재가
                매입가 = self.account_info_df.at[종목코드, "매입가"]
                수익률 = round((현재가 - 매입가) / 매입가 * 100 - self.transaction_cost, 2)
                self.account_info_df.at[종목코드, "수익률(%)"] = 수익률

                if 종목코드 in self.realtime_tracking_df.index:
                    self.on_realtime_tracking_df_update(종목코드, 현재가, 수익률)

        except Exception as e:
            logger.exception(f"실시간 시세 처리 중 오류: {e}")

    def on_receive_order_result(self, data):
        """주문 결과 수신"""
        try:
            종목코드 = data['종목코드']
            주문상태 = data['주문상태']
            주문구분 = data['주문구분']

            # 주문 접수/체결 로그에 매도 사유 포함
            if 주문상태 == "접수":
                매도사유 = ""
                if 주문구분 == "매도" and 종목코드 in self.realtime_tracking_df.index:
                    진입조건식 = self.realtime_tracking_df.at[
                        종목코드, "진입조건식"] if "진입조건식" in self.realtime_tracking_df.columns else "Unknown"
                    매도사유 = f" (진입: {진입조건식})"

                self.add_log(f"주문 접수: {종목코드} {주문구분}{매도사유}")

            # 체결 처리
            elif 주문상태 == "체결":
                if 주문구분 == "매수":
                    # 매수 체결 시 실시간 트래킹에서 매수주문여부를 True로 업데이트
                    if 종목코드 in self.realtime_tracking_df.index:
                        self.realtime_tracking_df.at[종목코드, "매수주문여부"] = True
                elif 주문구분 == "매도":
                    # 매도 체결 시 실시간 트래킹에서 제거
                    if 종목코드 in self.realtime_tracking_df.index:
                        self.realtime_tracking_df.drop(종목코드, inplace=True)

                self.add_log(f"주문 체결: {종목코드} {주문구분}")

        except Exception as e:
            logger.exception(f"주문 결과 처리 중 오류: {e}")

    def check_amend_orders(self):
        """정정 주문 체크"""
        try:
            # 구현 필요 시 여기에 정정 주문 로직 추가
            pass
        except Exception as e:
            logger.exception(f"정정 주문 체크 중 오류: {e}")

    def save_pickle(self):
        """데이터프레임 저장"""
        try:
            if not self.realtime_tracking_df.equals(self.last_saved_realtime_tracking_df):
                self.realtime_tracking_df.to_pickle("realtime_tracking_df.pkl")
                self.last_saved_realtime_tracking_df = self.realtime_tracking_df.copy(deep=True)
        except Exception as e:
            logger.exception(f"데이터 저장 중 오류: {e}")

    def update_pandas_models(self):
        """화면 모델 업데이트"""
        try:
            # 실시간 트래킹 테이블 업데이트
            if hasattr(self, 'autoTradeInfoTableView'):
                if not hasattr(self, 'realtime_tracking_model'):
                    self.realtime_tracking_model = PandasModel(self.realtime_tracking_df)
                    self.autoTradeInfoTableView.setModel(self.realtime_tracking_model)
                else:
                    self.realtime_tracking_model.update_data(self.realtime_tracking_df)

            # 계좌 정보 테이블 업데이트
            if hasattr(self, 'accountInfoTableView'):
                if not hasattr(self, 'account_info_model'):
                    self.account_info_model = PandasModel(self.account_info_df)
                    self.accountInfoTableView.setModel(self.account_info_model)
                else:
                    self.account_info_model.update_data(self.account_info_df)

            # 주문 정보 테이블 업데이트
            if hasattr(self, 'orderInfoTableView'):
                if not hasattr(self, 'order_info_model'):
                    self.order_info_model = PandasModel(self.order_info_df)
                    self.orderInfoTableView.setModel(self.order_info_model)
                else:
                    self.order_info_model.update_data(self.order_info_df)

            # 상태바 업데이트
            if hasattr(self, 'status_widget'):
                self.status_widget.set_realtime_count(self.current_realtime_count, self.max_realtime_count)

        except Exception as e:
            logger.exception(f"화면 업데이트 중 오류: {e}")

    def check_valid_time(self):
        """거래 유효 시간 체크"""
        try:
            now = datetime.datetime.now().time()
            start_time = datetime.time(9, 0)  # 09:00
            end_time = datetime.time(15, 30)  # 15:30

            # 거래 시간 외에는 자동매매 중지
            if not (start_time <= now <= end_time):
                if not self.is_no_transaction:
                    self.auto_trade_off()
                    self.add_log("거래 시간이 아니므로 자동매매를 중지합니다.")

        except Exception as e:
            logger.exception(f"거래 시간 체크 중 오류: {e}")

    def closeEvent(self, event):
        """프로그램 종료 시 호출"""
        reply = QMessageBox.question(
            self, "프로그램 종료",
            "자동매매 프로그램을 종료하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                # 자동매매가 실행 중이면 중지
                if not self.autoOnPushButton.isEnabled():
                    self.auto_trade_off()

                # 설정 저장
                self.save_settings()

                # 타이머 정지
                timers = [self.timer1, self.timer2, self.timer3, self.timer4, self.timer5, self.timer6]
                if hasattr(self, 'timer7'):
                    timers.append(self.timer7)

                for timer in timers:
                    if timer and timer.isActive():
                        timer.stop()

                self.add_log("프로그램이 종료됩니다.")
                event.accept()

            except Exception as e:
                logger.exception(f"프로그램 종료 중 오류: {e}")
                event.accept()
        else:
            event.ignore()


# 예외 처리 함수
sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    logger.debug(f"exctype: {exctype}, value: {value}, traceback: {traceback}")
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = my_exception_hook


# def main():
#     """메인 함수 (데모용)"""
#     try:
#         # 애플리케이션 시작
#         app = QApplication(sys.argv)
#         app.setStyle('Fusion')  # 모던한 스타일 적용
#
#         # 실제 환경에서는 Queue와 Process를 사용
#         # 여기서는 데모용으로 None으로 설정
#         kiwoom_api = KiwoomAPI(
#             tr_req_queue=None,
#             tr_result_queue=None,
#             order_tr_req_queue=None,
#             websocket_req_queue=None,
#             websocket_result_queue=None,
#         )
#
#         sys.exit(app.exec_())
#
#     except Exception as e:
#         logger.exception(f"메인 프로그램 실행 중 오류: {e}")
#         sys.exit(1)


if __name__ == "__main__":

    try:
        # Queue 생성
        tr_req_queue = Queue()
        tr_result_queue = Queue()
        order_tr_req_queue = Queue()
        websocket_req_queue = Queue()
        websocket_result_queue = Queue()

        # 프로세스 생성
        tr_gen_process = Process(
            target=tr_general_req_func,
            args=(tr_req_queue, tr_result_queue),
            daemon=True,
        )
        tr_order_process = Process(
            target=tr_order_req_func,
            args=(order_tr_req_queue, ),
            daemon=True,
        )
        tr_websocket_process = Process(
            target=run_websocket,
            args=(websocket_req_queue, websocket_result_queue),
            daemon=True,
        )

        # 프로세스 시작
        tr_gen_process.start()
        tr_order_process.start()
        tr_websocket_process.start()

        # 애플리케이션 시작
        app = QApplication(sys.argv)
        app.setStyle('Fusion')

        kiwoom_api = KiwoomAPI(
            tr_req_queue=tr_req_queue,
            tr_result_queue=tr_result_queue,
            order_tr_req_queue=order_tr_req_queue,
            websocket_req_queue=websocket_req_queue,
            websocket_result_queue=websocket_result_queue,
        )

        sys.exit(app.exec_())

    except Exception as e:
        logger.exception(f"메인 프로그램 실행 중 오류: {e}")
        sys.exit(1)


