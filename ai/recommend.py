# ============================================================
# AI 개인 맞춤형 학습 추천 시스템
# ai/recommend.py
# ============================================================


# ------------------------------------------------------------
# 1. 규칙 기반 학습 우선순위 계산
# ------------------------------------------------------------
def calculate_learning_priority(score, wrong_rate, study_time):
    """점수, 오답률, 공부시간을 이용해 학습 필요 점수를 계산합니다."""

    # 기본 학습 필요 점수입니다.
    priority_score = 0

    # -------------------------
    # 점수 평가
    # -------------------------

    # 60점 미만이면 학습 필요성이 매우 높습니다.
    if score < 60:
        priority_score += 40

    # 60점 이상 70점 미만입니다.
    elif score < 70:
        priority_score += 30

    # 70점 이상 80점 미만입니다.
    elif score < 80:
        priority_score += 20

    # 80점 이상 90점 미만입니다.
    elif score < 90:
        priority_score += 10

    # -------------------------
    # 오답률 평가
    # -------------------------

    # 오답률이 40%보다 높으면 매우 높은 학습 필요도로 판단합니다.
    if wrong_rate > 40:
        priority_score += 40

    # 오답률이 30%보다 높습니다.
    elif wrong_rate > 30:
        priority_score += 30

    # 오답률이 20%보다 높습니다.
    elif wrong_rate > 20:
        priority_score += 20

    # 오답률이 10%보다 높습니다.
    elif wrong_rate > 10:
        priority_score += 10

    # -------------------------
    # 공부시간 평가
    # -------------------------

    # 성적이나 오답률에 문제가 있을 때만
    # 부족한 공부시간을 추가로 반영합니다.
    if score < 80 or wrong_rate > 20:

        # 공부시간이 20분 미만이면 학습 부족 가능성이 높습니다.
        if study_time < 20:
            priority_score += 20

        # 20분 이상 30분 미만인 경우입니다.
        elif study_time < 30:
            priority_score += 10

    # 최종 규칙 기반 점수를 반환합니다.
    return priority_score


# ------------------------------------------------------------
# 2. AI + 규칙 기반 종합 우선순위 계산
# ------------------------------------------------------------
def calculate_total_priority(score, wrong_rate, study_time, need_percent):
    """규칙 기반 분석과 AI 예측을 결합합니다."""

    # 기존 규칙 기반 점수를 계산합니다.
    rule_score = calculate_learning_priority(
        score,
        wrong_rate,
        study_time
    )

    # AI 학습 필요 확률의 30%를 반영합니다.
    ai_score = need_percent * 0.3

    # 규칙 점수와 AI 점수를 합산합니다.
    total_score = rule_score + ai_score

    # 계산된 종합 우선순위를 반환합니다.
    return round(total_score, 1)


# ------------------------------------------------------------
# 3. 추천 공부시간 계산
# ------------------------------------------------------------
def calculate_recommended_time(
    score,
    wrong_rate,
    study_time,
    need_percent
):
    """학생의 상태에 따라 추천 공부시간을 계산합니다."""

    # 기본 추천 공부시간입니다.
    recommended_time = 30

    # 점수가 매우 낮으면 시간을 더 추가합니다.
    if score < 60:
        recommended_time += 20

    # 60~69점이면 15분을 추가합니다.
    elif score < 70:
        recommended_time += 15

    # 70~79점이면 10분을 추가합니다.
    elif score < 80:
        recommended_time += 10

    # 오답률이 매우 높으면 시간을 추가합니다.
    if wrong_rate > 40:
        recommended_time += 15

    # 오답률이 30%를 넘으면 시간을 추가합니다.
    elif wrong_rate > 30:
        recommended_time += 10

    # AI가 학습 필요성을 매우 높게 판단한 경우입니다.
    if need_percent >= 80:
        recommended_time += 10

    # 이미 공부시간이 긴 학생에게
    # 지나치게 긴 시간을 추천하지 않습니다.
    if study_time >= 60:
        recommended_time -= 10

    # 최소 공부시간은 20분입니다.
    recommended_time = max(20, recommended_time)

    # 최대 공부시간은 90분입니다.
    recommended_time = min(90, recommended_time)

    return recommended_time


