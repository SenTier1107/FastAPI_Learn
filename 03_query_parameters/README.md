# 03. Query Parameters

## 실행 방법
```bash
uvicorn main:app --reload
```

## 주요 개념

### 쿼리 매개변수란?
- URL에서 `?` 뒤에 오는 `키=값` 형태의 매개변수
- `&`으로 여러 개를 구분
- 예시: `/items/?skip=0&limit=10`

### 기본값이 있는 쿼리 매개변수
- 기본값을 선언하면 선택적 매개변수가 됨
- 예시: `skip=0`, `limit=10`은 기본값이므로 URL에 없어도 동작

### 선택적 쿼리 매개변수
- 기본값을 `None`으로 설정하면 선택적 매개변수가 됨
- 예시: `q: str | None = None`

### 쿼리 매개변수 형변환 (bool)
- `1`, `True`, `true`, `on`, `yes` → 모두 `True`로 변환
- 그 외 → `False`로 변환

### 여러 경로/쿼리 매개변수 동시 선언
- FastAPI가 이름으로 경로 매개변수와 쿼리 매개변수를 자동으로 구분
- 선언 순서 상관없음

### 필수 쿼리 매개변수
- 기본값을 선언하지 않으면 필수 매개변수가 됨
- 필수 매개변수를 URL에 포함하지 않으면 오류 반환

## 테스트 방법
| URL | 결과 |
|-----|------|
| `/items/` | 전체 목록 (기본값 적용) |
| `/items/?skip=1&limit=2` | 1번째부터 2개 반환 |
| `/items/foo` | `{"item_id": "foo"}` |
| `/items/foo?q=test` | `{"item_id": "foo", "q": "test"}` |
| `/items/foo/short?short=true` | description 없음 |
| `/items/foo/short?short=false` | description 포함 |
| `/items/foo-item/required?needy=hello` | 정상 동작 |
| `/items/foo-item/required` | 오류 (needy 없음) |

## 자동 문서화
- `/docs` → Swagger UI에서 직접 테스트 가능