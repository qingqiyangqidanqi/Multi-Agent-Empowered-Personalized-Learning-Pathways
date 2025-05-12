from typing import (
    Dict,
    List
)
from logging import Logger

import uvicorn
from fastapi import FastAPI, Depends, Request, Header, Body
from fastapi.routing import APIRoute
from pydantic import BaseModel

from src.apis.Teacher import router as Teacher_Check_router, Teacher_Check
from src.apis import server_response
from utils import return_config
from log import make_log


app = FastAPI()

# 确保 data 文件夹存在
import os

os.makedirs("data", exist_ok=True)


# 创建依赖项
async def get_logger():
    return logger


async def get_select_server():
    return select_server


async def get_llm_params():
    return llm_params


def health():
    return server_response(data="health")


# /Teacher_Check
class Input(BaseModel):
    student_message: str


async def Teacher_Check_wrapper(
        request: Request,
        log: Logger = Depends(get_logger),
        input_data: Input = Body(...),
        requestId: str = Header(None, alias="requestId")
):
    return await Teacher_Check(request, log, input_data, requestId)


if __name__ == "__main__":
    # 加载配置
    (log_params, server_params, llm_params, select_server, student) = return_config()

    logger = make_log(log_params)
    logger.info("%s", "成功加载日志配置!\n")

    # 设置需要转发的路由
    app.post("/health", description="健康检查")(health)
    Teacher_Check_router.post("", description="助教")(Teacher_Check_wrapper)

    # 添加路由
    app.include_router(Teacher_Check_router)

    # 打印所有注册的路由
    for route in app.routes:
        if isinstance(route, APIRoute):
            logger.info("Route path: {}, name: {}, description: {}".format(route.path, route.name, route.description))

    # 启动服务
    uvicorn.run(app, host=server_params["IP"], port=server_params["PORT"], workers=server_params["WORKERS"])
