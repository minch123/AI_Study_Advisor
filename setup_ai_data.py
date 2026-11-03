# 데이터베이스의 AI 관련 함수를 가져옵니다.
from database.database import add_ai_columns

# 기존 데이터를 AI 학습용 정답 데이터로 변환하는 함수를 가져옵니다.
from database.database import update_ai_labels


# 프로그램 시작 메시지를 출력합니다.
print("AI 데이터베이스 설정을 시작합니다.")


# AI 학습용 컬럼을 추가합니다.
add_ai_columns()


# 기존 데이터에 AI 정답을 생성합니다.
update_ai_labels()


# 완료 메시지를 출력합니다.
print("AI 학습 데이터 설정이 완료되었습니다.")