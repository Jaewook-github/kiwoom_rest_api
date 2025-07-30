import requests
import json
import time
from datetime import datetime
from collections import defaultdict, deque
from enhanced_logging import logger, log_info, log_error, log_debug
import threading
from queue import Queue


class TelegramNotifier:
    def __init__(self, bot_token, chat_id, config=None):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.config = config or {}
        self.base_url = f"https://api.telegram.org/bot{bot_token}"

        # 스팸 방지를 위한 메시지 큐
        self.message_queue = Queue()
        self.message_history = deque(maxlen=100)  # 최근 100개 메시지 기록
        self.last_message_time = defaultdict(float)  # 종목별 마지막 메시지 시간

        # 메시지 전송 쓰레드 시작
        self.running = True
        self.sender_thread = threading.Thread(target=self._message_sender, daemon=True)
        self.sender_thread.start()

        log_info("텔레그램 알림 시스템 초기화 완료")

    def _message_sender(self):
        """메시지 전송 쓰레드"""
        while self.running:
            try:
                if not self.message_queue.empty():
                    message_data = self.message_queue.get(timeout=1)
                    self._send_message_direct(message_data['message'], message_data.get('priority', 'normal'))
                    time.sleep(1)  # 1초 간격으로 전송
                else:
                    time.sleep(0.1)
            except Exception as e:
                log_error(f"메시지 전송 쓰레드 오류: {str(e)}")

    def _send_message_direct(self, message, priority='normal'):
        """실제 메시지 전송"""
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'  # HTML 포맷 지원
            }

            response = requests.post(url, data=data, timeout=10)

            if response.status_code == 200:
                log_debug(f"텔레그램 메시지 전송 성공: {message[:50]}...")
                self.message_history.append({
                    'timestamp': datetime.now(),
                    'message': message[:100],
                    'status': 'success'
                })
            else:
                log_error(f"텔레그램 메시지 전송 실패: {response.status_code}, {response.text}")
                self.message_history.append({
                    'timestamp': datetime.now(),
                    'message': message[:100],
                    'status': 'failed'
                })

        except Exception as e:
            log_error(f"텔레그램 메시지 전송 오류: {str(e)}")

    def _should_send_message(self, stock_code, message_type, cooldown_seconds=30):
        """메시지 전송 여부 판단 (스팸 방지)"""
        key = f"{stock_code}_{message_type}"
        current_time = time.time()
        last_time = self.last_message_time.get(key, 0)

        if current_time - last_time < cooldown_seconds:
            return False

        self.last_message_time[key] = current_time
        return True

    def send_message(self, message, priority='normal', stock_code=None, message_type=None, cooldown=30):
        """메시지 큐에 추가"""
        # 설정에서 해당 타입의 알림이 비활성화된 경우 전송하지 않음
        if message_type and not self.config.get('alert_levels', {}).get(message_type, True):
            return

        # 스팸 방지 체크
        if stock_code and message_type and not self._should_send_message(stock_code, message_type, cooldown):
            log_debug(f"메시지 스팸 방지로 전송 생략: {stock_code} {message_type}")
            return

        self.message_queue.put({
            'message': message,
            'priority': priority,
            'timestamp': datetime.now()
        })

        log_debug(f"텔레그램 메시지 큐에 추가: {message[:50]}...")

    def send_buy_condition_alert(self, stock_code, stock_name, condition_name, current_price, buy_amount,
                                 expected_quantity):
        """매수 조건 편입 알림"""
        message = f"""🟢 <b>[매수 조건 편입]</b>
📊 종목: {stock_name}({stock_code})
🎯 조건식: "{condition_name}"
💰 현재가: {current_price:,}원
💵 매수금액: {buy_amount:,}원
📈 예상수량: {expected_quantity:,}주
⏰ 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

        self.send_message(message, priority='normal', stock_code=stock_code,
                          message_type='buy_condition', cooldown=60)

    def send_buy_order_alert(self, stock_code, stock_name, condition_name, order_price, order_quantity, order_no,
                             is_market_order=True):
        """매수 주문 접수 알림"""
        order_type = "시장가" if is_market_order else "지정가"
        price_text = f"{order_price:,}원 ({order_type})" if order_price else f"{order_type}"

        message = f"""🔵 <b>[매수 주문 접수]</b>
