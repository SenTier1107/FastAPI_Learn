from fastapi import FastAPI

app = FastAPI()

# 가짜 데이터베이스 역할을 하는 리스트
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# 기본 쿼리 매개변수
# URL: /items/?skip=0&limit=10
# 경로 매개변수가 아닌 함수 매개변수는 자동으로 쿼리 매개변수로 해석됨
# skip, limit은 기본값이 있으므로 선택적 매개변수
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


# 선택적 쿼리 매개변수
# q는 기본값이 None이므로 선택적 매개변수
# URL: /items/foo 또는 /items/foo?q=검색어
@app.get("/items/{item_id}")
async def read_item_optional(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


# 쿼리 매개변수 형변환 (bool)
# short=1, short=True, short=true, short=on, short=yes 모두 True로 변환됨
# URL: /items/foo/short?q=test&short=true
@app.get("/items/{item_id}/short")
async def read_item_short(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item


# 여러 경로/쿼리 매개변수 동시 선언
# FastAPI가 이름으로 경로 매개변수와 쿼리 매개변수를 자동으로 구분
# URL: /users/1/items/foo?q=test&short=true
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item


# 필수 쿼리 매개변수
# 기본값이 없으면 필수 매개변수가 됨
# needy를 URL에 포함하지 않으면 오류 발생
# URL: /items/foo-item?needy=sooooneedy
@app.get("/items/{item_id}/required")
async def read_user_item_required(
    item_id: str, needy: str, skip: int = 0, limit: int | None = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item