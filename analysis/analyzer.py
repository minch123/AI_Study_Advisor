# 학습 데이터를 분석하는 함수를 정의합니다.
def analyze_subjects(study_data):

    # 분석 결과를 저장할 빈 리스트를 만듭니다.
    analysis_result = []

    # 전달받은 모든 과목과 점수를 하나씩 확인합니다.
    for subject, score in study_data.items():

        # 점수가 낮을수록 취약도가 높아지도록 계산합니다.
        weakness_score = 100 - score

        # 현재 과목의 분석 결과를 딕셔너리로 만듭니다.
        subject_result = {
            "subject": subject,
            "score": score,
            "weakness_score": weakness_score
        }

        # 현재 과목의 분석 결과를 리스트에 추가합니다.
        analysis_result.append(subject_result)

    # 취약도가 높은 과목부터 정렬합니다.
    analysis_result.sort(
        key=lambda item: item["weakness_score"],
        reverse=True
    )

    # 최종 분석 결과를 반환합니다.
    return analysis_result