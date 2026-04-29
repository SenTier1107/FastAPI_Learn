# FastAPI 라이브러리에서 FastAPI 클래스를 임포트
from fastapi import FastAPI

# FastAPI 인스턴스 생성
# app은 API의 모든 기능을 담당하는 핵심 객체
app = FastAPI()


# 경로 처리 데코레이터
# @app.get("/") : 루트 경로("/")에 GET 요청이 오면 아래 함수를 실행
@app.get("/")
async def root():
    # dict 형태로 반환하면 FastAPI가 자동으로 JSON으로 변환
    return {"message": "Hello my name is J.LEE"}


# 경로 매개변수 예시
# /items/1 처럼 URL에 값을 포함시킬 수 있음
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


# 여러 HTTP 메소드 예시
# POST: 데이터 생성
@app.post("/items/")
async def create_item():
    return {"message": "아이템이 생성되었습니다"}

# PUT: 데이터 수정
@app.put("/items/{item_id}")
async def update_item(item_id: int):
    return {"message": f"{item_id}번 아이템이 수정되었습니다"}

# DELETE: 데이터 삭제
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    return {"message": f"{item_id}번 아이템이 삭제되었습니다"}


# async def vs def
# async def: 비동기 함수 (I/O 작업이 많을 때 효율적)
# def: 일반 동기 함수
@app.get("/sync-example")
def sync_example():
    return {"message": "이건 일반 동기 함수입니다"}


# 자동 문서화
# /docs     -> Swagger UI (대화형 API 문서)
# /redoc    -> ReDoc (대안 API 문서)
# /openapi.json -> OpenAPI 스키마 (JSON 형식)