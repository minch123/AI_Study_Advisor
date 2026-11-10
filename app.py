# Flask에서 필요한 기능을 가져옵니다.
from flask import Flask, render_template, request

# Flask 웹 기능과 페이지 이동, 세션 기능을 가져옵니다.
from flask import Flask, render_template, request, redirect, url_for, session

# 데이터베이스 테이블 생성 함수를 가져옵니다.
from database.database import create_table

# 저장된 학습 기록을 조회하는 함수를 가져옵니다.
from database.database import get_all_study_records

# 학습 기록 저장 함수를 가져옵니다.
from database.database import save_study_record

# AI 분석 결과를 이용하여 추천 과목을 결정하는 함수를 가져옵니다.
from ai.recommend import recommend_subject, recommend_subjects, create_ai_summary, create_priority_text

# AI 학습용 정답 데이터를 생성하는 함수를 가져옵니다.
from database.database import create_table, update_ai_labels, add_ai_columns

# 기존 취약도 분석 함수를 가져옵니다.
from analysis.analyzer import analyze_subjects

# 머신러닝 AI 예측 함수를 가져옵니다.
from ai.model import predict_study_need

# Flask 애플리케이션을 생성합니다.
app = Flask(__name__)


# 세션에서 로그인 상태를 확인할 때 사용할 비밀 키입니다.
# 로컬 개발용 예시이며, 실제 배포 전에는 안전한 환경 변수로 설정해야 합니다.
app.secret_key = "local-development-change-this-secret-key"


# 회원가입 페이지와 회원가입 요청을 처리합니다.
@app.route("/register", methods=["GET", "POST"])
def register():

    # GET 요청이면 회원가입 화면을 보여줍니다.
    if request.method == "GET":
        return render_template("register.html", message=None)

    # 입력받은 아이디의 앞뒤 공백을 제거합니다.
    username = request.form.get("username", "").strip()

    # 입력받은 비밀번호를 가져옵니다.
    password = request.form.get("password", "")

    # 데이터베이스에 회원가입 정보를 저장합니다.
    success, message = register_user(username, password)

    # 회원가입에 성공하면 로그인 화면으로 이동합니다.
    if success:
        return redirect(url_for("login"))

    # 실패하면 회원가입 화면에 오류 메시지를 표시합니다.
    return render_template("register.html", message=message)



# 첫 화면을 처리합니다.
@app.route("/")
def home():

    # 입력 화면을 표시합니다.
    return render_template("index.html")

# 저장된 학습 기록을 조회하는 주소입니다.
@app.route("/history")
def history():

    # 데이터베이스에서 모든 학습 기록을 가져옵니다.
    records = get_all_study_records()

    # 학습 기록을 최신순으로 정렬합니다.
    records = records.sort_values(
        by="id",
        ascending=False
    ) if not records.empty else records

    # 학습 기록 화면에 데이터를 전달합니다.
    return render_template(
        "history.html",
        records=records.to_dict(orient="records")
    )
