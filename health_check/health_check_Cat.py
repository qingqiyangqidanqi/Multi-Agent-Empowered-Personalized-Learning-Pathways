import requests
import time

if __name__ == '__main__':
    base_url = "http://127.0.0.1:10007"

    try:
        # 启动测验
        start_response = requests.post(f"{base_url}/quiz/start")
        start_response.raise_for_status()  # 如果请求失败会抛出异常
        start_data = start_response.json()
        print("测验启动成功:")
        print(f"问题: {start_data['question']}")
        print(f"选项: {start_data['options']}")
        print(f"会话ID: {start_data['session_id']}")

        # 提交答案
        session_id = start_data["session_id"]
        answer_response = requests.post(
            f"{base_url}/quiz/answer",
            json={"answer": "A", "session_id": session_id}
        )
        answer_response.raise_for_status()
        answer_data = answer_response.json()
        print("\n提交答案结果:")
        print(f"答案正确: {answer_data['is_correct']}")
        print(f"正确答案: {answer_data['correct_answer']}")

        # 如果有下一题，显示下一题信息
        if not answer_data['is_completed'] and 'next_question' in answer_data:
            next_q = answer_data['next_question']
            print("\n下一题:")
            print(f"问题: {next_q['question']}")
            print(f"选项: {next_q['options']}")
        else:
            print("\n测验已完成")
            print(f"最终得分: {answer_data['score']}")
            print(f"Bloom分类等级: {answer_data['bloom_level']}")

    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
    except ValueError as e:
        print(f"JSON解析错误: {e}")
        print(f"服务器响应: {start_response.text}")