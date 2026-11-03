# SQLite 데이터베이스를 사용하기 위한 모듈을 가져옵니다.
import sqlite3

# 데이터베이스 파일 이름을 지정합니다.
DATABASE_NAME = "database/study.db"


# 데이터베이스 연결을 생성하는 함수를 정의합니다.
def get_connection():

    # study.db 파일에 연결합니다.
    connection = sqlite3.connect(DATABASE_NAME)

    # 조회 결과를 딕셔너리처럼 사용할 수 있도록 설정합니다.
    connection.row_factory = sqlite3.Row

    # 데이터베이스 연결 객체를 반환합니다.
    return connection


# 학습 기록 테이블을 생성하는 함수를 정의합니다.
def create_table():

    # 데이터베이스에 연결합니다.
    connection = get_connection()

    # SQL 명령을 실행하기 위한 커서를 생성합니다.
    cursor = connection.cursor()

    # 학습 기록 테이블을 생성합니다.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,

            korean_score INTEGER NOT NULL,
            korean_wrong_rate INTEGER NOT NULL,
            korean_study_time INTEGER NOT NULL,

            math_score INTEGER NOT NULL,
            math_wrong_rate INTEGER NOT NULL,
            math_study_time INTEGER NOT NULL,

            english_score INTEGER NOT NULL,
            english_wrong_rate INTEGER NOT NULL,
            english_study_time INTEGER NOT NULL,

            science_score INTEGER NOT NULL,
            science_wrong_rate INTEGER NOT NULL,
            science_study_time INTEGER NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 변경된 데이터베이스 내용을 저장합니다.
    connection.commit()

    # 데이터베이스 연결을 종료합니다.
    connection.close()


# SQLite 데이터베이스를 사용하기 위한 sqlite3 모듈을 가져옵니다.
import sqlite3


# Pandas를 가져옵니다.
import pandas as pd


# 데이터베이스 파일의 위치를 지정합니다.
DB_PATH = "database/study.db"