# 학습 데이터를 분석하는 주소입니다.
@app.route("/analyze", methods=["POST"])
def analyze():

    # 학생 이름을 가져옵니다.
    student_name = request.form["student_name"]


    # ==============================
    # 국어 데이터
    # ==============================

    # 국어의 전체 문항 수를 입력받습니다.
    korean_total_text = request.form.get("korean_total_questions", "").strip()

    # 국어의 전체 문항 수가 비어 있는지 확인합니다.
    if not korean_total_text:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "국어의 전체 문항 수를 입력해주세요."

    # 입력된 문자를 숫자로 변환합니다.
    try:

        # 문자열을 정수로 변환합니다.
        korean_total_questions = int(korean_total_text)

    # 숫자로 변환할 수 없는 경우입니다.
    except ValueError:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "국어의 전체 문항 수는 숫자로 입력해주세요."

    # 국어의 전체 문항 수가 0 이하인지 확인합니다.
    if korean_total_questions <= 0:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "국어의 전체 문항 수는 1개 이상이어야 합니다."

    # 국어의 맞은 문항 수를 입력받습니다.
    korean_correct_text = request.form.get("korean_correct_questions", "").strip()

    # 국어의 맞은 문항 수가 비어 있는지 확인합니다.
    if not korean_correct_text:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "국어의 맞은 문항 수를 입력해주세요."

    # 입력된 문자를 숫자로 변환합니다.
    try:

        # 문자열을 정수로 변환합니다.
        korean_correct_questions = int(korean_correct_text)

    # 숫자로 변환할 수 없는 경우입니다.
    except ValueError:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "국어의 맞은 문항 수는 숫자로 입력해주세요."

    # 국어의 맞은 문항 수가 음수인지 확인합니다.
    if korean_correct_questions < 0:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "국어의 맞은 문항 수는 0개 이상이어야 합니다."

    # 국어의 맞은 문항 수가 전체 문항 수보다 많은지 확인합니다.
    if korean_correct_questions > korean_total_questions:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "국어의 맞은 문항 수는 전체 문항 수보다 많을 수 없습니다."

    # 국어의 공부 시간을 입력받습니다.
    korean_study_time = int(request.form["korean_study_time"])

    # 국어의 공부 시간이 음수인지 확인합니다.
    if korean_study_time < 0:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "국어의 공부 시간은 0분 이상이어야 합니다."

    # 맞은 문항 수를 기준으로 국어 점수를 100점 만점으로 계산합니다.
    korean_score = round((korean_correct_questions / korean_total_questions) * 100)

    # 틀린 문항 수를 계산합니다.
    korean_wrong_questions = korean_total_questions - korean_correct_questions

    # 틀린 문항의 비율을 백분율로 계산합니다.
    korean_wrong_rate = round(
        (korean_wrong_questions / korean_total_questions) * 100
    )
        # ==============================
    # 수학 데이터
    # ==============================

    # 수학의 전체 문항 수를 입력받습니다.
    math_total_text = request.form.get("math_total_questions", "").strip()

    # 수학의 전체 문항 수가 비어 있는지 확인합니다.
    if not math_total_text:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "수학의 전체 문항 수를 입력해주세요."

    # 입력된 문자를 숫자로 변환합니다.
    try:

        # 문자열을 정수로 변환합니다.
        math_total_questions = int(math_total_text)

    # 숫자로 변환할 수 없는 경우입니다.
    except ValueError:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "수학의 전체 문항 수는 숫자로 입력해주세요."

    # 수학의 전체 문항 수가 0 이하인지 확인합니다.
    if math_total_questions <= 0:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "수학의 전체 문항 수는 1개 이상이어야 합니다."

    # 수학의 맞은 문항 수를 입력받습니다.
    math_correct_text = request.form.get("math_correct_questions", "").strip()

    # 수학의 맞은 문항 수가 비어 있는지 확인합니다.
    if not math_correct_text:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "수학의 맞은 문항 수를 입력해주세요."

    # 입력된 문자를 숫자로 변환합니다.
    try:

        # 문자열을 정수로 변환합니다.
        math_correct_questions = int(math_correct_text)

    # 숫자로 변환할 수 없는 경우입니다.
    except ValueError:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "수학의 맞은 문항 수는 숫자로 입력해주세요."

    # 수학의 맞은 문항 수가 음수인지 확인합니다.
    if math_correct_questions < 0:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "수학의 맞은 문항 수는 0개 이상이어야 합니다."

    # 수학의 맞은 문항 수가 전체 문항 수보다 많은지 확인합니다.
    if math_correct_questions > math_total_questions:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "수학의 맞은 문항 수는 전체 문항 수보다 많을 수 없습니다."

    # 수학의 공부 시간을 입력받습니다.
    math_study_time = int(request.form["math_study_time"])

    # 수학의 공부 시간이 음수인지 확인합니다.
    if math_study_time < 0:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "수학의 공부 시간은 0분 이상이어야 합니다."

    # 맞은 문항 수를 기준으로 수학 점수를 100점 만점으로 계산합니다.
    math_score = round((math_correct_questions / math_total_questions) * 100)

    # 틀린 문항 수를 계산합니다.
    math_wrong_questions = math_total_questions - math_correct_questions

    # 틀린 문항의 비율을 백분율로 계산합니다.
    math_wrong_rate = round(
        (math_wrong_questions / math_total_questions) * 100
    )
    # ==============================
    # 영어 데이터
    # ==============================

    # 영어의 전체 문항 수를 입력받습니다.
    english_total_text = request.form.get("english_total_questions", "").strip()

    # 영어의 전체 문항 수가 비어 있는지 확인합니다.
    if not english_total_text:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "영어의 전체 문항 수를 입력해주세요."

    # 입력된 문자를 숫자로 변환합니다.
    try:

        # 문자열을 정수로 변환합니다.
        english_total_questions = int(english_total_text)

    # 숫자로 변환할 수 없는 경우입니다.
    except ValueError:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "영어의 전체 문항 수는 숫자로 입력해주세요."

    # 영어의 전체 문항 수가 0 이하인지 확인합니다.
    if english_total_questions <= 0:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "영어의 전체 문항 수는 1개 이상이어야 합니다."

    # 영어의 맞은 문항 수를 입력받습니다.
    english_correct_text = request.form.get("english_correct_questions", "").strip()

    # 영어의 맞은 문항 수가 비어 있는지 확인합니다.
    if not english_correct_text:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "영어의 맞은 문항 수를 입력해주세요."

    # 입력된 문자를 숫자로 변환합니다.
    try:

        # 문자열을 정수로 변환합니다.
        english_correct_questions = int(english_correct_text)

    # 숫자로 변환할 수 없는 경우입니다.
    except ValueError:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "영어의 맞은 문항 수는 숫자로 입력해주세요."

    # 영어의 맞은 문항 수가 음수인지 확인합니다.
    if english_correct_questions < 0:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "영어의 맞은 문항 수는 0개 이상이어야 합니다."

    # 영어의 맞은 문항 수가 전체 문항 수보다 많은지 확인합니다.
    if english_correct_questions > english_total_questions:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "영어의 맞은 문항 수는 전체 문항 수보다 많을 수 없습니다."

    # 영어의 공부 시간을 입력받습니다.
    english_study_time = int(request.form["english_study_time"])

    # 영어의 공부 시간이 음수인지 확인합니다.
    if english_study_time < 0:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "영어의 공부 시간은 0분 이상이어야 합니다."

    # 맞은 문항 수를 기준으로 영어 점수를 100점 만점으로 계산합니다.
    english_score = round(
        (english_correct_questions / english_total_questions) * 100
    )

    # 틀린 문항 수를 계산합니다.
    english_wrong_questions = english_total_questions - english_correct_questions

    # 틀린 문항의 비율을 백분율로 계산합니다.
    english_wrong_rate = round(
        (english_wrong_questions / english_total_questions) * 100
    )
        # ==============================
    # 과학 데이터
    # ==============================

    # 과학의 전체 문항 수를 입력받습니다.
    science_total_text = request.form.get("science_total_questions", "").strip()

    # 과학의 전체 문항 수가 비어 있는지 확인합니다.
    if not science_total_text:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "과학의 전체 문항 수를 입력해주세요."

    # 입력된 문자를 숫자로 변환합니다.
    try:

        # 문자열을 정수로 변환합니다.
        science_total_questions = int(science_total_text)

    # 숫자로 변환할 수 없는 경우입니다.
    except ValueError:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "과학의 전체 문항 수는 숫자로 입력해주세요."

    # 과학의 전체 문항 수가 0 이하인지 확인합니다.
    if science_total_questions <= 0:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "과학의 전체 문항 수는 1개 이상이어야 합니다."

    # 과학의 맞은 문항 수를 입력받습니다.
    science_correct_text = request.form.get("science_correct_questions", "").strip()

    # 과학의 맞은 문항 수가 비어 있는지 확인합니다.
    if not science_correct_text:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "과학의 맞은 문항 수를 입력해주세요."

    # 입력된 문자를 숫자로 변환합니다.
    try:

        # 문자열을 정수로 변환합니다.
        science_correct_questions = int(science_correct_text)

    # 숫자로 변환할 수 없는 경우입니다.
    except ValueError:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "과학의 맞은 문항 수는 숫자로 입력해주세요."

    # 과학의 맞은 문항 수가 음수인지 확인합니다.
    if science_correct_questions < 0:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "과학의 맞은 문항 수는 0개 이상이어야 합니다."

    # 과학의 맞은 문항 수가 전체 문항 수보다 많은지 확인합니다.
    if science_correct_questions > science_total_questions:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "과학의 맞은 문항 수는 전체 문항 수보다 많을 수 없습니다."

    # 과학의 공부 시간을 입력받습니다.
    science_study_time = int(request.form["science_study_time"])

    # 과학의 공부 시간이 음수인지 확인합니다.
    if science_study_time < 0:

        # 잘못된 입력이면 오류 메시지를 보여줍니다.
        return "과학의 공부 시간은 0분 이상이어야 합니다."

    # 맞은 문항 수를 기준으로 과학 점수를 100점 만점으로 계산합니다.
    science_score = round(
        (science_correct_questions / science_total_questions) * 100
    )

    # 틀린 문항 수를 계산합니다.
    science_wrong_questions = science_total_questions - science_correct_questions

    # 틀린 문항의 비율을 백분율로 계산합니다.
    science_wrong_rate = round(
        (science_wrong_questions / science_total_questions) * 100
    )
    # 과목별 데이터를 하나의 딕셔너리로 구성합니다.
    study_data = {

        "국어": {
            "score": korean_score,
            "wrong_rate": korean_wrong_rate,
            "study_time": korean_study_time
        },

        "수학": {
            "score": math_score,
            "wrong_rate": math_wrong_rate,
            "study_time": math_study_time
        },

        "영어": {
            "score": english_score,
            "wrong_rate": english_wrong_rate,
            "study_time": english_study_time
        },

        "과학": {
            "score": science_score,
            "wrong_rate": science_wrong_rate,
            "study_time": science_study_time
        }
    }


    # 데이터베이스에 학습 기록을 저장합니다.
    save_study_record(
    student_name,

    korean_score,
    korean_wrong_rate,
    korean_study_time,

    math_score,
    math_wrong_rate,
    math_study_time,

    english_score,
    english_wrong_rate,
    english_study_time,

    science_score,
    science_wrong_rate,
    science_study_time
    )

    # 새로 저장된 학습 기록을 포함하여 AI 정답 데이터를 갱신합니다.
    update_ai_labels()
    
    # 기존 규칙 기반 분석을 위한 점수 데이터입니다.
    score_data = {

        "국어": korean_score,
        "수학": math_score,
        "영어": english_score,
        "과학": science_score
    }


    # 규칙 기반 취약도 분석을 실행합니다.
    analysis_result = analyze_subjects(score_data)

    # AI가 각 과목을 분석할 수 있도록 준비합니다.
    ai_results = []


    # 모든 과목을 하나씩 분석합니다.
    for subject, data in study_data.items():

        # 현재 과목의 AI 예측 결과를 계산합니다.
        prediction = predict_study_need(
            data["score"],
            data["study_time"],
            data["wrong_rate"]
        )


        # AI 결과를 리스트에 추가합니다.
        ai_results.append({
            "subject": subject,
            "score": data["score"],
            "wrong_rate": data["wrong_rate"],
            "study_time": data["study_time"],
            "prediction": prediction
        })

    # 최고 우선순위 과목을 모두 가져옵니다.
    recommended_subjects = recommend_subjects(ai_results)

