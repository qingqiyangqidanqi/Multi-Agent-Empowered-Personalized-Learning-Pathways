import requests
import sys
import json
from configs.my_prompt import *

header = {"appId": "yxcptj_ydy", "requestId": "80088208820",
          "requestTime": "2021-03-16 23:15:00"}

url = 'http://localhost:10007/Cat'  # 测试


def check_health(input):
    # 不加统一接口
    http_body = {"student_message": input}

    try:
        exception = 0
        response = requests.post(url, json=http_body, headers=header)
        print(response.text)

        if response.status_code == 200:

            res = '11'


        else:
            exception = 1


    except Exception as e:
        exception = 1
        print(e)
    if exception == 1:
        sys.exit(1)
    return exception


# 示例用法
if __name__ == "__main__":
    input = (check_health("请求题目"))
    result = check_health("A")

