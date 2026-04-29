# 01. First Steps

## 실행 방법
```bash
uvicorn main:app --reload
```

## 주요 개념

### FastAPI 인스턴스
- `from fastapi import FastAPI`로 FastAPI 클래스를 임포트
- `app = FastAPI()`로 인스턴스 생성
- app 객체가 API의 모든 기능을 담당

### 경로(Path)
- URL에서 `/`부터 시작하는 뒷부분
- "엔드포인트" 또는 "라우트"라고도 불림
- 예시: `https://example.com/items/foo` → 경로는 `/items/foo`

### 작동(Operation) - HTTP 메소드
| 메소드 | 용도 |
|--------|------|
| GET | 데이터 읽기 |
| POST | 데이터 생성 |
| PUT | 데이터 수정 |
| DELETE | 데이터 삭제 |

### 데코레이터
- `@app.get("/")`처럼 함수 위에 붙여 경로와 메소드를 지정
- FastAPI에게 어떤 경로와 메소드에 해당하는 함수인지 알려줌

### async def vs def
- `async def`: 비동기 함수, I/O 작업이 많을 때 효율적
- `def`: 일반 동기 함수

## 자동 문서화
- `/docs` → Swagger UI (대화형 API 문서)
- `/redoc` → ReDoc (대안 API 문서)
- `/openapi.json` → OpenAPI 스키마 (JSON 형식)S