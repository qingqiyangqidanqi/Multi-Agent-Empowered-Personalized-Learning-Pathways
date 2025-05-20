
import requests
import sys
import json

from prompt_toolkit import output

header = {"appId": "yxcptj_ydy", "requestId": "80088208820",
          "requestTime": "2021-03-16 23:15:00"}

url = 'http://localhost:10007/productRec'#测试


# 解析openai流式输出内容
def analy_openai_stream(response) -> None:
    full_text = ""
    for line in response.iter_lines():
        if line:
            line_str = line.decode("utf-8")
            print(line_str)
            try:
                data = json.loads(line_str.split(":", 1)[1])
                if data["choices"][0]["finish_reason"] != "stop":
                    if "content" in data["choices"][0]["delta"]:
                        full_text += data["choices"][0]["delta"]["content"]
                else:
                    print("本次回答使用token数:", data["usage"]["completion_tokens"])
                    print("提问和回答总共使用token数:", data["usage"]["total_tokens"])
                    break
            except Exception as e:
                print(line_str)
    print("大模型完整回答：\n", full_text)


def check_health():

    # 不加统一接口
    http_body = {"Company_Id" : "57171401903","Product_Name" : ["中移舆情","E企组网","集团固话"]}

    try:
        exception = 0
        response = requests.post(url, json=http_body, headers=header)
        print(response.text)
        analy_openai_stream(response)

        if response.status_code==200:

            res='11'


        else:
            exception = 1


    except Exception as e:
        exception = 1
        print(e)
    if exception == 1:
        sys.exit(1)
    return exception


# if __name__ == '__main__':
#     # # print(check_health())
#     # # for item in [1,5]:
#     # #     print(item)
#     # coentents:list[dict[str,str]]
#     # # content:dict[str,str] = {input:"请给我第一个问题",output:"具体的一个question"}
#     # # content:dict[str,str] = {input:"我回答的结果是：A",output:"True/False"}
#     # content:dict[str,str] = {input:"整个quiz过程结果，请给我最终结果",output:"两个分数"}
# # # content:dict[str,str] = {input:"我回答的结果是：A",output:"True/False"}