# 학습 기록을 저장하는 함수입니다.
def save_study_record(
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
):

    # SQLite 데이터베이스에 연결합니다.
    conn = sqlite3.connect(DB_PATH)

    # SQL INSERT 명령을 준비합니다.
    query = """
    INSERT INTO study_records (
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
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    # 학생의 학습 데이터를 데이터베이스에 저장합니다.
    conn.execute(
        query,
        (
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
    )

    # 변경된 내용을 데이터베이스에 저장합니다.
    conn.commit()

    # 데이터베이스 연결을 종료합니다.
    conn.close()


# 지금까지 저장된 모든 학습 기록을 가져오는 함수입니다.
def get_all_study_records():

    # SQLite 데이터베이스에 연결합니다.
    conn = sqlite3.connect(DB_PATH)

    # study_records 테이블의 모든 데이터를 가져옵니다.
    dataframe = pd.read_sql_query(
        "SELECT * FROM study_records",
        conn
    )

    # 데이터베이스 연결을 종료합니다.
    conn.close()

    # Pandas DataFrame을 반환합니다.
    return dataframe
# 기존 학습 기록에 AI 학습 필요 여부를 계산하는 함수입니다.
def calculate_study_need(score, wrong_rate, study_time):

    # 점수가 70점 미만인 경우입니다.
    if score < 70:

        # 추가 학습이 필요하다고 판단합니다.
        return 1

    # 오답률이 30%보다 높은 경우입니다.
    if wrong_rate > 30:

        # 추가 학습이 필요하다고 판단합니다.
        return 1

    # 공부 시간이 30분보다 적은 경우입니다.
    if study_time < 30:

        # 추가 학습이 필요하다고 판단합니다.
        return 1

    # 위 조건에 해당하지 않으면 학습 상태가 양호하다고 판단합니다.
    return 0
# SQLite 데이터베이스에 필요한 AI 학습용 컬럼을 추가하는 함수입니다.
def add_ai_columns():

    # SQLite 데이터베이스에 연결합니다.
    conn = sqlite3.connect(DB_PATH)

    # 데이터베이스 커서를 생성합니다.
    cursor = conn.cursor()

    # 현재 study_records 테이블의 컬럼 정보를 가져옵니다.
    cursor.execute("PRAGMA table_info(study_records)")

    # 컬럼 정보를 모두 가져옵니다.
    columns = cursor.fetchall()

    # 현재 존재하는 컬럼 이름만 따로 저장합니다.
    column_names = [column[1] for column in columns]

    # 국어 학습 필요 여부 컬럼이 없는 경우입니다.
    if "korean_need" not in column_names:

        # 국어 AI 정답 컬럼을 추가합니다.
        cursor.execute(
            "ALTER TABLE study_records ADD COLUMN korean_need INTEGER"
        )

    # 수학 학습 필요 여부 컬럼이 없는 경우입니다.
    if "math_need" not in column_names:

        # 수학 AI 정답 컬럼을 추가합니다.
        cursor.execute(
            "ALTER TABLE study_records ADD COLUMN math_need INTEGER"
        )

    # 영어 학습 필요 여부 컬럼이 없는 경우입니다.
    if "english_need" not in column_names:

        # 영어 AI 정답 컬럼을 추가합니다.
        cursor.execute(
            "ALTER TABLE study_records ADD COLUMN english_need INTEGER"
        )

    # 과학 학습 필요 여부 컬럼이 없는 경우입니다.
    if "science_need" not in column_names:

        # 과학 AI 정답 컬럼을 추가합니다.
        cursor.execute(
            "ALTER TABLE study_records ADD COLUMN science_need INTEGER"
        )

    # 데이터베이스 변경사항을 저장합니다.
    conn.commit()

    # 데이터베이스 연결을 종료합니다.
    conn.close()
    # 기존 학습 데이터에 AI 학습 필요 여부를 자동으로 생성하는 함수입니다.
    # 점수, 오답률, 공부 시간을 이용해 학습 필요 여부를 계산합니다.
def calculate_study_need(score, wrong_rate, study_time):

    # 점수가 70점 미만이면 학습이 필요하다고 판단합니다.
    if score < 70:
        return 1

    # 오답률이 30%를 초과하면 학습이 필요하다고 판단합니다.
    if wrong_rate > 30:
        return 1

    # 공부 시간이 30분보다 적으면 학습이 필요하다고 판단합니다.
    if study_time < 30:
        return 1

    # 모든 조건을 통과하면 추가 학습 필요도가 낮다고 판단합니다.
    return 0
def update_ai_labels():

    # SQLite 데이터베이스에 연결합니다.
    conn = sqlite3.connect(DB_PATH)

    # 데이터베이스 커서를 생성합니다.
    cursor = conn.cursor()

    # 모든 학습 기록을 가져옵니다.
    cursor.execute("SELECT * FROM study_records")

    # 모든 데이터를 가져옵니다.
    rows = cursor.fetchall()

    # 현재 테이블의 컬럼 정보를 가져옵니다.
    cursor.execute("PRAGMA table_info(study_records)")

    # 컬럼 정보를 가져옵니다.
    columns = cursor.fetchall()

    # 컬럼 이름만 추출합니다.
    column_names = [column[1] for column in columns]

    # 각 학습 기록을 하나씩 처리합니다.
    for row in rows:

        # 각 컬럼의 위치를 찾습니다.
        row_data = dict(zip(column_names, row))

        # 국어 학습 필요 여부를 계산합니다.
        korean_need = calculate_study_need(
            row_data["korean_score"],
            row_data["korean_wrong_rate"],
            row_data["korean_study_time"]
        )

        # 수학 학습 필요 여부를 계산합니다.
        math_need = calculate_study_need(
            row_data["math_score"],
            row_data["math_wrong_rate"],
            row_data["math_study_time"]
        )

        # 영어 학습 필요 여부를 계산합니다.
        english_need = calculate_study_need(
            row_data["english_score"],
            row_data["english_wrong_rate"],
            row_data["english_study_time"]
        )

        # 과학 학습 필요 여부를 계산합니다.
        science_need = calculate_study_need(
            row_data["science_score"],
            row_data["science_wrong_rate"],
            row_data["science_study_time"]
        )

        # 현재 학습 기록의 ID를 가져옵니다.
        record_id = row_data["id"]

        # 계산한 AI 정답 데이터를 데이터베이스에 저장합니다.
        cursor.execute(
            """
            UPDATE study_records
            SET
                korean_need = ?,
                math_need = ?,
                english_need = ?,
                science_need = ?
            WHERE id = ?
            """,
            (
                korean_need,
                math_need,
                english_need,
                science_need,
                record_id
            )
        )

    # 변경사항을 저장합니다.
    conn.commit()

    # 데이터베이스 연결을 종료합니다.
    conn.close()

# 데이터베이스 테이블이 존재하는지 확인하기 위해 테이블을 생성합니다.
create_table()

# AI 학습에 사용할 데이터에 비어 있는 정답값이 있는지 확인하고 수정하는 함수입니다.
def fix_ai_labels():

    # SQLite 데이터베이스에 연결합니다.
    conn = sqlite3.connect(DB_PATH)

    # 데이터베이스 커서를 생성합니다.
    cursor = conn.cursor()

    # 국어 학습 필요 여부가 비어 있는 데이터를 다시 계산합니다.
    cursor.execute("""
        UPDATE study_records
        SET korean_need =
            CASE
                WHEN korean_score < 70
                     OR korean_wrong_rate > 30
                     OR korean_study_time < 30
                THEN 1
                ELSE 0
            END
        WHERE korean_need IS NULL
    """)

    # 수학 학습 필요 여부가 비어 있는 데이터를 다시 계산합니다.
    cursor.execute("""
        UPDATE study_records
        SET math_need =
            CASE
                WHEN math_score < 70
                     OR math_wrong_rate > 30
                     OR math_study_time < 30
                THEN 1
                ELSE 0
            END
        WHERE math_need IS NULL
    """)

    # 영어 학습 필요 여부가 비어 있는 데이터를 다시 계산합니다.
    cursor.execute("""
        UPDATE study_records
        SET english_need =
            CASE
                WHEN english_score < 70
                     OR english_wrong_rate > 30
                     OR english_study_time < 30
                THEN 1
                ELSE 0
            END
        WHERE english_need IS NULL
    """)

    # 과학 학습 필요 여부가 비어 있는 데이터를 다시 계산합니다.
    cursor.execute("""
        UPDATE study_records
        SET science_need =
            CASE
                WHEN science_score < 70
                     OR science_wrong_rate > 30
                     OR science_study_time < 30
                THEN 1
                ELSE 0
            END
        WHERE science_need IS NULL
    """)

    # 변경된 내용을 저장합니다.
    conn.commit()

    # 데이터베이스 연결을 종료합니다.
    conn.close()

# SQLite 데이터베이스 기능을 가져옵니다.
import sqlite3

# 사용자 테이블을 생성하는 함수입니다.
def create_users_table():

    # 기존 프로젝트에서 사용하는 데이터베이스에 연결합니다.
    connection = get_connection()

    # 데이터베이스 명령을 실행할 커서를 만듭니다.
    cursor = connection.cursor()

    # 사용자 정보를 저장할 테이블을 생성합니다.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 변경 사항을 데이터베이스에 저장합니다.
    connection.commit()

    # 데이터베이스 연결을 종료합니다.
    connection.close()

# 비밀번호 해시 기능을 가져옵니다.
from werkzeug.security import generate_password_hash


# 회원가입 정보를 데이터베이스에 저장하는 함수입니다.
def register_user(username, password):

    # 아이디 앞뒤의 공백을 제거합니다.
    username = username.strip()

    # 아이디가 비어 있는지 확인합니다.
    if not username:
        return False, "아이디를 입력해주세요."

    # 비밀번호가 비어 있는지 확인합니다.
    if not password:
        return False, "비밀번호를 입력해주세요."

    # 비밀번호는 최소 8자 이상으로 제한합니다.
    if len(password) < 8:
        return False, "비밀번호는 8자 이상이어야 합니다."

    # 비밀번호를 안전한 해시 문자열로 변환합니다.
    password_hash = generate_password_hash(password)

    # 데이터베이스에 연결합니다.
    connection = get_connection()

    try:
        # SQL 명령을 실행할 커서를 생성합니다.
        cursor = connection.cursor()

        # 사용자 정보를 저장합니다.
        cursor.execute(
            """
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
            """,
            (username, password_hash)
        )

        # 데이터베이스에 저장 사항을 반영합니다.
        connection.commit()

        # 회원가입 성공을 반환합니다.
        return True, "회원가입이 완료되었습니다."

    # 아이디 중복 등 데이터베이스 제약 조건 오류를 처리합니다.
    except sqlite3.IntegrityError:

        # 중복 아이디 안내를 반환합니다.
        return False, "이미 사용 중인 아이디입니다."

    # 데이터베이스 연결을 항상 종료합니다.
    finally:
        connection.close()

# 저장된 비밀번호 해시를 검증하는 기능을 가져옵니다.
from werkzeug.security import check_password_hash


# 아이디와 비밀번호로 사용자를 확인하는 함수입니다.
def verify_user(username, password):

    # 아이디 앞뒤의 공백을 제거합니다.
    username = username.strip()

    # 데이터베이스에 연결합니다.
    connection = get_connection()

    try:
        # SQL 명령을 실행할 커서를 생성합니다.
        cursor = connection.cursor()

        # 입력한 아이디와 일치하는 사용자만 조회합니다.
        cursor.execute(
            "SELECT id, username, password_hash FROM users WHERE username = ?",
            (username,)
        )

        # 조회된 사용자 정보를 가져옵니다.
        user = cursor.fetchone()

        # 아이디가 없으면 로그인 실패를 반환합니다.
        if user is None:
            return None

        # 입력한 비밀번호가 저장된 해시와 일치하는지 확인합니다.
        if not check_password_hash(user["password_hash"], password):
            return None

        # 로그인에 성공하면 사용자 ID와 아이디를 반환합니다.
        return {
            "id": user["id"],
            "username": user["username"]
        }

    # 사용자가 로그인 정보를 확인할 수 없을 때 연결을 종료합니다.
    finally:
        connection.close()

