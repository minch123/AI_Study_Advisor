# Python이 프로젝트 최상위 폴더를 찾을 수 있도록 os 모듈을 가져옵니다.
import os

# Python의 모듈 검색 경로를 관리하기 위해 sys 모듈을 가져옵니다.
import sys


# 현재 파일의 폴더인 ai 폴더의 상위 폴더를 가져옵니다.
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# 프로젝트 최상위 폴더를 Python 모듈 검색 경로에 추가합니다.
sys.path.insert(0, project_root)


# database 폴더의 database.py에서 함수를 가져옵니다.
from database.database import get_all_study_records


# 프로그램이 정상적으로 시작되었는지 출력합니다.
print("CHECK_DATA 시작")


# SQLite에서 모든 학습 기록을 가져옵니다.
data = get_all_study_records()


# 데이터베이스의 컬럼 이름을 출력합니다.
print("===== 데이터베이스 컬럼 =====")


# 모든 컬럼 이름을 리스트로 변환하여 출력합니다.
print(data.columns.tolist())


# 현재 저장된 학습 기록의 개수를 출력합니다.
print("===== 데이터 개수 =====")


# 데이터 개수를 출력합니다.
print(len(data))


# 실제 데이터 내용을 출력합니다.
print("===== 실제 데이터 =====")


# Pandas DataFrame을 출력합니다.
print(data)


# 프로그램이 정상적으로 종료되었음을 출력합니다.
print("CHECK_DATA 종료")