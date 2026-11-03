# Python의 시스템 경로를 관리하기 위한 모듈을 가져옵니다.
import sys

# 현재 파일의 위치를 기준으로 프로젝트 루트 폴더를 찾기 위한 모듈을 가져옵니다.
import os

# 현재 model.py의 상위 폴더인 프로젝트 루트 경로를 가져옵니다.
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 프로젝트 루트를 Python 모듈 검색 경로에 추가합니다.
sys.path.insert(0, project_root)

# Random Forest 분류 모델을 가져옵니다.
from sklearn.ensemble import RandomForestClassifier

# 학습 데이터와 테스트 데이터를 나누기 위해 사용합니다.
from sklearn.model_selection import train_test_split

# AI 모델의 정확도를 계산하기 위해 사용합니다.
from sklearn.metrics import accuracy_score

# 데이터베이스에서 학습 기록을 가져오는 함수를 가져옵니다.
from database.database import get_all_study_records


# 현재 학습되어 있는 AI 모델을 저장합니다.
model = None

# 현재 AI 모델의 정확도를 저장합니다.
model_accuracy = None


# 데이터베이스의 학습 기록을 AI가 사용할 형태로 변환합니다.
def prepare_training_data():

    # SQLite에서 모든 학습 기록을 가져옵니다.
    data = get_all_study_records()

    # 데이터가 하나도 없는 경우입니다.
    if len(data) == 0:

        # 학습할 데이터가 없다는 오류를 발생시킵니다.
        raise ValueError("데이터베이스에 학습 기록이 없습니다.")

    # AI가 학습할 입력 데이터를 저장할 리스트입니다.
    X = []

    # AI가 학습할 정답 데이터를 저장할 리스트입니다.
    y = []

    # 데이터베이스의 각 학습 기록을 하나씩 확인합니다.
    for _, row in data.iterrows():

        # 국어 데이터를 AI 학습 데이터에 추가합니다.
        X.append([
            row["korean_score"],
            row["korean_study_time"],
            row["korean_wrong_rate"]
        ])

        # 국어의 학습 필요 여부를 정답 데이터에 추가합니다.
        y.append(row["korean_need"])

        # 수학 데이터를 AI 학습 데이터에 추가합니다.
        X.append([
            row["math_score"],
            row["math_study_time"],
            row["math_wrong_rate"]
        ])

        # 수학의 학습 필요 여부를 정답 데이터에 추가합니다.
        y.append(row["math_need"])

        # 영어 데이터를 AI 학습 데이터에 추가합니다.
        X.append([
            row["english_score"],
            row["english_study_time"],
            row["english_wrong_rate"]
        ])

        # 영어의 학습 필요 여부를 정답 데이터에 추가합니다.
        y.append(row["english_need"])

        # 과학 데이터를 AI 학습 데이터에 추가합니다.
        X.append([
            row["science_score"],
            row["science_study_time"],
            row["science_wrong_rate"]
        ])

        # 과학의 학습 필요 여부를 정답 데이터에 추가합니다.
        y.append(row["science_need"])

    # 학습용 입력 데이터와 정답 데이터를 반환합니다.
    return X, y


# Random Forest AI 모델을 학습시키는 함수입니다.
def train_model():

    # 데이터베이스에서 AI 학습 데이터를 준비합니다.
    X, y = prepare_training_data()

    # 서로 다른 정답 종류가 2개 미만인지 확인합니다.
    if len(set(y)) < 2:

        # 분류 모델을 학습할 수 없다는 오류를 발생시킵니다.
        raise ValueError(
            "AI 학습을 위해서는 학습 필요(1)와 학습 불필요(0) 데이터가 모두 필요합니다."
        )

    # 데이터가 충분한 경우 학습 데이터와 테스트 데이터를 분리합니다.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # Random Forest 모델을 생성합니다.
    trained_model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    # 학습 데이터로 AI 모델을 학습시킵니다.
    trained_model.fit(X_train, y_train)

    # 테스트 데이터를 이용하여 AI 예측을 수행합니다.
    predictions = trained_model.predict(X_test)

    # 실제 정답과 AI 예측을 비교하여 정확도를 계산합니다.
    accuracy = accuracy_score(y_test, predictions)

    # 전역 모델 변수에 학습된 모델을 저장합니다.
    global model

    # 전역 정확도 변수에 정확도를 저장합니다.
    global model_accuracy

    # 학습된 모델을 저장합니다.
    model = trained_model

    # 정확도를 저장합니다.
    model_accuracy = accuracy

    # 학습된 모델을 반환합니다.
    return trained_model


# 학생의 학습 필요도를 예측하는 함수입니다.
def predict_study_need(score, study_time, wrong_rate):

    # 전역 AI 모델을 사용합니다.
    global model

    # 아직 AI 모델이 학습되지 않은 경우입니다.
    if model is None:

        # AI 모델을 학습합니다.
        train_model()

    # 학생의 학습 데이터를 AI 입력 형태로 변환합니다.
    student_data = [
        [score, study_time, wrong_rate]
    ]

    # AI가 학습 필요 여부를 예측합니다.
    prediction = model.predict(student_data)[0]

    # AI가 각 클래스에 대해 계산한 확률을 가져옵니다.
    probabilities = model.predict_proba(student_data)[0]

    # 학습 필요(1)의 확률을 가져옵니다.
    need_percent = round(probabilities[1] * 100)

    # 학습 불필요(0)의 확률을 가져옵니다.
    no_need_percent = round(probabilities[0] * 100)

    # 분석 결과를 딕셔너리 형태로 반환합니다.
    return {
        "prediction": int(prediction),
        "need_percent": need_percent,
        "no_need_percent": no_need_percent
    }


# 현재 AI 모델의 정확도를 가져오는 함수입니다.
def get_model_accuracy():

    # 현재 정확도가 저장되어 있는지 확인합니다.
    if model_accuracy is None:

        # 아직 모델이 학습되지 않았다면 학습합니다.
        train_model()

    # 정확도를 백분율로 변환하여 반환합니다.
    return round(model_accuracy * 100, 2)

