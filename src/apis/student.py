#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@PROJECT_NAME: Multi-Agent-Empowered-Personalized-Learning-Pathways
@File    : student.py
@Author  : jiesheng
@Date    : 2025/5/18 01:06
@Desc    :
            智能体扮演学生进行多轮对话接口
@Modify History:

@Copyright：Copyright(c) 2025-2028. All Rights Reserved
=================================================="""
from typing import (
    Any
)
from fastapi import APIRouter, Body, Header, Request
from pydantic import BaseModel
import logging
import requests

from src.modules.prompt import PromptTemplateFactory
from src.modules.llm.request_llm import openai_chat
from utils import *

from .response import (
    params_error_response,
    server_error_response,
    child_server_error_response
)

router = APIRouter(
    prefix="/student",
    tags=["智能体扮演学生"],
    responses={404: {"description": "Not found"}},
)


class StudentInput(BaseModel):
    student_id: str  # 学生的id
    talk: str = None  # 向学生智能体提出的问题


async def student(
        request: Request,
        logger: logging.Logger,
        input_data: StudentInput = Body(...),
        requestId: str = Header(None, alias="requestId")
) -> Any:
    try:
        # ==============================================================================================================================================
        # 1. 请求入参日志留存
        headers = request.headers
        logger.info("Request ID: {}, 请求头信息如下：\n{}\n".format(requestId, headers))
        logger.info("Request ID: {}, 请求Body信息：\n{}\n".format(requestId, input_data))

        if not input_data or not input_data.student_id:
            return params_error_response(data=f"No input provided in the request body")

        # ==============================================================================================================================================
        # 2. 组装提示词
        message = []
        is_exist = read_csv_student_data(id=input_data.student_id, file_path='./data/talks_student.csv')
        try:
            # 如果talks_student.csv中不存在学生的会话，则创建一个新的提示词
            if input_data.talk == "" or not is_exist:
                student_prompt = PromptTemplateFactory.create_template(template_name="student_prompt",
                                                                       student_id=input_data.student_id)
                prompt = student_prompt.create_prompt()
                message.append({"role": "system", "content": prompt})
            # 如果talks_student.csv中存在学生的会话，则将新会话内容增加进去
            else:
                system_promt = json.loads(read_csv_student_data(id=input_data.student_id, file_path='./data/talks_student.csv').get("contents"))
                for item in system_promt:
                    message.append(item)
                message.append({"role": "user", "content": input_data.talk})
            logger.info("Request ID: {}, 组装提示词：\n提示词：{}".format(requestId, message))
        except Exception as e:
            logger.error("Request ID: {}, 提示词组装失败！".format(requestId))
            return server_error_response(data="组装提示词失败\nError:" + str(e))

        # ==============================================================================================================================================
        # 3. 请求大模型
        try:
            response_data = openai_chat(message)
            logger.info(f"大模型输出中...\n {str(response_data)}")

            try:
                result = response_data
                message.append({"role": "assistant", "content": result})
                append_messages_to_talks_student(student_ID=input_data.student_id, new_messages=message[-2:])

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
