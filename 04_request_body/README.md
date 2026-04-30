# 04. Request Body

## 실행 방법
```bash
uvicorn main:app --reload
```

## 주요 개념

### 요청 본문(Request Body)이란?
- 클라이언트에서 API로 보내는 데이터
- 주로 POST, PUT, DELETE, PATCH 요청에 사용
- GET 요청에는 본문을 담지 않는 것이 권장됨

### Pydantic BaseModel
- `BaseModel`을 상속받아 데이터 모델을 선언
- 기본값이 없는 필드 → 필수
- 기본값이 `None`인 필드 → 선택적
- 자동으로 타입 변환 및 데이터 검증 수행

### 매개변수 자동 인식 규칙
FastAPI는 함수 매개변수를 아래 규칙으로 자동 구분함
- 경로에 선언된 매개변수 → 경로 매개변수
- `int`, `float`, `str`, `bool` 등 단순 타입 → 쿼리 매개변수
- Pydantic 모델 타입 → 요청 본문

### 모델 어트리뷰트 접근
- `item.name`, `item.price` 처럼 모델의 각 필드에 직접 접근 가능
- `item.model_dump()` 로 dict 형태로 변환 가능

## 1,2,3번과의 차이점
| 챕터 | 방식 | 예시 |
|------|------|------|
| 02 Path Parameters | URL 경로에 값 포함 | `/items/3` |
| 03 Query Parameters | URL 뒤에 조건 추가 | `/items/?skip=0` |
| 04 Request Body | JSON 데이터를 본문에 담아 전송 | `{"name": "Foo", "price": 45.2}` |

## 테스트 방법
- `/docs` → POST `/items/` 에서 JSON 데이터 직접 입력해서 테스트
- 필수 필드(`name`, `price`) 없이 전송하면 오류 반환
- 선택 필드(`description`, `tax`) 없이 전송해도 정상 동작

## 자동 문서화
- `/docs` → Swagger UI에서 JSON 입력 폼 자동 생성

---

## 응용 실습 (advanced_request_body.py)

### 추가한 기능
- 가짜 DB를 활용한 실제 CRUD 구현
- 상품 생성 (POST)
- 상품 전체/단건 조회 (GET)
- 상품 수정 (PUT)
- 상품 삭제 (DELETE)

### 실행 방법
```bash
uvicorn advanced_request_body:app --reload
```

### 테스트
| 메소드 | URL | 설명 |
|--------|-----|------|
| POST | `/items/` | 상품 생성 |
| GET | `/items/` | 전체 상품 조회 |
| GET | `/items/1` | 1번 상품 조회 |
| PUT | `/items/1` | 1번 상품 수정 |
| DELETE | `/items/1` | 1번 상품 삭제 |
