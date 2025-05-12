# 启动api服务

# 智能体模拟学生

# 学生智能体进行计算机自适应测试

# 智能体模拟教师

# 教师智能体对学生智能体进行学习路径规划import requests

import json
import requests
from utils import *
from configs.my_prompt import teacher_prompt

# API请求相关的配置
BASE_URL = "http://localhost:10007"
PLPP_SAVE_PATH = "data/learning_path_planning.csv"
HEADERS = {
    "appId": "yxcptj_ydy",
    "requestId": "80088208820",
    "requestTime": "2021-03-16 23:15:00"
}


def check_service_available():
    """检查API服务是否可用"""
    try:
        # 尝试发送一个简单请求来检查服务是否启动
        http_body = {"student_message": "test"}
        response = requests.post(url=BASE_URL + "/health", json=http_body, headers=HEADERS)
        return response.status_code == 200
    except:
        print("警告: API服务似乎未启动，请确保服务在运行")
        return False


def convert_student_data(student_data: Dict[str, str]) -> str:
    """
    将英文格式的学生完整数据转换为中文格式字符串作为学生重要的信息

    Args:
        student_data: 包含学生信息的英文格式字典

    Returns:
        str: 格式化的中文JSON字符串
    """
    # 创建新的中文格式字典
    chinese_format = {
        "考试分数": student_data.get("Exam_Score (%)", ""),
        "最终成绩": student_data.get("Final_Grade", ""),
        "学习风格": student_data.get("Preferred_Learning_Style", ""),
        "完成课程数": student_data.get("Online_Courses_Completed", ""),
        "每周学习时长": student_data.get("Study_Hours_per_Week", ""),
        "作业完成率": student_data.get("Assignment_Completion_Rate (%)", ""),
        "压力水平": student_data.get("Self_Reported_Stress_Level", ""),
        "睡眠时长": student_data.get("Sleep_Hours_per_Night", ""),
        "花费在社交媒体上的时间": f"{student_data.get('Time_Spent_on_Social_Media (hours/week)', '')}小时/周",
        "出勤率": f"{student_data.get('Attendance_Rate (%)', '')}%"
    }

    # 格式化为指定的字符串形式
    formatted_string = "{\n"
    for key, value in chinese_format.items():
        formatted_string += f'"{key}": "{value}",\n'

    # 去掉最后一个逗号并添加结束括号
    formatted_string = formatted_string.rstrip(',\n') + "\n}"

    return formatted_string


def simulate_student(student_message):
    """智能体模拟学生"""
    print("智能体模拟学生...")
    # # 发送请求获取题目
    # try:
    #     response = requests.post(
    #         f'{BASE_URL}/Cat',
    #         json={"student_message": "请求题目"},
    #         headers=HEADERS
    #     )
    #     print(f"学生智能体请求题目: {response.text}")
    #     return response.json()
    # except Exception as e:
    #     print(f"请求失败: {e}")
    #     return None
    return student_message


def adaptive_testing(input) -> tuple[str, str]:
    """学生智能体进行计算机自适应测试"""
    print("学生智能体进行计算机自适应测试...")
    # 模拟一系列自适应测试问题
    test_questions = ["A", "B", "C", "D"]
    results = []

    for question in test_questions:
        try:
            response = requests.post(
                f'{BASE_URL}/Cat',
                json={"student_message": question},
                headers=HEADERS
            )
            results.append(response.json())
            print(f"问题 '{question}' 的回答: {response.text}")
        except Exception as e:
            print(f"测试问题 {question} 请求失败: {e}")

    print(f"测试完成，结果数: {len(results)}")
    return results[0], results[1]  # 返回考试分数，bloom测试水平级别


