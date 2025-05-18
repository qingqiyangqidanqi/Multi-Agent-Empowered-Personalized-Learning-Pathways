#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@PROJECT_NAME: Multi-Agent-Empowered-Personalized-Learning-Pathways
@File    : teacher.py
@Author  : jiesheng
@Date    : 2025/5/18 11:50
@Desc    : 

@Modify History:
         
@Copyright：Copyright(c) 2025-2028. All Rights Reserved
=================================================="""
from .base import PromptTemplateBase
from config.prompt import teacher_prompt
from utils import *


class TeacherPrompt(PromptTemplateBase):
    """
    教师智能体进行plpp提示词生成
    """

    def __init__(
            self,
            student_id: str,
    ):
        self.student_id = student_id
        student_data = self._get_student_data()
        self.age = student_data.get("Age"),
        self.gender = student_data.get("Gender"),
        self.study_hours_per_week = student_data.get("Study_Hours_per_Week"),
        self.preferred_learning_style = student_data.get("Preferred_Learning_Style"),
        self.online_courses_completed = student_data.get("Online_Courses_Completed"),
        self.participation_in_discussions = student_data.get("Participation_in_Discussions"),
        self.assignment_completion_rate = student_data.get("Assignment_Completion_Rate (%)"),
        self.exam_score = student_data.get("Exam_Score (%)"),
        self.attendance_rate = student_data.get("Attendance_Rate (%)"),
        self.use_of_educational_tech = student_data.get("Use_of_Educational_Tech"),
        self.self_reported_stress_level = student_data.get("Self_Reported_Stress_Level"),
        self.time_spent_on_social_media = student_data.get("Time_Spent_on_Social_Media (hours/week)"),
        self.sleep_hours_per_night = student_data.get("Sleep_Hours_per_Night"),
        self.final_grade = student_data.get("Final_Grade"),

    def _get_student_data(self):
        """
        通过学号获取学生数据
        """
        student_data = read_csv_row(id=self.student_id, file_path='./data/student_performance_large_dataset.csv')
        return student_data

    def create_prompt(self) -> str:
        prompt_init = teacher_prompt
        prompt = prompt_init.format(
            student_id=self.student_id,
            age=self.age[0],
            gender=self.gender[0],
            study_hours_per_week=self.study_hours_per_week[0],
            preferred_learning_style=self.preferred_learning_style[0],
            online_courses_completed=self.online_courses_completed[0],
            participation_in_discussions=self.participation_in_discussions[0],
            assignment_completion_rate=self.assignment_completion_rate[0],
            exam_score=self.exam_score[0],
            final_grade=self.final_grade[0],
            attendance_rate=self.attendance_rate[0],
            use_of_educational_tech=self.use_of_educational_tech[0],
            self_reported_stress_level=self.self_reported_stress_level[0],
            time_spent_on_social_media=self.time_spent_on_social_media[0],
            sleep_hours_per_night=self.sleep_hours_per_night[0]
        )
        return prompt


if __name__ == '__main__':
    student_id = "S00003"
    teacher = TeacherPrompt(student_id)
    prompt = teacher.create_prompt()
    print(prompt)
