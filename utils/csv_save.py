import csv
import json
import os
from typing import Dict, Any, Optional


def save_learning_path_to_csv(student_id: int, learning_path: Dict[str, Any], file_path: str = '../data/student_learning_paths.csv') -> None:
            """
            将学习路径规划结果保存到CSV文件中

            Args:
                student_id: 学生编号
                learning_path: 包含学习路径规划的字典
                file_path: 要保存的CSV文件路径
            """
            # 检查是否为有效的学习路径数据
            if not isinstance(learning_path, dict):
                print("错误: 提供的学习路径不是有效的字典格式")
                return

            # 定义表头
            headers = ["学生编号", "当前水平评估", "定制方法", "调整深度", "结构化路径", "可行性建议", "最终目标"]

            # 检查文件是否已存在
            file_exists = os.path.isfile(file_path)

            try:
                with open(file_path, 'a', newline='', encoding='utf-8-sig') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=headers)

                    # 如果文件不存在，写入表头
                    if not file_exists:
                        writer.writeheader()

                    # 准备要写入的行数据
                    row = {"学生编号": student_id}  # 添加学生编号

                    # 添加其他字段
                    for header in headers[1:]:  # 跳过"学生编号"字段
                        if header in learning_path:
                            row[header] = json.dumps(learning_path[header], ensure_ascii=False)
                        else:
                            row[header] = ""

                    writer.writerow(row)
                    print(f"已成功将学习路径规划数据写入到 {file_path}")

            except Exception as e:
                print(f"写入CSV文件时出错: {e}")


if __name__ == "__main__":
    # 示例使用
    # 1. 从字符串解析JSON
    json_str = """
    {
      "当前水平评估": {
        "级别": "初学者",
        "结论": "您的基础概念掌握较弱，考试分数和最终成绩均处于初级阶段。建议从最基本的数据结构（如数组、链表）开始系统学习，加强算法逻辑训练和编程实践能力。"
      },
      "定制方法": {
        "学习风格": "动觉型",
        "结论": "通过编程实践和模拟实验深化理解，建议使用在线编程平台进行动手练习，结合实际问题提升编码能力。"
      },
      "调整深度": {
        "完成课程数": "11门",
        "定位": "进阶训练",
        "重点": [
          "强化基本数据结构的掌握（如栈、队列、线性表）。",
          "引入中等难度题目（如LeetCode、HackerRank）。",
          "分析常见错误及调试技巧（如边界条件处理、指针操作）。"
        ]
      },
      "结构化路径": {
        "每周学习时长": 47,
        "周计划": [
          {
            "周次": 1,
            "主题": "基础数据结构复习：数组与链表",
            "资源": "LeetCode简单题、B站算法入门视频",
            "时间分配": {
              "理论时间": 5,
              "实践时间": 8
            },
            "里程碑": "完成10道数组/链表题目，正确率≥75%"
          },
          {
            "周次": 2,
            "主题": "栈与队列的应用与实现",
            "资源": "GeeksforGeeks图文解析、手写模拟题",
            "时间分配": {
              "理论时间": 3,
              "实践时间": 9
            },
            "里程碑": "实现自定义栈与队列类，并通过测试用例"
          },
          {
            "周次": 3,
            "主题": "递归与分治策略入门",
            "资源": "Khan Academy递归讲解、CodinGame递归挑战",
            "时间分配": {
              "理论时间": 4,
              "实践时间": 10
            },
            "里程碑": "编写并调试至少3种递归函数（如斐波那契数列、二分查找）"
          },
          {
            "周次": 4,
            "主题": "排序与搜索算法初步",
            "资源": "MIT OpenCourseWare《Python编程与AI基础》、VisualGo演示",
            "时间分配": {
              "理论时间": 4,
              "实践时间": 12
            },
            "里程碑": "实现冒泡排序、插入排序、二分查找，并分析性能差异"
          }
        ]
      },
      "可行性建议": {
        "压力管理": "压力水平低 → 可适当增加每日学习强度；睡眠7小时 → 建议保持规律作息，避免熬夜刷题影响效率。",
        "时间优化": "社交媒体13小时/周 → 压缩至6小时以内，节省的时间用于每日30分钟LeetCode打卡。",
        "习惯改善": "出勤率79% → 建议设置固定学习闹钟提醒，并加入学习群组互相监督打卡进度。"
      },
      "最终目标": {
        "3个月后": "掌握五大基础数据结构（数组、链表、栈、队列、树）的基本实现与应用。",
        "6个月后": "能够独立完成小型项目（如简易计算器、通讯录管理系统），作业完成率提升至85%以上，达到中级水平。"
      }
    }
    """
    student_id = 1
    learning_path_data = json.loads(json_str)

    # 2. 将数据写入CSV
    save_learning_path_to_csv(student_id = student_id, learning_path=learning_path_data)