def generate_learning_plan(student_message):
    """教师智能体对学生智能体进行学习路径规划"""

    print("智能体模拟教师...")

    try:
        response = requests.post(
            f'{BASE_URL}/Teacher',
            json={"student_message": student_message},
            headers=HEADERS
        )
        teacher_response = response.json()
        print("教师智能体已响应,正在生成学习路径规划...")

    except Exception as e:
        print(f"教师智能体响应失败: {e}")
        return None

    # 处理各种可能的返回格式
    if teacher_response:
        # 处理响应是字符串的情况（可能是Markdown格式的JSON）
        if isinstance(teacher_response, str):
            # 如果是Markdown代码块格式，移除```json和```标记
            if teacher_response.startswith("```json"):
                json_start = teacher_response.find("\n") + 1
                json_end = teacher_response.rfind("```")
                if json_end > json_start:
                    json_str = teacher_response[json_start:json_end].strip()
                    try:
                        plan = json.loads(json_str)
                        print("学习路径规划已生成:")
                        return json.dumps(plan, ensure_ascii=False, indent=2)
                    except json.JSONDecodeError:
                        print("无法解析返回的JSON字符串")
                        return teacher_response
            # 可能是普通JSON字符串
            try:
                plan = json.loads(teacher_response)
                return json.dumps(plan, ensure_ascii=False, indent=2)
            except json.JSONDecodeError:
                # 如果不是有效JSON，直接返回原字符串
                return teacher_response

        # 如果响应是字典
        elif isinstance(teacher_response, dict):
            if "当前水平评估" in teacher_response:
                plan = teacher_response
            else:
                plan = teacher_response.get("learning_path", teacher_response)

            print("学习路径规划已生成:")
            return json.dumps(plan, ensure_ascii=False, indent=2)

        # 其他类型响应，直接转换为字符串
        else:
            return str(teacher_response)
    else:
        print("无法生成学习路径规划，教师响应为空")
        return False


def main():
    """主函数"""
    print("程序开始运行...", "\n")

    # 检查服务是否可用
    if not check_service_available():
        print("服务未启动，尝试继续执行...", "\n")
    else:
        print("服务已启动，继续执行...", "\n")
        print(
            "*********************************************************************************************************************************************",
            "\n")

    # 准备教师的设定信息
    teacher_message = teacher_prompt
    print("教师的信息:", teacher_message, "\n")
    print(
        "*********************************************************************************************************************************************",
        "\n")

    # 准备学生信息迭代器
    (log_params, server_params, llm_params, select_server, student) = return_config()
    student_data_generator = read_data_from_csv(order=student["START_NUMBER"],
                                                file_path='data/student_performance_large_dataset.csv')

    for item in range(student["START_NUMBER"], student["END_NUMBER"] + 1):

        # 准备学生的设定信息
        student_data = next(student_data_generator)
        student_message = convert_student_data(student_data)
        # print(f"第{item}个学生的信息:", student_message, "\n")
        print(
            "*********************************************************************************************************************************************",
            "\n")

        # 智能体模拟学生
        student_agent = simulate_student(student_message)
        print("学生智能体模拟结果:", student_agent, "\n")
        print(
            "*********************************************************************************************************************************************",
            "\n")

        # 学生智能体进行计算机自适应测试
        # exam_score, student_level = adaptive_testing(student_agent)
        exam_score, student_level = student_data.get("Exam_Score (%)", ""), student_data.get("Final_Grade", "")  # test：先写死，之后CAT程序出来了再改
        print(f"计算机自适应测试已完成，测试分数是{exam_score}分，bloom级别是{student_level}<UNK>", "\n")
        print(
            "*********************************************************************************************************************************************",
            "\n")

        # 教师智能体对学生智能体进行学习路径规划
        plpp_result = generate_learning_plan(student_message)
        print(f"教师智能体学习路径规划已完成，结果是\n{plpp_result}", "\n")
        print(
            "*********************************************************************************************************************************************",
            "\n")

        # 如果成功生成了学习路径，将其保存到CSV
        if plpp_result:
            try:
                # 将JSON字符串转换为字典
                plan_dict = json.loads(plpp_result)
                # 保存到CSV，使用item作为学生编号
                save_learning_path_to_csv(student_id=item, learning_path=plan_dict, file_path=PLPP_SAVE_PATH)
                print(f"已将学生{item}的学习路径保存到CSV文件")
            except json.JSONDecodeError:
                print(f"无法将学习路径结果转换为JSON: {plpp_result}")
        print(
            "*********************************************************************************************************************************************",
            "\n")

        print(f"第{item}个学生的PLPP推荐程序执行完毕", "\n")
        print(
            "*********************************************************************************************************************************************",
            "\n")


if __name__ == "__main__":
    # 记得先启动API服务,再进行测试
    main()
