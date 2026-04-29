from fastapi import FastAPI

app = FastAPI()

# 가짜 DB
fake_users_db = {
    1: {"name": "Alice", "age": 25, "job": "Developer"},
    2: {"name": "Bob", "age": 30, "job": "Designer"},
    3: {"name": "Charlie", "age": 28, "job": "Manager"},
}

fake_products_db = {
    "apple": {"name": "Apple", "price": 1000, "stock": 50},
    "banana": {"name": "Banana", "price": 500, "stock": 100},
    "cherry": {"name": "Cherry", "price": 3000, "stock": 20},
}


# 사용자 조회 - 없으면 오류 반환
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id not in fake_users_db:
        return {"error": f"{user_id}번 사용자를 찾을 수 없습니다"}
    return fake_users_db[user_id]


# 상품 조회 - 문자열 경로 매개변수
@app.get("/products/{product_name}")
async def get_product(product_name: str):
    if product_name not in fake_products_db:
        return {"error": f"{product_name} 상품을 찾을 수 없습니다"}
    return fake_products_db[product_name]


# 카테고리 + 상품 ID 동시 조회
@app.get("/categories/{category}/products/{product_id}")
async def get_product_by_category(category: str, product_id: int):
    return {"category": category, "product_id": product_id}