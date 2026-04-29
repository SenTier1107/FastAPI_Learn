from typing import Annotated
from fastapi import FastAPI, Query

app = FastAPI()

fake_users_db = [
    {"username": "alice123", "email": "alice@example.com", "role": "admin"},
    {"username": "bob456", "email": "bob@example.com", "role": "user"},
    {"username": "charlie789", "email": "charlie@example.com", "role": "user"},
]


# 사용자 검색 - 길이 및 패턴 검증 적용
@app.get("/users/search/")
async def search_users(
    username: Annotated[
        str | None,
        Query(
            min_length=3,
            max_length=20,
            title="Username",
            description="검색할 사용자 이름 (3~20자)",
        ),
    ] = None,
    role: Annotated[
        str | None,
        Query(
            title="Role",
            description="필터링할 역할 (admin 또는 user)",
            pattern="^(admin|user)$",
        ),
    ] = None,
):
    results = fake_users_db

    if username:
        results = [u for u in results if username.lower() in u["username"].lower()]
    if role:
        results = [u for u in results if u["role"] == role]

    return {"total": len(results), "users": results}


# 태그 다중 검색
@app.get("/items/tags/")
async def get_items_by_tags(
    tags: Annotated[list[str] | None, Query()] = None,
):
    return {"searched_tags": tags}