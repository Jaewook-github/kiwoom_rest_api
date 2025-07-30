import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from pathlib import Path
import re
from collections import defaultdict
import json


class LogAnalyzer:
    def __init__(self, logs_dir="logs"):
        self.logs_dir = Path(logs_dir)
        self.ensure_logs_exist()

    def ensure_logs_exist(self):
        """로그 디렉토리 존재 확인"""
        if not self.logs_dir.exists():
            print(f"로그 디렉토리가 존재하지 않습니다: {self.logs_dir}")
            return False
        return True

    def get_log_files(self, category=None, date=None):
        """특정 카테고리와 날짜의 로그 파일 목록 반환"""
        if date is None:
            date = datetime.now().strftime("%Y%m%d")

        if category:
            category_dir = self.logs_dir / category
            if category_dir.exists():
                pattern = f"*_{date}.log"
                return list(category_dir.glob(pattern))
        else:
            # 모든 카테고리의 로그 파일
            all_files = []
            for cat_dir in self.logs_dir.iterdir():
                if cat_dir.is_dir():
                    pattern = f"*_{date}.log"
                    all_files.extend(cat_dir.glob(pattern))
            return all_files

    def parse_log_line(self, line):
        """로그 라인 파싱"""
        # 로그 포맷: YYYY-MM-DD HH:MM:SS | LEVEL | MESSAGE
        pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \| (\w+)\s+ \| (.+)'
        match = re.match(pattern, line.strip())

        if match:
            timestamp_str, level, message = match.groups()
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            return {
                'timestamp': timestamp,
                'level': level,
                'message': message
            }
        return None

    def read_log_file(self, file_path):
        """로그 파일 읽기"""
        logs = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    parsed = self.parse_log_line(line)
                    if parsed:
                        logs.append(parsed)
        except Exception as e:
            print(f"파일 읽기 오류 {file_path}: {e}")
        return logs

    def analyze_trading_performance(self, date=None):
        """매매 성과 분석"""
        trading_files = self.get_log_files("trading", date)
        if not trading_files:
            print("매매 로그 파일이 없습니다.")
            return None

        all_logs = []
        for file_path in trading_files:
            logs = self.read_log_file(file_path)
            all_logs.extend(logs)

        # 매매 관련 로그 분석
        buy_orders = []
        sell_orders = []
        profits = []

        for log in all_logs:
            message = log['message']

            # 매수주문 분석
            if "매수주문 성공" in message or "매수체결" in message:
                # 종목코드와 가격 정보 추출
                stock_match = re.search(r'([A-Z가-힣]+)\((\d+)\)', message)
                price_match = re.search(r'체결가:\s*([\d,]+)', message)
                quantity_match = re.search(r'체결량:\s*([\d,]+)주', message)

                if stock_match and price_match:
                    stock_name, stock_code = stock_match.groups()
                    price = int(price_match.group(1).replace(',', ''))
                    quantity = int(quantity_match.group(1).replace(',', '')) if quantity_match else 0

                    buy_orders.append({
                        'timestamp': log['timestamp'],
                        'stock_code': stock_code,
                        'stock_name': stock_name,
                        'price': price,
                        'quantity': quantity,
                        'amount': price * quantity
                    })

            # 매도주문 분석
            elif "매도주문 성공" in message or "매도체결" in message:
                stock_match = re.search(r'([A-Z가-힣]+)\((\d+)\)', message)
                price_match = re.search(r'체결가:\s*([\d,]+)', message)
                quantity_match = re.search(r'체결량:\s*([\d,]+)주', message)

                if stock_match and price_match:
                    stock_name, stock_code = stock_match.groups()
                    price = int(price_match.group(1).replace(',', ''))
                    quantity = int(quantity_match.group(1).replace(',', '')) if quantity_match else 0

                    sell_orders.append({
                        'timestamp': log['timestamp'],
                        'stock_code': stock_code,
                        'stock_name': stock_name,
                        'price': price,
                        'quantity': quantity,
                        'amount': price * quantity
                    })

            # 수익률 정보 추출
            elif "수익률:" in message:
                profit_match = re.search(r'수익률:\s*([-\d.]+)%', message)
                if profit_match:
                    profit_rate = float(profit_match.group(1))
                    profits.append({
                        'timestamp': log['timestamp'],
                        'profit_rate': profit_rate
                    })

        # 데이터프레임 생성
        buy_df = pd.DataFrame(buy_orders)
        sell_df = pd.DataFrame(sell_orders)
        profit_df = pd.DataFrame(profits)

        # timestamp 컬럼을 datetime으로 명시적 변환
        if not buy_df.empty and 'timestamp' in buy_df.columns:
            buy_df['timestamp'] = pd.to_datetime(buy_df['timestamp'])
        if not sell_df.empty and 'timestamp' in sell_df.columns:
            sell_df['timestamp'] = pd.to_datetime(sell_df['timestamp'])
        if not profit_df.empty and 'timestamp' in profit_df.columns:
            profit_df['timestamp'] = pd.to_datetime(profit_df['timestamp'])

        return {
            'buy_orders': buy_df,
            'sell_orders': sell_df,
            'profits': profit_df,
            'summary': {
                'total_buy_count': len(buy_orders),
                'total_sell_count': len(sell_orders),
                'total_buy_amount': sum([order['amount'] for order in buy_orders]),
                'total_sell_amount': sum([order['amount'] for order in sell_orders])
            }
        }

    def analyze_error_patterns(self, date=None, days_back=7):
        """에러 패턴 분석"""
        error_summary = defaultdict(int)
        error_details = []

        # 최근 N일간의 에러 로그 분석
        for i in range(days_back):
            target_date = (datetime.now() - timedelta(days=i)).strftime("%Y%m%d")
            error_files = self.get_log_files("errors", target_date)

            for file_path in error_files:
                logs = self.read_log_file(file_path)
                for log in logs:
                    # 에러 타입 분류
                    message = log['message']

                    if "HTTP Error" in message:
                        error_summary["HTTP_ERROR"] += 1
                        error_details.append({
                            'date': target_date,
                            'timestamp': log['timestamp'],
                            'type': 'HTTP_ERROR',
                            'message': message[:100]  # 처음 100자만
                        })
                    elif "웹소켓" in message:
                        error_summary["WEBSOCKET_ERROR"] += 1
                        error_details.append({
                            'date': target_date,
                            'timestamp': log['timestamp'],
                            'type': 'WEBSOCKET_ERROR',
                            'message': message[:100]
                        })
                    elif "주문" in message:
                        error_summary["ORDER_ERROR"] += 1
                        error_details.append({
                            'date': target_date,
                            'timestamp': log['timestamp'],
                            'type': 'ORDER_ERROR',
                            'message': message[:100]
                        })
                    else:
                        error_summary["OTHER_ERROR"] += 1
                        error_details.append({
                            'date': target_date,
                            'timestamp': log['timestamp'],
                            'type': 'OTHER_ERROR',
                            'message': message[:100]
                        })

        return {
            'summary': dict(error_summary),
            'details': pd.DataFrame(error_details)
        }

    def analyze_system_performance(self, date=None):
        """시스템 성능 분석"""
        tr_files = self.get_log_files("tr_requests", date)
        websocket_files = self.get_log_files("websocket", date)

        performance_data = {
            'tr_request_count': 0,
            'websocket_message_count': 0,
            'tr_request_times': [],
            'error_count': 0
        }

        # TR 요청 분석
        for file_path in tr_files:
            logs = self.read_log_file(file_path)
            performance_data['tr_request_count'] += len(logs)

            # 요청 시간대별 분석
            for log in logs:
                hour = log['timestamp'].hour
                performance_data['tr_request_times'].append(hour)

        # 웹소켓 메시지 분석
        for file_path in websocket_files:
            logs = self.read_log_file(file_path)
            performance_data['websocket_message_count'] += len(logs)

        return performance_data

    def generate_daily_report(self, date=None):
        """일일 리포트 생성"""
        if date is None:
            date = datetime.now().strftime("%Y%m%d")

        print(f"일일 리포트 생성 중... ({date})")

        try:
            # 각 분석을 개별적으로 실행하고 에러 처리
            trading_analysis = None
            error_analysis = None
            performance_analysis = None

            try:
                trading_analysis = self.analyze_trading_performance(date)
                print("매매 분석 완료")
            except Exception as e:
                print(f"매매 분석 중 오류: {e}")
                trading_analysis = {'buy_orders': pd.DataFrame(), 'sell_orders': pd.DataFrame(),
                                    'profits': pd.DataFrame(), 'summary': {}}

            try:
                error_analysis = self.analyze_error_patterns(date, days_back=1)
                print("에러 분석 완료")
            except Exception as e:
                print(f"에러 분석 중 오류: {e}")
                error_analysis = {'summary': {}, 'details': pd.DataFrame()}

            try:
                performance_analysis = self.analyze_system_performance(date)
                print("성능 분석 완료")
            except Exception as e:
                print(f"성능 분석 중 오류: {e}")
                performance_analysis = {'tr_request_count': 0, 'websocket_message_count': 0,
                                        'tr_request_times': [], 'error_count': 0}

            report = {
                'date': date,
                'generated_at': datetime.now().isoformat(),
                'trading_analysis': trading_analysis,
                'error_analysis': error_analysis,
                'performance_analysis': performance_analysis
            }

            # 리포트 저장
            report_dir = self.logs_dir / "reports"
            report_dir.mkdir(exist_ok=True)

            report_file = report_dir / f"daily_report_{date}.json"

            # JSON 직렬화를 위한 데이터 변환
            try:
                serializable_report = self._make_serializable(report)
                print("데이터 직렬화 완료")

                with open(report_file, 'w', encoding='utf-8') as f:
                    json.dump(serializable_report, f, ensure_ascii=False, indent=2)

                print(f"일일 리포트 생성 완료: {report_file}")

            except Exception as e:
                print(f"리포트 저장 중 오류: {e}")
                # 간단한 텍스트 리포트로 대체 저장
                text_report_file = report_dir / f"daily_report_{date}.txt"
                with open(text_report_file, 'w', encoding='utf-8') as f:
                    f.write(f"일일 리포트 - {date}\n")
                    f.write(f"생성 시간: {datetime.now()}\n\n")
                    f.write(f"매매 현황:\n")
                    if trading_analysis and 'summary' in trading_analysis:
                        for key, value in trading_analysis['summary'].items():
                            f.write(f"  {key}: {value}\n")
                    f.write(f"\n에러 현황:\n")
                    if error_analysis and 'summary' in error_analysis:
                        for key, value in error_analysis['summary'].items():
                            f.write(f"  {key}: {value}\n")
                    f.write(f"\n성능 정보:\n")
                    if performance_analysis:
                        for key, value in performance_analysis.items():
                            if key != 'tr_request_times':  # 리스트는 제외
                                f.write(f"  {key}: {value}\n")
                print(f"텍스트 리포트 저장 완료: {text_report_file}")

            return report

        except Exception as e:
            print(f"리포트 생성 중 전체 오류: {e}")
            return None

    def _make_serializable(self, obj):
        """JSON 직렬화 가능하도록 변환"""
        if isinstance(obj, dict):
            return {key: self._make_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._make_serializable(item) for item in obj]
        elif isinstance(obj, pd.DataFrame):
            if obj.empty:
                return []
            # DataFrame의 모든 컬럼을 직렬화 가능하도록 변환
            df_dict = obj.copy()
            # Timestamp 컬럼들을 문자열로 변환
            for col in df_dict.columns:
                if df_dict[col].dtype == 'datetime64[ns]' or col == 'timestamp':
                    df_dict[col] = df_dict[col].dt.strftime('%Y-%m-%d %H:%M:%S') if hasattr(df_dict[col], 'dt') else \
                    df_dict[col].astype(str)
            return df_dict.to_dict('records')
        elif isinstance(obj, (datetime, pd.Timestamp)):
            return obj.isoformat() if hasattr(obj, 'isoformat') else str(obj)
        elif pd.isna(obj):
            return None
        elif hasattr(obj, 'item'):  # numpy 타입들 처리
            return obj.item()
        elif isinstance(obj, (pd.Int64Dtype, pd.Float64Dtype)):
            return str(obj)
        else:
            try:
                # 기본 JSON 직렬화 테스트
                import json
                json.dumps(obj)
                return obj
            except (TypeError, ValueError):
                return str(obj)

    def plot_trading_timeline(self, date=None):
        """매매 타임라인 시각화"""
        trading_data = self.analyze_trading_performance(date)
        if not trading_data or trading_data['buy_orders'].empty:
            print("매매 데이터가 없습니다.")
            return

        plt.figure(figsize=(15, 8))

        # 매수/매도 타임라인
        buy_df = trading_data['buy_orders']
        sell_df = trading_data['sell_orders']

        if not buy_df.empty:
            plt.scatter(buy_df['timestamp'], buy_df['price'],
                        c='red', marker='^', s=100, label='매수', alpha=0.7)

        if not sell_df.empty:
            plt.scatter(sell_df['timestamp'], sell_df['price'],
                        c='blue', marker='v', s=100, label='매도', alpha=0.7)

        plt.xlabel('시간')
        plt.ylabel('가격')
        plt.title(f'매매 타임라인 ({date or "오늘"})')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        # 이미지 저장
        chart_dir = self.logs_dir / "charts"
        chart_dir.mkdir(exist_ok=True)

        chart_file = chart_dir / f"trading_timeline_{date or datetime.now().strftime('%Y%m%d')}.png"
        plt.savefig(chart_file, dpi=300, bbox_inches='tight')
        plt.show()

        print(f"차트 저장 완료: {chart_file}")

    def print_summary(self, date=None):
        """요약 정보 출력"""
        if date is None:
            date = datetime.now().strftime("%Y%m%d")

        print(f"\n=== 로그 분석 요약 ({date}) ===")

        # 매매 분석
        trading_data = self.analyze_trading_performance(date)
        if trading_data:
            summary = trading_data['summary']
            print(f"\n[매매 현황]")
            print(f"  매수 주문: {summary['total_buy_count']}건")
            print(f"  매도 주문: {summary['total_sell_count']}건")
            print(f"  총 매수금액: {summary['total_buy_amount']:,}원")
            print(f"  총 매도금액: {summary['total_sell_amount']:,}원")

        # 에러 분석
        error_data = self.analyze_error_patterns(date, days_back=1)
        if error_data['summary']:
            print(f"\n[에러 현황]")
            for error_type, count in error_data['summary'].items():
                print(f"  {error_type}: {count}건")

        # 성능 분석
        performance_data = self.analyze_system_performance(date)
        print(f"\n[시스템 성능]")
        print(f"  TR 요청: {performance_data['tr_request_count']}건")
        print(f"  웹소켓 메시지: {performance_data['websocket_message_count']}건")


if __name__ == "__main__":
    # 사용 예시
    try:
        analyzer = LogAnalyzer()

        # 오늘 로그 분석
        print("=== 로그 분석 시작 ===")
        analyzer.print_summary()

        # 매매 타임라인 차트 생성 (데이터가 있는 경우에만)
        print("\n=== 차트 생성 ===")
        try:
            analyzer.plot_trading_timeline()
        except Exception as e:
            print(f"차트 생성 실패: {e}")

        # 일일 리포트 생성
        print("\n=== 리포트 생성 ===")
        analyzer.generate_daily_report()

        print("\n=== 분석 완료 ===")

    except Exception as e:
        print(f"로그 분석 중 오류 발생: {e}")
        import traceback

        traceback.print_exc()