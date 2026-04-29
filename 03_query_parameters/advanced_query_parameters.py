from fastapi import FastAPI

app = FastAPI()

fake_items_db = [
    {"name": "Apple", "category": "fruit", "price": 1000},
    {"name": "Banana", "category": "fruit", "price": 500},
    {"name": "Carrot", "category": "vegetable", "price": 800},
    {"name": "Daikon", "category": "vegetable", "price": 600},
    {"name": "Eggplant", "category": "vegetable", "price": 1200},
]


# 카테고리 필터링 + 페이지네이션
@app.get("/items/")
async def get_items(
    category: str | None = None,
    skip: int = 0,
    limit: int = 10,
    min_price: int | None = None,
    max_price: int | None = None,
):
    results = fake_items_db

    # 카테고리 필터
    if category:
        results = [item for item in results if item["category"] == category]

    # 가격 필터
    if min_price is not None:
        results = [item for item in results if item["price"] >= min_price]
    if max_price is not None:
        results = [item for item in results if item["price"] <= max_price]

    return {"total": len(results), "items": results[skip: skip + limit]}


# 검색 기능
@app.get("/items/search/")
async def search_items(q: str):
    results = [item for item in fake_items_db if q.lower() in item["name"].lower()]
    return {"query": q, "results": results}