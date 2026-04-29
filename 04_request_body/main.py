from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


# Pydantic BaseModel을 상속받아 데이터 모델 선언
# 기본값이 없는 필드(name, price)는 필수, 기본값이 None인 필드는 선택적
class Item(BaseModel):
    name: str                       # 필수
    description: str | None = None  # 선택적
    price: float                    # 필수
    tax: float | None = None        # 선택적


# 기본 요청 본문
# POST 요청으로 JSON 데이터를 받아서 반환
@app.post("/items/")
async def create_item(item: Item):
    return item


# 모델 어트리뷰트 직접 접근
# item.tax, item.price 처럼 모델의 각 필드에 직접 접근 가능
@app.post("/items/detail/")
async def create_item_detail(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# 요청 본문 + 경로 매개변수
# FastAPI가 item_id는 경로 매개변수, item은 요청 본문으로 자동 인식
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}


# 요청 본문 + 경로 매개변수 + 쿼리 매개변수
# 세 가지를 동시에 선언해도 FastAPI가 각각을 자동으로 구분
# - item_id: 경로 매개변수 (경로에 선언되어 있으므로)
# - item: 요청 본문 (Pydantic 모델이므로)
# - q: 쿼리 매개변수 (단순 타입이고 경로에 없으므로)
@app.put("/items/{item_id}/query")
async def update_item_with_query(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result