from typing import (
    Dict,
    List
)
from logging import Logger

import uvicorn
from fastapi import FastAPI, Depends, Request, Header, Body
from fastapi.routing import APIRoute
from pydantic import BaseModel

from src.apis.teacher import TeacherInput, router as teacher_router, teacher
from src.apis.student import StudentInput, router as student_router, student
from src.apis.quiz import QuestionRequest, AnswerRequest, answer_router, question_router, question, answer
from src.apis import server_response
from utils import return_config, service_run_name
from log import make_log
import os

app = FastAPI()

# 确保 data 文件夹存在
os.makedirs("data", exist_ok=True)


# 创建依赖项
async def get_logger():
    return logger


def health():
    return server_response(data="health")


# 1. ===========================学生智能体对话===========================
async def student_wrapper(
        request: Request,
        log: Logger = Depends(get_logger),
        input_data: StudentInput = Body(...),
        requestId: str = Header(None, alias="requestId")
):
    return await student(request, log, input_data, requestId)


# 2. ===========================教师智能体个性化学习路径推荐==================
async def teacher_wrapper(
        request: Request,
        log: Logger = Depends(get_logger),
        input_data: TeacherInput = Body(...),
        requestId: str = Header(None, alias="requestId")
):
    return await teacher(request, log, input_data, requestId)


# 3. ===========================计算机自适应测试==========================
async def question_wrapper(
        request: Request,
        log: Logger = Depends(get_logger),
        input_data: QuestionRequest = Body(...),
        requestId: str = Header(None, alias="requestId")
):
    return await question(request, log, input_data, requestId)


async def answer_wrapper(
        request: Request,
        log: Logger = Depends(get_logger),
        input_data: AnswerRequest = Body(...),
        requestId: str = Header(None, alias="requestId")
):
    return await answer(request, log, input_data, requestId)


# 加载配置
(log_params, server_params, llm_params, select_server, student_1, cat) = return_config()

# 当前需要启动的服务区分
service_name = service_run_name()

logger = make_log(log_params)
logger.info("%s", "成功加载日志配置!\n")

# 按照配置的service_name启动对应的服务
if service_name == "student":
    # 设置需要转发的路由
    app.post("/health", description="健康检查")(health)
    student_router.post("", description="学生智能体进行交流")(student_wrapper)
    app.include_router(student_router)

elif service_name == "teacher":
    # 设置需要转发的路由
    app.post("/health", description="健康检查")(health)
    teacher_router.post("", description="教师agent")(teacher_wrapper)
    app.include_router(teacher_router)

elif service_name == "quiz":
    # 设置需要转发的路由
    app.post("/health", description="健康检查")(health)
    question_router.post("", description="计算机自适应测试-返回问题")(question_wrapper)
    answer_router.post("", description="计算机自适应测试-返回结果")(answer_wrapper)
    app.include_router(question_router)
    app.include_router(answer_router)

else:
    app.post("/health", description="健康检查")(health)
    student_router.post("", description="学生智能体进行交流")(student_wrapper)
    teacher_router.post("", description="教师智能体进行个性化学习路径推荐")(teacher_wrapper)
    question_router.post("", description="计算机自适应测试-问题")(question_wrapper)
    answer_router.post("", description="计算机自适应测试-结果")(answer_wrapper)

    app.include_router(student_router)
    app.include_router(teacher_router)
    app.include_router(question_router)
    app.include_router(answer_router)

# 打印所有注册的路由
for route in app.routes:
    if isinstance(route, APIRoute):
        logger.info("Route path: {}, name: {}, description: {}".format(route.path, route.name, route.description))
