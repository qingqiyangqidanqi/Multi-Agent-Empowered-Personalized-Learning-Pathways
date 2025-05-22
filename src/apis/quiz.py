#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@PROJECT_NAME: Multi-Agent-Empowered-Personalized-Learning-Pathways
@File    : quiz.py
@Author  : jiesheng
@Date    : 2025/5/18 15:31
@Desc    : 
           包括三个部分：1. 用户发送请求获得问题。Question 2. 用户回答问题，服务器判断对错返回结果。Answer 3. 用户答完所有题目，服务器返回最终结果。Result
@Modify History:
         
@Copyright：Copyright(c) 2025-2028. All Rights Reserved
=================================================="""
from fastapi import APIRouter, HTTPException, Request, Header, Body
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import logging

from src.modules.quiz.quiz import get_question, judeg_correct, get_result
from utils import *

question_router = APIRouter(
    prefix="/quiz/question",
    tags=["计算机自适应测试-返回问题"],
    responses={404: {"description": "Not found"}}
)

answer_router = APIRouter(
    prefix="/quiz/answer",
    tags=["计算机自适应测试-返回结果"],
    responses={404: {"description": "Not found"}}
)


# ===========================================1. 用户发送请求获得问题。===========================================
class QuestionRequest(BaseModel):
    student_id: str
    session_id: str = None


async def question(
        request: Request,
        logger: logging.Logger,
        input_data: QuestionRequest = Body(...),
        requestId: str = Header(None, alias="requestId")
):
    try:
        # 请求入参日志留存
        headers = request.headers
        logger.info("Request ID: {}, 请求头信息如下：\n{}\n".format(requestId, headers))
        logger.info("Request ID: {}, 请求Body信息：\n{}\n".format(requestId, input_data))

        # 如果session_id不存在，则生成一个新会话并返回第一个问题，否则返回下一个问题
        session_id = input_data.session_id
        student_id = input_data.student_id
        if session_id is None:
            session_id = student_id + "_01"

        # 获取问题
        question_num, next_question,next_question_full = get_question(session_id)  # 之前做过的题目数量，下一道题
        if next_question is not None:
            logger.info(f"quiz会话在继续, session_id: {session_id}, 第{question_num}题: {next_question}")
            # 将题目记录在talks_quiz中
            append_messages_to_talks_quiz(session_id,student_id, question_num, next_question_full)
        else:
            logger.error("Request ID: %s, 无法获取题目，请检查问题", requestId or "unknown")
        return (session_id, question_num, next_question)
    except Exception as e:
        logger.error(f"session_id: {session_id}, 会话失败: {str(e)}")
        import traceback
        logger.error("详细错误: %s", traceback.format_exc())


# =========================2. 用户回答问题，服务器判断对错返回结果;用户答完所有题目，服务器返回最终结果。===================================

class AnswerRequest(BaseModel):
    session_id: str
    student_answer: str


async def answer(
        request: Request,
        logger: logging.Logger,
        input_data: AnswerRequest = Body(...),
        requestId: str = Header(None, alias="requestId")
):
    """提交答案并获取下一个问题"""
    try:
        # 记录请求信息
        logger.info("Request ID: %s, 提交答案请求, session_id: %s, answer: %s",
                    requestId or "unknown", input_data.session_id, input_data.answer)

        session_id = input_data.session_id
        student_answer = input_data.student_answer

        # 检查会话是否存在talks_quiz中
        if session_id:
            logger.warning("Request ID: %s, 会话不存在: %s", requestId or "unknown", session_id)
            raise HTTPException(status_code=404, detail="会话不存在，请重新开始测验")

        # 验证和处理答案
        is_correct, is_end = judeg_correct(session_id, student_answer)
        if not is_end:
            # 如果不是最后一道题
            logger.info(f"session_id: {session_id}, 回答是{is_correct}")
            return tuple(session_id, is_correct)
        else:
            # 如果是最后一道题
            final_level, final_bloom = get_result(session_id)
            logger.info(f"session_id: {session_id}, 回答是{is_correct}")
            logger.info(f"session_id: {session_id}, 测试结束, 最终水平: {final_level},bloom等级: {final_bloom}")
            return tuple(session_id, is_correct, final_level, final_bloom)
    except HTTPException:
        # 直接重新抛出HTTP异常
        raise
    except Exception as e:
        logger.error("Request ID: %s, 处理答案时发生错误: %s", requestId or "unknown", str(e))
        import traceback
        logger.error("详细错误: %s", traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"处理答案时发生错误: {str(e)}")
