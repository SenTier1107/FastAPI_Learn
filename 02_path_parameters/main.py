from enum import Enum
from fastapi import FastAPI

app = FastAPI()


# 기본 경로 매개변수
# URL에서 {item_id} 부분이 함수의 item_id 인자로 전달됨
@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}


# 타입이 있는 경로 매개변수
# item_id: int로 선언하면 FastAPI가 자동으로 타입 변환 및 검증
@app.get("/items/typed/{item_id}")
async def read_item_typed(item_id: int):
    return {"item_id": item_id}


# 순서 문제 - 고정 경로가 동적 경로보다 먼저 선언되어야 함
# /users/me가 /users/{user_id}보다 먼저 선언되어야 "me"가 user_id로 인식되지 않음
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


# Enum을 사용한 사전정의 값
# 가능한 값을 미리 정의하여 잘못된 값이 들어오면 자동으로 검증
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}


# 경로를 포함하는 경로 매개변수
# :path를 사용하면 슬래시(/)를 포함한 전체 경로를 매개변수로 받을 수 있음
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}