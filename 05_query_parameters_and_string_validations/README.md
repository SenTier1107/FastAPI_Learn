# 05. Query Parameters and String Validations

## 실행 방법
```bash
uvicorn main:app --reload
```

## 주요 개념

### Annotated와 Query
- `Annotated`를 사용해 매개변수에 추가 검증 및 메타데이터를 선언
- `Query()`를 `Annotated` 안에 넣어 쿼리 매개변수에 검증 적용

### 문자열 검증
| 옵션 | 설명 |
|------|------|
| `max_length` | 최대 길이 제한 |
| `min_length` | 최소 길이 제한 |
| `pattern` | 정규식 패턴 검증 |

### 메타데이터
- `title`: 매개변수 제목 (docs에 표시)
- `description`: 매개변수 설명 (docs에 표시)
- `deprecated=True`: 사용 중단 표시 (docs에 취소선으로 표시)
- `include_in_schema=False`: docs에서 매개변수 숨기기

### 별칭(alias)
- 파이썬 변수명으로 사용 불가능한 이름을 URL에서 사용할 때 활용
- 예시: URL에서 `item-query`로 전달 → 함수에서 `q`로 사용

### 쿼리 매개변수 리스트
- `list[str]` 타입으로 선언하면 여러 값을 한번에 받을 수 있음
- 예시: `/items/list?q=foo&q=bar` → `q = ["foo", "bar"]`

### 커스텀 검증 (AfterValidator)
- 기본 검증으로 불가능한 복잡한 검증이 필요할 때 사용
- `AfterValidator`에 검증 함수를 전달

## 테스트 방법
| URL | 결과 |
|-----|------|
| `/items/max-length?q=hello` | 정상 |
| `/items/max-length?q=51자이상문자열` | 오류 |
| `/items/min-max-length?q=hi` | 오류 (3자 미만) |
| `/items/pattern?q=fixedquery` | 정상 |
| `/items/pattern?q=other` | 오류 |
| `/items/list?q=foo&q=bar` | `{"q": ["foo", "bar"]}` |
| `/items/alias?item-query=hello` | 정상 |
| `/items/custom-validation?id=isbn-9781529046137` | 정상 |
| `/items/custom-validation?id=invalid-id` | 오류 |

## 자동 문서화
- `/docs` → 각 엔드포인트에서 검증 조건 확인 가능

---

## 🔥 응용 실습 (advanced_request_body.py)

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