# ------------------------------------------------------------
# 4. 추천 이유 생성
# ------------------------------------------------------------
def create_reasons(score, wrong_rate, study_time, need_percent):
    """학생의 실제 학습 데이터를 이용해 추천 이유를 생성합니다."""

    reasons = []

    # 점수에 따른 이유입니다.
    if score < 60:
        reasons.append(
            f"현재 점수가 {score}점으로 낮아 기초 개념 보완이 필요합니다."
        )

    elif score < 70:
        reasons.append(
            f"현재 점수가 {score}점으로 핵심 개념 복습이 필요합니다."
        )

    elif score < 80:
        reasons.append(
            f"현재 점수가 {score}점으로 추가 학습을 통해 성적 향상이 가능합니다."
        )

    # 오답률에 따른 이유입니다.
    if wrong_rate > 40:
        reasons.append(
            f"오답률이 {wrong_rate}%로 높아 틀린 문제에 대한 집중적인 복습이 필요합니다."
        )

    elif wrong_rate > 30:
        reasons.append(
            f"오답률이 {wrong_rate}%로 높은 편이므로 오답 분석이 필요합니다."
        )

    elif wrong_rate > 20:
        reasons.append(
            f"오답률이 {wrong_rate}%이므로 취약 문제를 다시 확인하는 것이 좋습니다."
        )

    # 공부시간에 따른 이유입니다.
    if study_time < 20 and (score < 80 or wrong_rate > 20):
        reasons.append(
            f"현재 공부시간이 {study_time}분으로 짧아 학습시간을 늘릴 필요가 있습니다."
        )

    elif study_time < 30 and (score < 80 or wrong_rate > 20):
        reasons.append(
            f"현재 공부시간이 {study_time}분으로 다소 부족합니다."
        )

    # AI 예측 결과를 이유에 포함합니다.
    if need_percent >= 80:
        reasons.append(
            f"AI 모델도 학습 필요 확률을 {need_percent}%로 높게 예측했습니다."
        )

    elif need_percent >= 50:
        reasons.append(
            f"AI 모델이 학습 필요 확률을 {need_percent}%로 예측했습니다."
        )

    # 특별한 취약 조건이 없는 경우입니다.
    if not reasons:
        reasons.append(
            "다른 과목과 비교한 종합 학습 우선순위를 바탕으로 추천되었습니다."
        )

    return reasons


# ------------------------------------------------------------
# 5. 과목별 맞춤 학습 방법
# ------------------------------------------------------------
def create_study_method(subject):
    """과목별로 다른 학습 방법을 추천합니다."""

    # 국어 학습 방법입니다.
    if subject == "국어":
        return (
            "틀린 문제의 지문과 선택지를 다시 읽고, "
            "오답의 근거를 직접 정리해 보세요."
        )

    # 수학 학습 방법입니다.
    elif subject == "수학":
        return (
            "틀린 문제와 관련된 개념과 공식을 먼저 복습한 뒤, "
            "비슷한 유형의 문제를 다시 풀어보세요."
        )

    # 영어 학습 방법입니다.
    elif subject == "영어":
        return (
            "틀린 문제에서 모르는 단어와 문법을 정리하고, "
            "지문을 다시 해석해 보세요."
        )

    # 과학 학습 방법입니다.
    elif subject == "과학":
        return (
            "틀린 문제와 관련된 핵심 개념과 원리를 정리하고, "
            "개념을 문제에 적용하는 연습을 해보세요."
        )

    # 등록되지 않은 과목의 기본 학습 방법입니다.
    return "오답을 확인하고 부족한 개념을 중심으로 복습해 보세요."


# ------------------------------------------------------------
# 6. 하나의 과목에 대한 추천 정보 생성
# ------------------------------------------------------------
def build_recommendation(result):
    """과목 하나의 최종 추천 정보를 생성합니다."""

    # AI 예측 정보를 가져옵니다.
    prediction = result["prediction"]

    # 각 데이터를 가져옵니다.
    score = result["score"]
    wrong_rate = result["wrong_rate"]
    study_time = result["study_time"]
    need_percent = prediction["need_percent"]
    subject = result["subject"]

    # 종합 우선순위를 계산합니다.
    priority_score = calculate_total_priority(
        score,
        wrong_rate,
        study_time,
        need_percent
    )

    # 최종 추천 정보를 반환합니다.
    return {
        "subject": subject,
        "need_percent": need_percent,
        "score": score,
        "wrong_rate": wrong_rate,
        "study_time": study_time,

        # 새롭게 추가된 종합 우선순위입니다.
        "priority_score": priority_score,

        # 추천 공부시간입니다.
        "study_recommendation": calculate_recommended_time(
            score,
            wrong_rate,
            study_time,
            need_percent
        ),

        # 추천 이유입니다.
        "reasons": create_reasons(
            score,
            wrong_rate,
            study_time,
            need_percent
        ),

        # 과목별 맞춤 학습 방법입니다.
        "study_method": create_study_method(subject)
    }


