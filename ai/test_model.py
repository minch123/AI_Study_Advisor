# AI 모델에서 학습 필요도 예측 함수를 가져옵니다.
from model import predict_study_need

# 테스트 시작 메시지를 출력합니다.
print("===== AI 예측 테스트 시작 =====")

# 테스트 학생의 점수, 공부 시간, 오답률을 입력합니다.
result = predict_study_need(
    score=90,
    study_time=60,
    wrong_rate=10
)

# AI 예측 결과를 출력합니다.
print("AI 예측 결과:", result)

# 테스트 종료 메시지를 출력합니다.
print("===== AI 예측 테스트 완료 =====")