📊 종목: {stock_name}({stock_code})
🎯 발동조건: "{condition_name}"
💰 주문가격: {price_text}
📈 주문수량: {order_quantity:,}주
🎫 주문번호: {order_no}
⏰ 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

        self.send_message(message, priority='high', stock_code=stock_code,
                          message_type='buy_order', cooldown=10)

    def send_buy_filled_alert(self, stock_code, stock_name, condition_name, filled_price, filled_quantity,
                              filled_amount, avg_price):
        """매수 체결 완료 알림"""
        message = f"""✅ <b>[매수 체결 완료]</b>
📊 종목: {stock_name}({stock_code})
🎯 매수조건: "{condition_name}"
💰 체결가: {filled_price:,}원
📈 체결수량: {filled_quantity:,}주
💵 체결금액: {filled_amount:,}원
📊 평균단가: {avg_price:,}원
⏰ 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

        self.send_message(message, priority='high', stock_code=stock_code,
                          message_type='buy_filled', cooldown=5)

    def send_sell_condition_alert(self, stock_code, stock_name, buy_condition, sell_condition,
                                  current_price, profit_rate):
        """매도 조건 발동 알림"""
        message = f"""🟡 <b>[매도 조건 발동]</b>
📊 종목: {stock_name}({stock_code})
🎯 매도조건: "{sell_condition}"
💰 현재가: {current_price:,}원
📈 수익률: {profit_rate:+.2f}%
🔄 매수조건: "{buy_condition}" → 매도조건: "{sell_condition}"
⏰ 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

        self.send_message(message, priority='normal', stock_code=stock_code,
                          message_type='sell_condition', cooldown=60)

    def send_stop_loss_alert(self, stock_code, stock_name, buy_condition, current_price,
                             profit_rate, stop_loss_rate):
        """손절 발동 알림"""
        message = f"""🔴 <b>[손절 발동]</b>
📊 종목: {stock_name}({stock_code})
🎯 원매수조건: "{buy_condition}"
💰 현재가: {current_price:,}원
📉 수익률: {profit_rate:+.2f}%
🛑 손절기준: {stop_loss_rate}%
⏰ 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

        self.send_message(message, priority='urgent', stock_code=stock_code,
                          message_type='stop_loss', cooldown=5)

    def send_trailing_stop_alert(self, stock_code, stock_name, buy_condition, current_price,
                                 profit_rate, trailing_rate, high_price):
        """트레일링 스탑 발동 알림"""
        message = f"""🟠 <b>[트레일링 스탑 발동]</b>
📊 종목: {stock_name}({stock_code})
🎯 원매수조건: "{buy_condition}"
💰 현재가: {current_price:,}원
📈 수익률: {profit_rate:+.2f}%
🎯 트레일링 기준: +{trailing_rate}%
🔝 발동후 고가: {high_price:,}원
⏰ 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

        self.send_message(message, priority='high', stock_code=stock_code,
                          message_type='trailing_stop', cooldown=30)

    def send_sell_order_alert(self, stock_code, stock_name, buy_condition, sell_reason,
                              order_price, order_quantity, order_no, expected_profit_rate, is_market_order=True):
        """매도 주문 접수 알림"""
        order_type = "시장가" if is_market_order else "지정가"
        price_text = f"{order_price:,}원 ({order_type})" if order_price else f"{order_type}"

        message = f"""🔴 <b>[매도 주문 접수]</b>
📊 종목: {stock_name}({stock_code})
🎯 매수조건: "{buy_condition}"
🎯 매도사유: {sell_reason}
💰 주문가격: {price_text}
📉 주문수량: {order_quantity:,}주
🎫 주문번호: {order_no}
📈 예상수익률: {expected_profit_rate:+.2f}%
⏰ 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

        self.send_message(message, priority='high', stock_code=stock_code,
                          message_type='sell_order', cooldown=10)

    def send_sell_filled_alert(self, stock_code, stock_name, buy_condition, sell_reason,
                               filled_price, filled_quantity, filled_amount, buy_price,
                               realized_profit, profit_rate):
        """매도 체결 완료 알림"""
        profit_emoji = "🎉" if profit_rate > 0 else "😢" if profit_rate < -2 else "😐"

        message = f"""{profit_emoji} <b>[매도 체결 완료]</b>
