#!/usr/bin/env python3
"""
DataManager 테스트 스크립트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.data_manager import data_manager
from datetime import datetime

def test_data_manager():
    """DataManager 기능 테스트"""
    print("🔧 DataManager 테스트 시작...")
    
    # 1. 디렉토리 구조 확인
    print("\n📁 디렉토리 구조 확인:")
    print(f"  - Base: {data_manager.base_dir}")
    print(f"  - Daily: {data_manager.daily_dir}")
    print(f"  - Realtime: {data_manager.realtime_dir}")
    print(f"  - Backup: {data_manager.backup_dir}")
    print(f"  - Analysis: {data_manager.analysis_dir}")
    
    # 2. 파일 정보 확인
    print("\n📊 파일 현황:")
    info = data_manager.get_file_info()
    for key, value in info.items():
        print(f"  - {key}: {value}")
    
    # 3. 백업 테스트
    print("\n💾 백업 테스트:")
    today = datetime.now().strftime("%Y%m%d")
    success = data_manager.create_daily_backup(today)
    print(f"  - 백업 성공: {success}")
    
    # 4. 백업 후 파일 정보 재확인
    print("\n📊 백업 후 파일 현황:")
    info = data_manager.get_file_info()
    for key, value in info.items():
        print(f"  - {key}: {value}")
    
    print("\n✅ DataManager 테스트 완료!")

if __name__ == "__main__":
    test_data_manager()
