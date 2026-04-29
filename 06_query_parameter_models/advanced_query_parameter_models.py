from typing import Annotated, Literal
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

fake_products_db = [
    {"name": "Laptop", "category": "electronics", "price": 1200000, "created_at": "2024-01-01"},
    {"name": "Phone", "category": "electronics", "price": 800000, "created_at": "2024-02-01"},
    {"name": "Desk", "category": "furniture", "price": 300000, "created_at": "2024-01-15"},
    {"name": "Chair", "category": "furniture", "price": 150000, "created_at": "2024-03-01"},
    {"name": "Monitor", "category": "electronics", "price": 500000, "created_at": "2024-02-15"},
]


# 상품 필터링 모델
class ProductFilter(BaseModel):
    limit: int = Field(10, gt=0, le=50)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "price", "name"] = "created_at"
    category: str | None = None
    min_price: int | None = Field(None, ge=0)
    max_price: int | None = Field(None, ge=0)


@app.get("/products/")
async def get_products(filter_query: Annotated[ProductFilter, Query()]):
    results = fake_products_db

    # 카테고리 필터
    if filter_query.category:
        results = [p for p in results if p["category"] == filter_query.category]

    # 가격 필터
    if filter_query.min_price is not None:
        results = [p for p in results if p["price"] >= filter_query.min_price]
    if filter_query.max_price is not None:
        results = [p for p in results if p["price"] <= filter_query.max_price]

    # 정렬
    results = sorted(results, key=lambda x: x[filter_query.order_by])

    # 페이지네이션
    results = results[filter_query.offset: filter_query.offset + filter_query.limit]

    return {"total": len(results), "products": results}