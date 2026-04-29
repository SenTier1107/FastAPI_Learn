from typing import Annotated, Literal
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


# Pydantic 모델로 쿼리 매개변수 그룹 선언
# 여러 쿼리 매개변수를 하나의 모델로 묶어서 관리
# Field()로 각 필드에 검증 조건 추가
class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)   # 1~100 사이의 정수, 기본값 100
    offset: int = Field(0, ge=0)             # 0 이상의 정수, 기본값 0
    order_by: Literal["created_at", "updated_at"] = "created_at"  # 두 값 중 하나만 허용
    tags: list[str] = []                     # 문자열 리스트, 기본값 빈 리스트


# 기본 쿼리 매개변수 모델
# URL: /items/?limit=10&offset=0&order_by=created_at&tags=foo&tags=bar
@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query


# 추가 쿼리 매개변수 금지
# model_config = {"extra": "forbid"}로 선언되지 않은 쿼리 매개변수 차단
class StrictFilterParams(BaseModel):
    model_config = {"extra": "forbid"}  # 선언되지 않은 필드 금지

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


# URL에 선언되지 않은 쿼리 매개변수가 있으면 오류 반환
# 예: /strict-items/?limit=10&tool=plumbus → 오류 (tool은 선언되지 않은 필드)
@app.get("/strict-items/")
async def read_strict_items(filter_query: Annotated[StrictFilterParams, Query()]):
    return filter_query