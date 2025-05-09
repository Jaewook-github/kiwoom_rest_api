# data/cache.py
import os
import json
import pickle
import pandas as pd
from typing import Dict, List, Optional, Union, Any
from datetime import datetime, timedelta
import hashlib


class DataCache:
    """데이터 캐싱 관리 클래스"""
    
    def __init__(self, cache_dir: str = './cache'):
        """데이터 캐시 초기화
        
        Args:
            cache_dir: 캐시 디렉토리 경로
        """
        self.cache_dir = cache_dir
        self._ensure_cache_dir()
        
    def _ensure_cache_dir(self):
        """캐시 디렉토리 생성"""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
            
    def _get_cache_path(self, key: str, ext: str = 'pkl') -> str:
        """캐시 파일 경로 생성
        
        Args:
            key: 캐시 키
            ext: 파일 확장자
            
        Returns:
            str: 캐시 파일 경로
        """
        # 키를 해시로 변환하여 파일명으로 사용
        hashed_key = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{hashed_key}.{ext}")
        
    def save_dataframe(self, key: str, df: pd.DataFrame, expires: int = 86400) -> bool:
        """데이터프레임 캐싱
        
        Args:
            key: 캐시 키
            df: 저장할 데이터프레임
            expires: 유효 기간 (초)
            
        Returns:
            bool: 저장 성공 여부
        """
        try:
            cache_data = {
                'data': df,
                'expires_at': datetime.now() + timedelta(seconds=expires)
            }
            
            cache_path = self._get_cache_path(key)
            with open(cache_path, 'wb') as f:
                pickle.dump(cache_data, f)
                
            return True
        except Exception as e:
            print(f"캐시 저장 중 오류 발생: {e}")
            return False
            
    def load_dataframe(self, key: str) -> Optional[pd.DataFrame]:
        """데이터프레임 로드
        
        Args:
            key: 캐시 키
            
        Returns:
            Optional[pd.DataFrame]: 캐시된 데이터프레임 (없거나 만료된 경우 None)
        """
        cache_path = self._get_cache_path(key)
        
        if not os.path.exists(cache_path):
            return None
            
        try:
            with open(cache_path, 'rb') as f:
                cache_data = pickle.load(f)
                
            # 유효 기간 확인
            if datetime.now() > cache_data.get('expires_at', datetime.now()):
                # 만료된 캐시는 삭제
                os.remove(cache_path)
                return None
                
            return cache_data.get('data')
        except Exception as e:
            print(f"캐시 로드 중 오류 발생: {e}")
            return None
            
    def invalidate(self, key: str) -> bool:
        """특정 캐시 삭제
        
        Args:
            key: 캐시 키
            
        Returns:
            bool: 삭제 성공 여부
        """
        cache_path = self._get_cache_path(key)
        
        if os.path.exists(cache_path):
            try:
                os.remove(cache_path)
                return True
            except Exception as e:
                print(f"캐시 삭제 중 오류 발생: {e}")
        
        return False
        
    def clear_all(self) -> int:
        """모든 캐시 삭제
        
        Returns:
            int: 삭제된 캐시 파일 수
        """
        count = 0
        
        if not os.path.exists(self.cache_dir):
            return 0
            
        for filename in os.listdir(self.cache_dir):
            file_path = os.path.join(self.cache_dir, filename)
            
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                    count += 1
                except Exception as e:
                    print(f"캐시 파일 {filename} 삭제 중 오류 발생: {e}")
                    
        return count
        
    def get_cache_info(self) -> Dict[str, Any]:
        """캐시 정보 조회
        
        Returns:
            Dict[str, Any]: 캐시 정보
        """
        if not os.path.exists(self.cache_dir):
            return {"count": 0, "size": 0, "files": []}
            
        files = []
        total_size = 0
        
        for filename in os.listdir(self.cache_dir):
            file_path = os.path.join(self.cache_dir, filename)
            
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                files.append({
                    "name": filename,
                    "size": file_size,
                    "modified": file_mtime.strftime("%Y-%m-%d %H:%M:%S")
                })
                
                total_size += file_size
                
        return {
            "count": len(files),
            "size": total_size,
            "files": files
        }