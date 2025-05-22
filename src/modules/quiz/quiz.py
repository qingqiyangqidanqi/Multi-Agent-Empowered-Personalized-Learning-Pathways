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
from utils import *
import random
import csv


def get_question(session_id: str) -> Any:
    """
    通过会话id获取问题，最开始的难度设为中间值，之后会根据学生上一个做题情况进行调整;如果已完成所有题目，不推荐题目，返回None
    :param session_id: 会话id
    :return: 做题序号，问题     or     None
    """

    quiz_qa = []  # 记录学生做过的题目
    quiz_num = 0  # 统计做过题目的数量
    *_, quiz = return_config()
    difficulty = quiz['DIFFICULT']  # 当前题目的难度，初始题目难度为quiz['DIFFICULTY']
    total_question_number = quiz['TOTAL_QUESTION_NUMBER']  # 测试的题目总数量

    talk_quiz = read_csv_quiz_data(session_id=session_id, file_path='./data/talks_quiz.csv')
    # 如果有之前的做题记录
    if talk_quiz is not None:
        quiz_qa = eval(talk_quiz['QA'])
        quiz_num = len(quiz_qa)
        # 未完成所有题目，推荐下一道题
        if quiz_num < total_question_number:
            # 读取学生做过的上一道题，如果做对了，难度增加1级，否则降低
            for item in quiz_qa:
                if item['order'] == quiz_num:
                    if item['is_true'] == True:  # 上一道题做对了
                        difficulty = item['difficulty'] + 1
                    else:  # 上一道题做错了
                        difficulty = item['difficulty'] - 1
                    # 随机选择一道difficulty难度的题目
                    if difficulty <= 6:
                        full_next_question = get_random_question_by_difficulty(file_path='./data/quiz/questions_choice.csv',
                                                                          difficulty=difficulty)
                    else:
                        full_next_question = get_random_question_by_difficulty(file_path='./data/quiz/questions_choice.csv',
                                                                          difficulty=6)
        # 已完成所有题目，不推荐题目，返回None
        else:
            return None
    else:
        full_next_question = get_random_question_by_difficulty(file_path='./data/quiz/questions_choice.csv',
                                                          difficulty=difficulty)

    next_question = {
        # "knowledge_point_first": full_next_question[" knowledge_point_first"],
        # "knowledge_point_second": full_next_question[" knowledge_point_second"],
        # "knowledge_point_type": full_next_question["knowledge_point_type"],
        "question": full_next_question["question"],
        "option_A": full_next_question["option_A"],
        "option_B": full_next_question["option_B"],
        "option_C": full_next_question["option_C"],
        "option_D": full_next_question["option_D"],
        # "answer": full_next_question["answer"],
        # "difficulty": full_next_question["difficulty"],
        # "bloom_level": full_next_question["bloom_level"]
    }
    return quiz_num, next_question,full_next_question


def judeg_correct(session_id: str, student_answer: str) -> str:
    """
    获取问题的答案，和是否是最后一道题
    """
    correct = True
    is_end = False
    return correct, is_end


def get_result(question: str) -> str:
    """
    获取最终的结果
    """
    final_level: int = 1
    final_bloom: str = "A"
    return final_level, final_bloom


def get_random_question_by_difficulty(difficulty: int, file_path: str = './data/quiz/question_choice.csv') -> dict[
                                                                                                              str:str]:
    """
    从文件中随机获取指定难度的一道题目

    参数:
    file_path: 题库文件路径
    difficulty: 指定难度级别(整数)

    返回:
    一个包含题目完整信息的字典
    """
    matching_questions = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                # 确保行有足够的字段
                if len(row) >= 10:
                    try:
                        # 第10个字段(索引9)是难度
                        q_difficulty = int(row[9])
                        if q_difficulty == difficulty:
                            matching_questions.append(row)
                    except (ValueError, IndexError):
                        # 跳过难度非整数或格式不符的行
                        continue
    except Exception as e:
        print(f"读取文件出错: {e}")
        return None

    if not matching_questions:
        return None

    # 随机选择一道题目
    question = random.choice(matching_questions)

    # 转换为字典格式，方便使用
    question_dict = {
        " knowledge_point_first": question[0],
        " knowledge_point_second": question[1],
        "knowledge_point_type": question[2],
        "question": question[3],
        "option_A": question[4],
        "option_B": question[5],
        "option_C": question[6],
        "option_D": question[7],
        "answer": question[8],
        "difficulty": question[9],
        "bloom_level": question[10]
    }

    return question_dict


if __name__ == "__main__":
    session_id = "S00001_01"
    question_num, question_message = get_question(session_id=session_id)
    print(question_num)
    print(question_message)
