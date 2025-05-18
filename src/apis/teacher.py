# -- coding: utf-8 --

# 教师

from typing import (
    Any
)
from fastapi import APIRouter, Body, Header, Request
from pydantic import BaseModel
import logging
import requests

from src.modules.prompt import PromptTemplateFactory
from src.modules.llm.request_llm import openai_chat

from .response import (
    params_error_response,
    server_error_response,
    child_server_error_response
)

router = APIRouter(
    prefix="/teacher",
    tags=["教师agent对话接口"]
)


class TeacherInput(BaseModel):
    student_id: str


async def teacher(
        request: Request,
        logger: logging.Logger,
        input_data: TeacherInput = Body(...),
        requestId: str = Header(None, alias="requestId")
) -> Any:
    try:
        # 请求入参日志留存
        headers = request.headers
        logger.info("Request ID: {}, 请求头信息如下：\n{}\n".format(requestId, headers))
        logger.info("Request ID: {}, 请求Body信息：\n{}\n".format(requestId, input_data))

        # ==============================================================================================================================================
        if not input_data or not input_data.student_id:
            return params_error_response(data=f"No input provided in the request body")

        # ==============================================================================================================================================
        # 组装提示词

        try:
            teacher_prompt = PromptTemplateFactory.create_template(template_name="teacher_prompt",
                                                                   student_id=input_data.student_id)
            prompt = teacher_prompt.create_prompt()
            logger.info("Request ID: {}, 组装提示词：\n提示词：{}".format(requestId, prompt))
        except Exception as e:
            logger.error("Request ID: {}, 提示词组装失败！".format(requestId))
            return server_error_response(data="组装提示词失败\nError:" + str(e))

        # ==============================================================================================================================================
        # 请求大模型
        try:
            response_data = openai_chat(prompt)
            logger.info(f"大模型输出中...\n {str(response_data)}")

            try:
                result = response_data
                return result
            except Exception as e:
                print("解析失败:", e)
                return server_error_response(data=str(e))

        except requests.exceptions.Timeout:
            logger.error(f"Request ID: {requestId},访问大模型接口超时\n")
            return child_server_error_response(data="访问大模型接口超时!")

        except Exception as e:
            return child_server_error_response(data="大模型接口访问失败！\nError:" + str(e))


    except Exception as e:
        return params_error_response(data=str(e))
