#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@PROJECT_NAME: Multi-Agent-Empowered-Personalized-Learning-Pathways
@File    : quiz.py
@Author  : jiesheng
@Date    : 2025/5/18 22:42
@Desc    : 

@Modify History:
         
@Copyright：Copyright(c) 2025-2028. All Rights Reserved
=================================================="""


def get_question(session_id: str, student_id: str) -> str:
    """
    通过会话id获取问题
    """
    question = ""
    return question


def judeg_correct(session_id: str, student_answer: str) -> str:
    """
    获取问题的答案，和是否是最后一道题
    """
    correct = True
    is_end = False
    return correct,is_end



def get_result(question: str) -> str:
    """
    获取最终的结果
    """
    final_level:int = 1
    final_bloom:str = "A"
    return final_level,final_bloom