# ------------------------------------------------------------
# 7. 가장 우선적으로 공부할 과목 추천
# ------------------------------------------------------------
def recommend_subject(ai_results):
    """가장 학습 우선순위가 높은 과목 하나를 추천합니다."""

    # 분석 결과가 없으면 추천할 수 없습니다.
    if not ai_results:
        return None

    # 추천 후보를 저장합니다.
    candidates = []

    # 모든 과목을 확인합니다.
    for result in ai_results:

        # 필요한 데이터가 있는지 확인합니다.
        required_keys = (
            "subject",
            "score",
            "wrong_rate",
            "study_time",
            "prediction"
        )

        # 필수 데이터가 없으면 건너뜁니다.
        if not all(key in result for key in required_keys):
            continue

        # prediction이 딕셔너리인지 확인합니다.
        if not isinstance(result["prediction"], dict):
            continue

        # AI 학습 필요 확률이 없으면 건너뜁니다.
        if "need_percent" not in result["prediction"]:
            continue

        # 100점이고 오답률이 0%이면 추천 대상에서 제외합니다.
        if result["score"] == 100 and result["wrong_rate"] == 0:
            continue

        # 과목별 추천 정보를 생성합니다.
        recommendation = build_recommendation(result)

        # 후보 목록에 추가합니다.
        candidates.append(recommendation)

    # 추천 후보가 없으면 None을 반환합니다.
    if not candidates:
        return None

    # 우선순위가 높은 순서대로 정렬합니다.
    # 점수가 같으면 공부시간이 짧은 과목을 우선합니다.
    candidates.sort(
        key=lambda item: (
            item["priority_score"],
            -item["study_time"]
        ),
        reverse=True
    )

    # 가장 우선순위가 높은 과목을 반환합니다.
    return candidates[0]


# ------------------------------------------------------------
# 8. 공동 1순위 과목 추천
# ------------------------------------------------------------
def recommend_subjects(ai_results):
    """최고 우선순위가 같은 과목들을 반환합니다."""

    # 데이터가 없으면 빈 목록을 반환합니다.
    if not ai_results:
        return []

    recommendations = []

    # 모든 과목을 확인합니다.
    for result in ai_results:

        required_keys = (
            "subject",
            "score",
            "wrong_rate",
            "study_time",
            "prediction"
        )

        # 필요한 정보가 없으면 제외합니다.
        if not all(key in result for key in required_keys):
            continue

        # prediction 형식을 확인합니다.
        if not isinstance(result["prediction"], dict):
            continue

        # AI 확률이 없으면 제외합니다.
        if "need_percent" not in result["prediction"]:
            continue

        # 완벽한 과목은 추천하지 않습니다.
        if result["score"] == 100 and result["wrong_rate"] == 0:
            continue

        # 추천 정보를 생성합니다.
        recommendations.append(
            build_recommendation(result)
        )

    # 추천 결과가 없으면 빈 목록입니다.
    if not recommendations:
        return []

    # 최고 종합 우선순위 점수를 찾습니다.
    highest_score = max(
        item["priority_score"]
        for item in recommendations
    )

    # 최고 점수와 같은 과목만 반환합니다.
    return [
        item
        for item in recommendations
        if item["priority_score"] == highest_score
    ]


# ------------------------------------------------------------
# 9. AI 학습 우선순위 문구
# ------------------------------------------------------------
def create_priority_text(need_percent):

    # AI 학습 필요도가 80% 이상입니다.
    if need_percent >= 80:
        return "🔥 최우선 학습"

    # AI 학습 필요도가 50% 이상입니다.
    elif need_percent >= 50:
        return "⭐ 우선 학습"

    # 그 외의 경우입니다.
    return "📚 일반 학습"


# ------------------------------------------------------------
# 10. AI 분석 결과 요약
# ------------------------------------------------------------
def create_ai_summary(recommended_subject):

    # 추천 결과가 없는 경우입니다.
    if recommended_subject is None:
        return "AI 분석 결과가 없습니다."

    # 추천 정보를 가져옵니다.
    subject = recommended_subject["subject"]
    need_percent = recommended_subject["need_percent"]
    study_time = recommended_subject["study_recommendation"]

    # 최종 AI 요약 문장을 반환합니다.
    return (
        f"AI와 학습 데이터를 종합적으로 분석한 결과, "
        f"{subject} 과목을 가장 우선적으로 학습하는 것을 추천합니다. "
        f"AI 학습 필요 확률은 {need_percent}%이며, "
        f"오늘은 약 {study_time}분 학습하는 것이 좋습니다."
    )