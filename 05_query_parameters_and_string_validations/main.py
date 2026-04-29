import random
from typing import Annotated
from fastapi import FastAPI, Query
from pydantic import AfterValidator

app = FastAPI()


# 기본 쿼리 매개변수 (검증 없음)
@app.get("/items/basic")
async def read_items_basic(q: str | None = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# max_length 검증
# q가 50자를 초과하면 자동으로 오류 반환
@app.get("/items/max-length")
async def read_items_max_length(
    q: Annotated[str | None, Query(max_length=50)] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# min_length + max_length 검증
# q가 3자 미만이거나 50자 초과하면 오류 반환
@app.get("/items/min-max-length")
async def read_items_min_max_length(
    q: Annotated[str | None, Query(min_length=3, max_length=50)] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 정규식 검증
# q가 정확히 "fixedquery" 문자열이어야 함
@app.get("/items/pattern")
async def read_items_pattern(
    q: Annotated[
        str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 기본값 설정
# q를 입력하지 않으면 기본값 "fixedquery" 사용
@app.get("/items/default")
async def read_items_default(
    q: Annotated[str, Query(min_length=3)] = "fixedquery",
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 필수 쿼리 매개변수
# 기본값 없이 선언하면 필수 매개변수가 됨
@app.get("/items/required")
async def read_items_required(
    q: Annotated[str, Query(min_length=3)],
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 쿼리 매개변수 리스트
# URL: /items/list?q=foo&q=bar → q = ["foo", "bar"]
@app.get("/items/list")
async def read_items_list(
    q: Annotated[list[str] | None, Query()] = None,
):
    query_items = {"q": q}
    return query_items


# 메타데이터 추가 (title, description)
# /docs에서 매개변수 설명이 표시됨
@app.get("/items/metadata")
async def read_items_metadata(
    q: Annotated[
        str | None,
        Query(
            title="Query string",
            description="Query string for the items to search in the database",
            min_length=3,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 별칭(alias) 사용
# URL에서 item-query로 전달하지만 함수에서는 q로 사용
# item-query는 파이썬 변수명으로 사용 불가하기 때문에 alias 사용
@app.get("/items/alias")
async def read_items_alias(
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 사용 중단(deprecated) 매개변수
# 문서에서 deprecated로 표시됨
@app.get("/items/deprecated")
async def read_items_deprecated(
    q: Annotated[
        str | None,
        Query(
            alias="item-query",
            title="Query string",
            description="Query string for the items to search in the database",
            min_length=3,
            max_length=50,
            pattern="^fixedquery$",
            deprecated=True,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# OpenAPI 스키마에서 매개변수 숨기기
# include_in_schema=False로 설정하면 /docs에서 보이지 않음
@app.get("/items/hidden")
async def read_items_hidden(
    hidden_query: Annotated[str | None, Query(include_in_schema=False)] = None,
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    return {"hidden_query": "Not found"}


# 커스텀 검증 (AfterValidator)
# id가 "isbn-" 또는 "imdb-"로 시작하는지 검증
data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}


def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id


@app.get("/items/custom-validation")
async def read_items_custom_validation(
    id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {"id": id, "name": item}