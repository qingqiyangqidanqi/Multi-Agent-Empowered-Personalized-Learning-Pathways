#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@PROJECT_NAME: Multi-Agent-Empowered-Personalized-Learning-Pathways
@File    : factory.py
@Author  : jiesheng
@Date    : 2025/5/18 11:40
@Desc    : 

@Modify History:
         
@Copyright：Copyright(c) 2025-2028. All Rights Reserved
=================================================="""
from .student import StudentPrompt
from .teacher import TeacherPrompt

# 提示词工厂类
class PromptTemplateFactory:
    @staticmethod
    def create_template(template_name, student_id):
        # 历史相似工单SQL生产提示词工厂
        if template_name == "student_prompt":
            return StudentPrompt(student_id=student_id)
        elif template_name == "teacher_prompt":
            return TeacherPrompt(student_id=student_id)
        else:
            raise ValueError(f"Unknown template type: {template_name}")