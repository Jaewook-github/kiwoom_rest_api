
import sys
import datetime
from PyQt5.QtCore import Qt, QTime
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QTimeEdit, QCheckBox, QGroupBox, QTabWidget,
    QWidget, QScrollArea, QFrame, QButtonGroup, QRadioButton,
    QDialogButtonBox, QMessageBox, QSpacerItem, QSizePolicy
)


class EasyTimeSettingDialog(QDialog):
    """쉬운 시간 설정 다이얼로그"""

    def __init__(self, condition_schedules, parent=None):
        super().__init__(parent)
        self.condition_schedules = condition_schedules.copy()
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        self.setWindowTitle("📅 조건식 매매시간 설정 (쉬운 버전)")
        self.setModal(True)
        self.resize(800, 600)

        # 메인 레이아웃
        main_layout = QVBoxLayout(self)

        # 제목 및 안내
        title_layout = QHBoxLayout()
        title_label = QLabel("📋 조건식별 매매시간 설정")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2196F3;
                padding: 10px;
            }
        """)
        title_layout.addWidget(title_label)
        title_layout.addStretch()

        # 도움말 버튼
        help_button = QPushButton("❓ 도움말")
        help_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        help_button.clicked.connect(self.show_help)
        title_layout.addWidget(help_button)

        main_layout.addLayout(title_layout)

        # 안내 메시지
        info_label = QLabel("""
        💡 <b>간단 설정 가이드:</b><br>
        • <span style='color: #4CAF50;'><b>전체 적용</b></span>: 모든 조건식에 동일한 시간 적용<br>
        • <span style='color: #2196F3;'><b>개별 설정</b></span>: 조건식마다 다른 시간 설정<br>
        • <span style='color: #FF5722;'><b>비활성화</b></span>: 특정 조건식만 시간 제한 없이 사용
        """)
        info_label.setStyleSheet("""
            QLabel {
                background-color: #f0f8ff;
                border: 2px solid #e3f2fd;
                border-radius: 8px;
                padding: 12px;
                margin: 5px;
            }
        """)
        main_layout.addWidget(info_label)

        # 탭 위젯
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #f5f5f5;
                padding: 12px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 3px solid #2196F3;
                color: #2196F3;
            }
        """)

        # 전체 적용 탭
        self.create_global_tab()

        # 개별 설정 탭
        self.create_individual_tab()

        main_layout.addWidget(self.tab_widget)

        # 버튼 영역
        button_layout = QHBoxLayout()

        # 미리보기 버튼
        preview_button = QPushButton("👁️ 미리보기")
        preview_button.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
        """)
        preview_button.clicked.connect(self.show_preview)

        # 초기화 버튼
        reset_button = QPushButton("🔄 초기화")
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #795548;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5D4037;
            }
        """)
        reset_button.clicked.connect(self.reset_settings)

        button_layout.addWidget(preview_button)
        button_layout.addWidget(reset_button)
        button_layout.addStretch()

        # 확인/취소 버튼
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.setStyleSheet("""
            QDialogButtonBox QPushButton {
                padding: 10px 25px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 80px;
            }
            QDialogButtonBox QPushButton[text="OK"] {
                background-color: #4CAF50;
                color: white;
                border: none;
            }
            QDialogButtonBox QPushButton[text="OK"]:hover {
                background-color: #45a049;
            }
            QDialogButtonBox QPushButton[text="Cancel"] {
                background-color: #f44336;
                color: white;
                border: none;
            }
            QDialogButtonBox QPushButton[text="Cancel"]:hover {
                background-color: #da190b;
            }
        """)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        button_layout.addWidget(button_box)
        main_layout.addLayout(button_layout)

    def create_global_tab(self):
        """전체 적용 탭 생성"""
        global_widget = QWidget()
        layout = QVBoxLayout(global_widget)

        # 전체 설정 그룹
        global_group = QGroupBox("🌍 모든 조건식에 동일한 시간 적용")
        global_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 15px;
                background-color: #f8fff8;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                background-color: white;
                color: #4CAF50;
            }
        """)
        global_layout = QVBoxLayout(global_group)

        # 전체 활성화 체크박스
        self.global_enable_checkbox = QCheckBox("✅ 전체 조건식 시간 제한 활성화")
        self.global_enable_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                font-weight: bold;
                color: #2E7D32;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
        """)
        self.global_enable_checkbox.toggled.connect(self.on_global_enable_changed)
        global_layout.addWidget(self.global_enable_checkbox)

        # 시간 설정 영역
        time_frame = QFrame()
        time_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        time_layout = QGridLayout(time_frame)

        # 시작 시간
        start_label = QLabel("🕘 시작 시간:")
        start_label.setStyleSheet("font-weight: bold; color: #1976D2;")
        self.global_start_time = QTimeEdit()
        self.global_start_time.setTime(QTime(9, 0))
        self.global_start_time.setDisplayFormat("HH:mm")
        self.global_start_time.setStyleSheet("""
            QTimeEdit {
                font-size: 16px;
                font-weight: bold;
                padding: 8px;
                border: 2px solid #2196F3;
                border-radius: 6px;
                background-color: #e3f2fd;
            }
        """)

        # 종료 시간
        end_label = QLabel("🕕 종료 시간:")
        end_label.setStyleSheet("font-weight: bold; color: #D32F2F;")
        self.global_end_time = QTimeEdit()
        self.global_end_time.setTime(QTime(15, 30))
        self.global_end_time.setDisplayFormat("HH:mm")
        self.global_end_time.setStyleSheet("""
            QTimeEdit {
                font-size: 16px;
                font-weight: bold;
                padding: 8px;
                border: 2px solid #f44336;
                border-radius: 6px;
                background-color: #ffebee;
            }
        """)

        time_layout.addWidget(start_label, 0, 0)
        time_layout.addWidget(self.global_start_time, 0, 1)
        time_layout.addWidget(end_label, 0, 2)
        time_layout.addWidget(self.global_end_time, 0, 3)

        # 빠른 설정 버튼들
        quick_layout = QHBoxLayout()
        quick_label = QLabel("⚡ 빠른 설정:")
        quick_label.setStyleSheet("font-weight: bold;")
        quick_layout.addWidget(quick_label)

        presets = [
            ("전체 시간", "09:00", "15:30"),
            ("오전만", "09:00", "12:00"),
            ("오후만", "13:00", "15:30"),
            ("점심 제외", "09:00", "11:30")
        ]

        for name, start, end in presets:
            btn = QPushButton(name)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #E1F5FE;
                    border: 1px solid #0288D1;
                    border-radius: 4px;
                    padding: 6px 12px;
                    font-weight: bold;
                    color: #0277BD;
                }
                QPushButton:hover {
                    background-color: #B3E5FC;
                }
            """)
            btn.clicked.connect(lambda checked, s=start, e=end: self.set_global_time(s, e))
            quick_layout.addWidget(btn)

        quick_layout.addStretch()

        # 전체 적용 버튼
        apply_button = QPushButton("🔄 모든 조건식에 적용")
        apply_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        apply_button.clicked.connect(self.apply_global_settings)

        global_layout.addWidget(time_frame)
        global_layout.addLayout(quick_layout)
        global_layout.addWidget(apply_button)
        global_layout.addStretch()

        layout.addWidget(global_group)
        self.tab_widget.addTab(global_widget, "🌍 전체 적용")

    def create_individual_tab(self):
        """개별 설정 탭 생성"""
        individual_widget = QWidget()
        layout = QVBoxLayout(individual_widget)

        # 스크롤 영역
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
            }
        """)

        scroll_content = QWidget()
        self.individual_layout = QVBoxLayout(scroll_content)

        # 조건식별 설정 생성
        self.create_individual_settings()

        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

        self.tab_widget.addTab(individual_widget, "⚙️ 개별 설정")

    def create_individual_settings(self):
        """개별 조건식 설정 위젯들 생성"""
        # 기존 위젯들 제거
        for i in reversed(range(self.individual_layout.count())):
            item = self.individual_layout.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)

        self.condition_widgets = {}

        for condition_name in self.condition_schedules.keys():
            # 조건식별 그룹 박스
            group = QGroupBox(f"📊 {condition_name}")
            group.setStyleSheet("""
                QGroupBox {
                    font-weight: bold;
                    border: 2px solid #2196F3;
                    border-radius: 8px;
                    margin-top: 1ex;
                    padding-top: 15px;
                    background-color: #fafafe;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 10px 0 10px;
                    background-color: white;
                    color: #2196F3;
                }
            """)

            group_layout = QHBoxLayout(group)

            # 활성화 체크박스
            enable_checkbox = QCheckBox("활성화")
            enable_checkbox.setStyleSheet("""
                QCheckBox {
                    font-weight: bold;
                    color: #4CAF50;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
            """)

            # 시작 시간
            start_time = QTimeEdit()
            start_time.setTime(QTime(9, 0))
            start_time.setDisplayFormat("HH:mm")
            start_time.setStyleSheet("""
                QTimeEdit {
                    font-weight: bold;
                    padding: 6px;
                    border: 2px solid #2196F3;
                    border-radius: 4px;
                    background-color: #e3f2fd;
                }
            """)

            # 종료 시간
            end_time = QTimeEdit()
            end_time.setTime(QTime(15, 30))
            end_time.setDisplayFormat("HH:mm")
            end_time.setStyleSheet("""
                QTimeEdit {
                    font-weight: bold;
                    padding: 6px;
                    border: 2px solid #f44336;
                    border-radius: 4px;
                    background-color: #ffebee;
                }
            """)

            # 시간 위젯들 활성화/비활성화 연결
            def toggle_time_widgets(checked, start=start_time, end=end_time):
                start.setEnabled(checked)
                end.setEnabled(checked)

            enable_checkbox.toggled.connect(toggle_time_widgets)

            # 레이아웃 배치
            group_layout.addWidget(enable_checkbox)
            group_layout.addWidget(QLabel("시작:"))
            group_layout.addWidget(start_time)
            group_layout.addWidget(QLabel("종료:"))
            group_layout.addWidget(end_time)
            group_layout.addStretch()

            # 위젯 저장
            self.condition_widgets[condition_name] = {
                'enabled': enable_checkbox,
                'start_time': start_time,
                'end_time': end_time
            }

            self.individual_layout.addWidget(group)

        self.individual_layout.addStretch()

    def on_global_enable_changed(self, checked):
        """전체 활성화 상태 변경"""
        self.global_start_time.setEnabled(checked)
        self.global_end_time.setEnabled(checked)

    def set_global_time(self, start_str, end_str):
        """전체 시간 빠른 설정"""
        start_time = QTime.fromString(start_str, "HH:mm")
        end_time = QTime.fromString(end_str, "HH:mm")
        self.global_start_time.setTime(start_time)
        self.global_end_time.setTime(end_time)

    def apply_global_settings(self):
        """전체 설정을 모든 조건식에 적용"""
        if not self.global_enable_checkbox.isChecked():
            QMessageBox.warning(self, "경고", "전체 조건식 시간 제한을 먼저 활성화해주세요.")
            return

        start_time = self.global_start_time.time().toString("HH:mm:ss")
        end_time = self.global_end_time.time().toString("HH:mm:ss")

        for condition_name, widgets in self.condition_widgets.items():
            widgets['enabled'].setChecked(True)
            widgets['start_time'].setTime(self.global_start_time.time())
            widgets['end_time'].setTime(self.global_end_time.time())

        QMessageBox.information(self, "완료", f"모든 조건식에 {start_time} ~ {end_time} 시간이 적용되었습니다.")

    def show_preview(self):
        """설정 미리보기"""
        preview_text = "📋 현재 설정 미리보기:\n\n"

        for condition_name, widgets in self.condition_widgets.items():
            if widgets['enabled'].isChecked():
                start = widgets['start_time'].time().toString("HH:mm")
                end = widgets['end_time'].time().toString("HH:mm")
                preview_text += f"✅ {condition_name}: {start} ~ {end}\n"
            else:
                preview_text += f"❌ {condition_name}: 비활성화 (24시간)\n"

        QMessageBox.information(self, "설정 미리보기", preview_text)

    def reset_settings(self):
        """설정 초기화"""
        reply = QMessageBox.question(
            self, "설정 초기화",
            "모든 설정을 초기값(09:00~15:30, 모두 활성화)으로 되돌리시겠습니까?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # 전체 설정 초기화
            self.global_enable_checkbox.setChecked(True)
            self.global_start_time.setTime(QTime(9, 0))
            self.global_end_time.setTime(QTime(15, 30))

            # 개별 설정 초기화
            for widgets in self.condition_widgets.values():
                widgets['enabled'].setChecked(True)
                widgets['start_time'].setTime(QTime(9, 0))
                widgets['end_time'].setTime(QTime(15, 30))

            QMessageBox.information(self, "완료", "모든 설정이 초기화되었습니다.")

    def show_help(self):
        """도움말 표시"""
        help_text = """
📚 시간 설정 도움말

🌍 전체 적용 탭:
• 모든 조건식에 동일한 시간을 한 번에 설정
• 빠른 설정 버튼으로 자주 사용하는 시간대 선택
• "모든 조건식에 적용" 버튼으로 일괄 적용

⚙️ 개별 설정 탭:
• 조건식마다 다른 시간 설정 가능
• 체크박스를 해제하면 해당 조건식은 24시간 활성화
• 각 조건식별로 세밀한 시간 제어 가능

💡 추천 설정:
• 전체 시간: 09:00 ~ 15:30 (일반적인 거래시간)
• 오전만: 09:00 ~ 12:00 (오전 변동성 활용)
• 오후만: 13:00 ~ 15:30 (오후 마감 거래)
• 점심 제외: 09:00 ~ 11:30 (점심시간 변동성 회피)

⚠️ 주의사항:
• 시작 시간이 종료 시간보다 늦으면 경고 메시지 표시
• 설정은 즉시 적용되며 자동 저장됨
        """
        QMessageBox.information(self, "도움말", help_text)

    def load_settings(self):
        """기존 설정 로드"""
        # 조건식이 없으면 샘플 생성
        if not self.condition_schedules:
            sample_conditions = [
                "상승추세 조건식", "거래량 급증 조건식", "기술적 돌파 조건식",
                "하락추세 조건식", "거래량 감소 조건식"
            ]
            for condition in sample_conditions:
                self.condition_schedules[condition] = {
                    'start_time': '09:00:00',
                    'end_time': '15:30:00',
                    'enabled': True
                }

        # 개별 설정 위젯 생성
        self.create_individual_settings()

        # 기존 설정값 로드
        for condition_name, schedule in self.condition_schedules.items():
            if condition_name in self.condition_widgets:
                widgets = self.condition_widgets[condition_name]

                # 활성화 상태
                widgets['enabled'].setChecked(schedule.get('enabled', True))

                # 시간 설정
                start_time_str = schedule.get('start_time', '09:00:00')
                end_time_str = schedule.get('end_time', '15:30:00')

                start_time = QTime.fromString(start_time_str, "HH:mm:ss")
                end_time = QTime.fromString(end_time_str, "HH:mm:ss")

                widgets['start_time'].setTime(start_time)
                widgets['end_time'].setTime(end_time)

                # 활성화 상태에 따른 위젯 활성화
                enabled = schedule.get('enabled', True)
                widgets['start_time'].setEnabled(enabled)
                widgets['end_time'].setEnabled(enabled)

    def get_schedules(self):
        """설정된 스케줄 반환"""
        result = {}

        for condition_name, widgets in self.condition_widgets.items():
            enabled = widgets['enabled'].isChecked()
            start_time = widgets['start_time'].time().toString("HH:mm:ss")
            end_time = widgets['end_time'].time().toString("HH:mm:ss")

            # 시간 유효성 검사
            if enabled and start_time >= end_time:
                QMessageBox.warning(
                    self, "시간 설정 오류",
                    f"{condition_name}의 시작 시간이 종료 시간보다 늦습니다.\n시작: {start_time}, 종료: {end_time}"
                )
                return None

            result[condition_name] = {
                'start_time': start_time,
                'end_time': end_time,
                'enabled': enabled
            }

        return result


# ==========================================
# 📁 파일 2: 기존 코드 수정 부분
# ==========================================
# 기존 FlexibleSellConditionWidget 클래스의 open_time_setting_dialog 메서드를 아래와 같이 수정하세요

def open_time_setting_dialog(self):
    """쉬운 시간 설정 다이얼로그 열기"""
    try:
        # easy_time_setting.py에서 EasyTimeSettingDialog를 import
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
    except ImportError:
        QMessageBox.warning(
            self, "⚠️ 모듈 오류",
            "시간 설정 위젯을 불러올 수 없습니다.\n"
            "easy_time_setting.py 파일이 필요합니다."
        )


# ==========================================
# 📁 파일 3: 테스트용 코드 (선택사항)
# ==========================================
# 시간 설정 위젯만 따로 테스트하고 싶을 때 사용하세요

def test_easy_time_setting():
    """시간 설정 위젯 테스트"""
    app = QApplication(sys.argv)

    # 샘플 데이터
    sample_schedules = {
        "상승추세 조건식": {'start_time': '09:00:00', 'end_time': '15:30:00', 'enabled': True},
        "거래량 급증 조건식": {'start_time': '09:00:00', 'end_time': '12:00:00', 'enabled': True},
        "기술적 돌파 조건식": {'start_time': '13:00:00', 'end_time': '15:30:00', 'enabled': True},
        "하락추세 조건식": {'start_time': '09:00:00', 'end_time': '15:30:00', 'enabled': False},
    }

    dialog = EasyTimeSettingDialog(sample_schedules)

    if dialog.exec_() == QDialog.Accepted:
        result = dialog.get_schedules()
        if result:
            print("✅ 설정 결과:")
            for name, schedule in result.items():
                status = "활성화" if schedule['enabled'] else "비활성화"
                print(f"   📊 {name}: {schedule['start_time']} ~ {schedule['end_time']} ({status})")

    app.exec_()


if __name__ == '__main__':
    test_easy_time_setting()