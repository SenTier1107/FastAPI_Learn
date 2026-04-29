from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 가짜 DB
fake_db: dict = {}
next_id = 1


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    in_stock: bool = True


# 상품 생성
@app.post("/items/")
async def create_item(item: Item):
    global next_id
    item_dict = item.model_dump()
    item_dict["id"] = next_id

    if item.tax is not None:
        item_dict["price_with_tax"] = item.price + item.tax

    fake_db[next_id] = item_dict
    next_id += 1
    return item_dict


# 상품 전체 조회
@app.get("/items/")
async def get_items():
    return {"items": list(fake_db.values())}


# 상품 단건 조회
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id not in fake_db:
        return {"error": f"{item_id}번 상품을 찾을 수 없습니다"}
    return fake_db[item_id]


# 상품 수정
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if item_id not in fake_db:
        return {"error": f"{item_id}번 상품을 찾을 수 없습니다"}
    item_dict = item.model_dump()
    item_dict["id"] = item_id
    fake_db[item_id] = item_dict
    return item_dict


# 상품 삭제
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in fake_db:
        return {"error": f"{item_id}번 상품을 찾을 수 없습니다"}
    deleted = fake_db.pop(item_id)
    return {"message": f"{item_id}번 상품이 삭제되었습니다", "deleted_item": deleted}