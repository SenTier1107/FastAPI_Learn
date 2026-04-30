# 02. Path Parameters

## 실행 방법
```bash
uvicorn main:app --reload
```

## 주요 개념

### 기본 경로 매개변수
- URL에서 `{item_id}` 처럼 중괄호로 감싸면 경로 매개변수가 됨
- URL에 입력한 값이 함수의 인자로 그대로 전달됨
- 예시: `/items/foo` → `{"item_id": "foo"}`

### 타입이 있는 경로 매개변수
- `item_id: int` 처럼 타입을 선언하면 FastAPI가 자동으로 타입 변환
- 예시: `/items/3` → `{"item_id": 3}` (문자열 "3"이 아닌 정수 3으로 변환)

### 데이터 검증
- 타입 선언을 하면 FastAPI가 자동으로 데이터 검증
- 예시: `/items/foo` (int 타입인데 문자열 입력) → 자동으로 오류 반환

### 순서 문제
- 고정 경로가 동적 경로보다 반드시 먼저 선언되어야 함
- `/users/me`가 `/users/{user_id}`보다 먼저 선언되어야 "me"가 user_id로 인식되지 않음

### Enum을 사용한 사전정의 값
- `str`과 `Enum`을 상속하는 클래스를 만들어 가능한 값을 미리 정의
- 정의되지 않은 값이 들어오면 자동으로 검증 오류 반환
- 예시: `/models/alexnet`, `/models/resnet`, `/models/lenet`만 허용

### 경로를 포함하는 경로 매개변수
- `:path`를 사용하면 슬래시(`/`)를 포함한 전체 경로를 매개변수로 받을 수 있음
- 예시: `/files/home/johndoe/myfile.txt`

## 테스트 방법
| URL | 결과 |
|-----|------|
| `/items/foo` | `{"item_id": "foo"}` |
| `/items/3` | `{"item_id": 3}` |
| `/items/foo` (int 타입) | 오류 반환 |
| `/users/me` | `{"user_id": "the current user"}` |
| `/users/123` | `{"user_id": "123"}` |
| `/models/alexnet` | `{"model_name": "alexnet", "message": "Deep Learning FTW!"}` |
| `/files/home/johndoe/myfile.txt` | `{"file_path": "home/johndoe/myfile.txt"}` |

## 자동 문서화
- `/docs` → Swagger UI에서 직접 테스트 가능

---

## 응용 실습 (advanced_path_parameters.py)

### 추가한 기능
- 가짜 DB(딕셔너리)를 활용한 실제 데이터 조회
- 존재하지 않는 데이터 요청 시 오류 메시지 반환
- 문자열 경로 매개변수로 상품 조회
- 카테고리 + 상품 ID 동시 조회

### 실행 방법
```bash
uvicorn advanced_path_parameters:app --reload
```

### 테스트
| URL | 결과 |
|-----|------|
| `/users/1` | Alice 정보 반환 |
| `/users/999` | 오류 메시지 반환 |
| `/products/apple` | Apple 상품 반환 |
| `/products/없는상품` | 오류 메시지 반환 |
| `/categories/fruit/products/1` | 카테고리 + 상품 ID 반환 |
