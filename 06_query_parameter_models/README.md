# 06. Query Parameter Models

## 실행 방법
```bash
uvicorn main:app --reload
```

## 주요 개념

### 쿼리 매개변수 모델이란?
- 연관된 쿼리 매개변수를 Pydantic 모델로 묶어서 관리
- 여러 곳에서 모델을 재사용 가능
- 검증 및 메타데이터를 한 번에 선언 가능
- FastAPI 0.115.0 버전부터 지원

### Field() 검증 옵션
| 옵션 | 설명 |
|------|------|
| `gt` | 초과 (greater than) |
| `ge` | 이상 (greater than or equal) |
| `lt` | 미만 (less than) |
| `le` | 이하 (less than or equal) |

### Literal 타입
- 특정 값만 허용할 때 사용
- 예시: `Literal["created_at", "updated_at"]` → 두 값 중 하나만 허용

### 추가 쿼리 매개변수 금지
- `model_config = {"extra": "forbid"}` 설정으로 선언되지 않은 쿼리 매개변수 차단
- 선언되지 않은 매개변수가 들어오면 오류 반환

## 5번과의 차이점
| 챕터 | 방식 |
|------|------|
| 05 String Validations | 매개변수 하나씩 개별로 검증 선언 |
| 06 Query Parameter Models | 여러 매개변수를 Pydantic 모델로 묶어서 한번에 관리 |

## 테스트 방법
| URL | 결과 |
|-----|------|
| `/items/` | 기본값으로 반환 |
| `/items/?limit=10&offset=5` | 정상 |
| `/items/?limit=0` | 오류 (gt=0 조건 위반) |
| `/items/?limit=101` | 오류 (le=100 조건 위반) |
| `/items/?order_by=name` | 오류 (Literal 조건 위반) |
| `/strict-items/?limit=10` | 정상 |
| `/strict-items/?limit=10&tool=plumbus` | 오류 (선언되지 않은 필드) |

## 자동 문서화
- `/docs` → 쿼리 매개변수 모델의 각 필드 확인 가능

---

## 🔥 응용 실습 (advanced_param_models.py)

### 추가한 기능
- 상품 필터링 모델 (ProductFilter) 구현
- 카테고리, 가격 범위 필터링
- 정렬 기능 (created_at, price, name)
- 페이지네이션 (limit, offset)

### 실행 방법
```bash
uvicorn advanced_param_models:app --reload
```

### 테스트
| URL | 결과 |
|-----|------|
| `/products/` | 전체 상품 반환 |
| `/products/?category=electronics` | 전자제품만 필터링 |
| `/products/?min_price=500000` | 50만원 이상 필터링 |
| `/products/?order_by=price` | 가격순 정렬 |
| `/products/?limit=2&offset=1` | 2개씩 페이지네이션 |