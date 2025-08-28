import os
import pandas as pd
import json
from datetime import datetime
from pathlib import Path
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.enhanced_logging import log_info, log_error, log_debug


class DataManager:
    """데이터 파일 관리 클래스"""
    
    def __init__(self, base_dir="data"):
        self.base_dir = Path(base_dir)
        self.daily_dir = self.base_dir / "daily"
        self.realtime_dir = self.base_dir / "realtime"
        self.backup_dir = self.base_dir / "backup"
        self.analysis_dir = self.base_dir / "analysis"
        
        # 디렉토리 생성
        self.create_directories()
    
    def create_directories(self):
        """필요한 디렉토리들 생성"""
        directories = [
            self.base_dir,
            self.daily_dir,
            self.realtime_dir,
            self.backup_dir,
            self.backup_dir / "daily",    # daily 백업 폴더 추가
            self.backup_dir / "weekly",
            self.backup_dir / "monthly",
            self.analysis_dir
        ]
        
        for directory in directories:
            try:
                directory.mkdir(parents=True, exist_ok=True)
                log_debug(f"디렉토리 생성/확인: {directory}")
            except Exception as e:
                log_error(f"디렉토리 생성 실패: {directory} - {str(e)}")
        
        log_info(f"데이터 디렉토리 구조 생성 완료: {self.base_dir}")
    
    def get_daily_file_path(self, filename_prefix, date_str, extension):
        """일별 파일 경로 반환"""
        filename = f"{filename_prefix}_{date_str}.{extension}"
        return self.daily_dir / filename
    
    def get_realtime_file_path(self, filename):
        """실시간 파일 경로 반환"""
        return self.realtime_dir / filename
    
    def get_backup_file_path(self, backup_type, filename):
        """백업 파일 경로 반환"""
        return self.backup_dir / backup_type / filename
    
    def get_analysis_file_path(self, filename):
        """분석 파일 경로 반환"""
        return self.analysis_dir / filename
    
    # === 실시간 트래킹 데이터 관리 ===
    def load_realtime_tracking_df(self):
        """실시간 트래킹 데이터 로드"""
        file_path = self.get_realtime_file_path("realtime_tracking_df.pkl")
        
        try:
            if file_path.exists():
                df = pd.read_pickle(file_path)
                log_info(f"실시간 트래킹 데이터 로드 성공: {len(df)}개 종목")
                return df
            else:
                log_info("실시간 트래킹 데이터 파일 없음 - 새로 생성")
                return self._create_empty_realtime_df()
        except Exception as e:
            log_error(f"실시간 트래킹 데이터 로드 실패: {str(e)}")
            return self._create_empty_realtime_df()
    
    def save_realtime_tracking_df(self, df):
        """실시간 트래킹 데이터 저장"""
        file_path = self.get_realtime_file_path("realtime_tracking_df.pkl")
        
        try:
            df.to_pickle(file_path)
            log_debug("실시간 트래킹 데이터 저장 완료")
            return True
        except Exception as e:
            log_error(f"실시간 트래킹 데이터 저장 실패: {str(e)}")
            return False
    
    def _create_empty_realtime_df(self):
        """빈 실시간 트래킹 데이터프레임 생성"""
        return pd.DataFrame(columns=[
            "종목명", "현재가", "매입가", "수익률(%)",
            "트레일링 발동 여부", "트레일링 발동 후 고가",
            "매수주문여부", "매도주문여부",
            "매수조건식명", "매수조건식index",
            "매도조건식명", "매도사유"
        ])
    
    # === 당일 매도 데이터 관리 ===
    def load_today_sold_data(self, today_date):
        """당일 매도 데이터 로드"""
        file_path = self.get_daily_file_path("sold_stocks_detail", today_date, "pkl")
        
        try:
            if file_path.exists():
                df = pd.read_pickle(file_path)
                log_info(f"당일 매도 데이터 로드 성공: {len(df)}건")
                return df
            else:
                log_info("당일 매도 데이터 없음 - 새로 시작")
                return self._create_empty_sold_df()
        except Exception as e:
            log_error(f"당일 매도 데이터 로드 실패: {str(e)}")
            return self._create_empty_sold_df()
    
    def save_today_sold_data(self, df, today_date):
        """당일 매도 데이터 저장 (PKL + CSV)"""
        try:
            # PKL 파일 저장
            pkl_path = self.get_daily_file_path("sold_stocks_detail", today_date, "pkl")
            df.to_pickle(pkl_path)
            
            # CSV 파일 저장 (사람이 읽기 쉬운 형태)
            csv_path = self.get_daily_file_path("sold_stocks_detail", today_date, "csv")
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            
            log_info(f"당일 매도 데이터 저장 완료: {len(df)}건")
            return True
        except Exception as e:
            log_error(f"당일 매도 데이터 저장 실패: {str(e)}")
            return False
    
    def _create_empty_sold_df(self):
        """빈 매도 데이터프레임 생성"""
        return pd.DataFrame(columns=[
            "종목코드", "종목명", "매도시간", "매수조건식", "매도사유",
            "매입가", "매도가", "수익률", "보유기간", "매도금액"
        ])
    
    # === 조건식 성과 데이터 관리 ===
    def save_condition_performance(self, performance_data, today_date):
        """조건식 성과 데이터 저장"""
        file_path = self.get_daily_file_path("condition_performance", today_date, "json")
        
        try:
            with open(file_path, "w", encoding='utf-8') as f:
                json.dump(performance_data, f, ensure_ascii=False, indent=2)
            log_info("조건식 성과 데이터 저장 완료")
            return True
        except Exception as e:
            log_error(f"조건식 성과 데이터 저장 실패: {str(e)}")
            return False
    
    def load_condition_performance(self, today_date):
        """조건식 성과 데이터 로드"""
        file_path = self.get_daily_file_path("condition_performance", today_date, "json")
        
        try:
            if file_path.exists():
                with open(file_path, "r", encoding='utf-8') as f:
                    data = json.load(f)
                log_info("조건식 성과 데이터 로드 성공")
                return data
            else:
                return {}
        except Exception as e:
            log_error(f"조건식 성과 데이터 로드 실패: {str(e)}")
            return {}
    
    # === 시간대별 패턴 데이터 관리 ===
    def save_hourly_pattern(self, hourly_pattern_dict, today_date):
        """시간대별 패턴 데이터 저장"""
        file_path = self.get_daily_file_path("hourly_pattern", today_date, "csv")
        
        try:
            if hourly_pattern_dict:
                hourly_df = pd.DataFrame(
                    list(hourly_pattern_dict.items()),
                    columns=["시간", "매도건수"]
                )
                hourly_df.to_csv(file_path, index=False, encoding='utf-8-sig')
                log_info("시간대별 패턴 데이터 저장 완료")
                return True
            else:
                log_info("시간대별 패턴 데이터 없음")
                return False
        except Exception as e:
            log_error(f"시간대별 패턴 데이터 저장 실패: {str(e)}")
            return False
    
    # === 백업 관리 ===
    def create_daily_backup(self, today_date):
        """일일 데이터 백업"""
        try:
            backup_date = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # daily 백업 디렉토리 확실히 생성
            daily_backup_dir = self.backup_dir / "daily"
            daily_backup_dir.mkdir(parents=True, exist_ok=True)
            
            # 백업할 파일들
            files_to_backup = [
                ("sold_stocks_detail", "pkl"),
                ("sold_stocks_detail", "csv"),
                ("condition_performance", "json"),
                ("hourly_pattern", "csv")
            ]
            
            backup_count = 0
            for filename_prefix, extension in files_to_backup:
                source_path = self.get_daily_file_path(filename_prefix, today_date, extension)
                if source_path.exists():
                    backup_filename = f"{filename_prefix}_{today_date}_{backup_date}.{extension}"
                    backup_path = daily_backup_dir / backup_filename
                    
                    # 파일 복사
                    import shutil
                    shutil.copy2(source_path, backup_path)
                    backup_count += 1
                    log_debug(f"백업 파일 생성: {backup_filename}")
            
            # 실시간 트래킹 데이터 백업
            realtime_source = self.get_realtime_file_path("realtime_tracking_df.pkl")
            if realtime_source.exists():
                backup_filename = f"realtime_tracking_df_{backup_date}.pkl"
                backup_path = daily_backup_dir / backup_filename
                import shutil
                shutil.copy2(realtime_source, backup_path)
                backup_count += 1
                log_debug(f"실시간 데이터 백업: {backup_filename}")
            
            log_info(f"일일 백업 완료: {backup_count}개 파일")
            return True
            
        except Exception as e:
            log_error(f"일일 백업 실패: {str(e)}")
            return False
    
    def cleanup_old_backups(self, days_to_keep=30):
        """오래된 백업 파일 정리"""
        try:
            from datetime import datetime, timedelta
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            deleted_count = 0
            for backup_path in self.backup_dir.rglob("*"):
                if backup_path.is_file():
                    file_mtime = datetime.fromtimestamp(backup_path.stat().st_mtime)
                    if file_mtime < cutoff_date:
                        backup_path.unlink()
                        deleted_count += 1
            
            log_info(f"오래된 백업 파일 정리 완료: {deleted_count}개 파일 삭제")
            return True
            
        except Exception as e:
            log_error(f"백업 파일 정리 실패: {str(e)}")
            return False
    
    def get_file_info(self):
        """데이터 파일 현황 반환"""
        try:
            info = {
                "daily_files": len(list(self.daily_dir.glob("*"))),
                "realtime_files": len(list(self.realtime_dir.glob("*"))),
                "backup_files": len(list(self.backup_dir.glob("**/*"))),
                "analysis_files": len(list(self.analysis_dir.glob("*"))),
                "total_size_mb": self._calculate_total_size()
            }
            return info
        except Exception as e:
            log_error(f"파일 정보 조회 실패: {str(e)}")
            return {
                "daily_files": 0,
                "realtime_files": 0,
                "backup_files": 0,
                "analysis_files": 0,
                "total_size_mb": 0
            }
    
    def _calculate_total_size(self):
        """전체 데이터 크기 계산 (MB)"""
        total_size = 0
        try:
            for file_path in self.base_dir.rglob("*"):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
            return round(total_size / (1024 * 1024), 2)
        except:
            return 0


# 전역 데이터 매니저 인스턴스
data_manager = DataManager()