# 기존 기능과의 호환성을 위해 첫 번째 추천 과목도 유지합니다.
    recommended_subject = recommended_subjects[0] if recommended_subjects else None

    
    # AI 추천 결과를 자연어 문장으로 요약합니다.
    ai_summary = create_ai_summary(recommended_subject)

    # 추천할 과목이 있는지 확인합니다.
    if recommended_subject is not None:

        # 추천 과목이 있으면 학습 우선순위 문구를 만듭니다.
        priority_text = create_priority_text(
            recommended_subject["need_percent"]
        )

    else:

        # 추천할 과목이 없으면 안내 문구를 표시합니다.
        priority_text = "일반 학습"


    # AI 결과를 웹페이지에 전달합니다.
    return render_template(
    "result.html",

    recommended_subjects=recommended_subjects,

    student_name=student_name,

    study_data=study_data,

    analysis_result=analysis_result,

    ai_results=ai_results,

    recommended_subject=recommended_subject,

    ai_summary=ai_summary,

    priority_text=priority_text
)


# Render와 로컬 환경에서 데이터베이스 테이블을 초기화합니다.
create_table()

# AI 분석에 필요한 컬럼을 추가합니다.
add_ai_columns()


# Python 파일을 직접 실행했을 때 실행됩니다.
if __name__ == "__main__":

    # Flask 개발 서버를 실행합니다.
    app.run(debug=False)