📊 종목: {stock_name}({stock_code})
🎯 매수조건: "{buy_condition}"
🎯 매도사유: {sell_reason}
💰 체결가: {filled_price:,}원
📉 체결수량: {filled_quantity:,}주
💵 체결금액: {filled_amount:,}원
📊 매입가: {buy_price:,}원
💰 실현손익: {realized_profit:+,}원 ({profit_rate:+.2f}%)
⏰ 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

        self.send_message(message, priority='urgent', stock_code=stock_code,
                          message_type='sell_filled', cooldown=5)

    def send_error_alert(self, error_type, error_message, stock_code=None, stock_name=None):
        """에러 알림"""
        if stock_code and stock_name:
            message = f"""❌ <b>[주문 오류]</b>
📊 종목: {stock_name}({stock_code})
🚫 오류내용: {error_message}
⏰ 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
        else:
            message = f"""🚨 <b>[시스템 오류]</b>
⚠️ 오류유형: {error_type}
📝 상세내용: {error_message}
⏰ 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

        self.send_message(message, priority='urgent', stock_code=stock_code,
                          message_type='errors', cooldown=30)

    def send_daily_summary(self, summary_data):
        """일일 요약 알림"""
        buy_count = summary_data.get('buy_count', 0)
        sell_count = summary_data.get('sell_count', 0)
        buy_amount = summary_data.get('buy_amount', 0)
        sell_amount = summary_data.get('sell_amount', 0)
        realized_profit = summary_data.get('realized_profit', 0)
        unrealized_profit = summary_data.get('unrealized_profit', 0)
        success_rate = summary_data.get('success_rate', 0)
        condition_performance = summary_data.get('condition_performance', {})
        error_count = summary_data.get('error_count', 0)

        profit_emoji = "📈" if realized_profit > 0 else "📉" if realized_profit < 0 else "📊"

        message = f"""{profit_emoji} <b>[일일 매매 요약]</b>
📅 날짜: {datetime.now().strftime('%Y-%m-%d')}

💰 <b>매매 현황:</b>
  └ 매수: {buy_count}건 ({buy_amount:,}원)
  └ 매도: {sell_count}건 ({sell_amount:,}원)

🎯 <b>조건식별 성과:</b>"""

        for condition_name, performance in condition_performance.items():
            message += f"\n  └ \"{condition_name}\": 매수 {performance.get('buy_count', 0)}건, 수익률 {performance.get('avg_profit_rate', 0):+.1f}%"

        message += f"""

📊 <b>수익 현황:</b>
  └ 실현손익: {realized_profit:+,}원
  └ 평가손익: {unrealized_profit:+,}원

🎯 성공률: {success_rate:.1f}%"""

        if error_count > 0:
            message += f"\n⚠️ 오류: {error_count}건"

        message += f"\n⏰ 생성시간: {datetime.now().strftime('%H:%M:%S')}"

        self.send_message(message, priority='normal', message_type='daily_summary', cooldown=3600)

    def test_connection(self):
        """텔레그램 연결 테스트"""
        try:
            test_message = f"""🤖 <b>[시스템 테스트]</b>
✅ 텔레그램 알림 시스템이 정상적으로 연결되었습니다.
⏰ 테스트 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

            self.send_message(test_message, priority='normal', message_type='test')
            log_info("텔레그램 연결 테스트 메시지 전송")
            return True
        except Exception as e:
            log_error(f"텔레그램 연결 테스트 실패: {str(e)}")
            return False

    def get_message_stats(self):
        """메시지 전송 통계"""
        total_messages = len(self.message_history)
        success_count = sum(1 for msg in self.message_history if msg['status'] == 'success')
        failed_count = total_messages - success_count

        return {
            'total_messages': total_messages,
            'success_count': success_count,
            'failed_count': failed_count,
            'success_rate': (success_count / total_messages * 100) if total_messages > 0 else 0,
            'queue_size': self.message_queue.qsize()
        }

    def stop(self):
        """알림 시스템 종료"""
        self.running = False
        if self.sender_thread.is_alive():
            self.sender_thread.join(timeout=5)
        log_info("텔레그램 알림 시스템 종료")


# 싱글톤 패턴으로 전역 알림 객체 생성
_telegram_notifier = None


def initialize_telegram_notifier(bot_token, chat_id, config=None):
    """텔레그램 알림 시스템 초기화"""
    global _telegram_notifier
    _telegram_notifier = TelegramNotifier(bot_token, chat_id, config)
    return _telegram_notifier


def get_telegram_notifier():
    """전역 텔레그램 알림 객체 반환"""
    return _telegram_notifier


def send_telegram_alert(alert_type, **kwargs):
    """편의 함수: 알림 타입에 따른 메시지 전송"""
    notifier = get_telegram_notifier()
    if not notifier:
        log_error("텔레그램 알림 시스템이 초기화되지 않았습니다.")
        return

    try:
        if alert_type == 'buy_condition':
            notifier.send_buy_condition_alert(**kwargs)
        elif alert_type == 'buy_order':
            notifier.send_buy_order_alert(**kwargs)
        elif alert_type == 'buy_filled':
            notifier.send_buy_filled_alert(**kwargs)
        elif alert_type == 'sell_condition':
            notifier.send_sell_condition_alert(**kwargs)
        elif alert_type == 'stop_loss':
            notifier.send_stop_loss_alert(**kwargs)
        elif alert_type == 'trailing_stop':
            notifier.send_trailing_stop_alert(**kwargs)
        elif alert_type == 'sell_order':
            notifier.send_sell_order_alert(**kwargs)
        elif alert_type == 'sell_filled':
            notifier.send_sell_filled_alert(**kwargs)
        elif alert_type == 'error':
            notifier.send_error_alert(**kwargs)
        elif alert_type == 'daily_summary':
            notifier.send_daily_summary(**kwargs)
        else:
            log_error(f"알 수 없는 알림 타입: {alert_type}")
    except Exception as e:
        log_error(f"텔레그램 알림 전송 오류 ({alert_type}): {str(e)}")


if __name__ == "__main__":
    # 테스트 코드
    import os

    # 환경변수에서 토큰과 채팅ID 읽기 (실제 사용시)
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN')
    CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', 'YOUR_CHAT_ID')

    config = {
        'alert_levels': {
            'buy_condition': True,
            'buy_order': True,
            'buy_filled': True,
            'sell_condition': True,
            'sell_order': True,
            'sell_filled': True,
            'stop_loss': True,
            'trailing_stop': True,
            'errors': True,
            'daily_summary': True
        }
    }

    # 테스트 실행
    notifier = initialize_telegram_notifier(BOT_TOKEN, CHAT_ID, config)

    if notifier.test_connection():
        print("텔레그램 알림 시스템 테스트 성공!")

        # 테스트 알림 전송
        notifier.send_buy_condition_alert(
            stock_code="005930",
            stock_name="삼성전자",
            condition_name="급등주 포착",
            current_price=75000,
            buy_amount=200000,
            expected_quantity=2
        )

        time.sleep(2)

        # 통계 출력
        stats = notifier.get_message_stats()
        print(f"메시지 통계: {stats}")
    else:
        print("텔레그램 알림 시스템 테스트 실패!")

    # 종료
    notifier.stop()