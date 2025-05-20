from utils import *
from config.prompt import *
from openai import OpenAI
import os


def openai_chat(message: list[dict[str, str]]) -> str:
    """
    调用OpenAI的聊天模型
    :param message: 消息列表，包含角色和内容
    :return: 模型的响应解析后的结果
    """
    (log_params, server_params, llm_params, select_server, student, quiz) = return_config()

    def anal_openai_chat(llm_output: str):
        """
        解析OpenAI的聊天模型输出
        :param llm_output: OpenAI聊天模型的输出
        :return: 解析后的内容
        """
        result = None
        try:
            parsed_data = json.loads(llm_output)
            return parsed_data["choices"][0]["message"]["content"]
        except json.JSONDecodeError as e:
            print("JSON解析失败:", e)
            return result

    try:
        client = OpenAI(
            api_key=os.environ.get(f"""{llm_params["API_KEY_NAME"]}"""),
            base_url=llm_params["BASE_URL"],
        )
        completion = client.chat.completions.create(
            model=llm_params["MODEL_NAME"],
            messages=message
        )
        response = completion.model_dump_json()
        return anal_openai_chat(response)
    except Exception as e:
        print("request llm Exception:{}".format(e))
        return None


if __name__ == '__main__':
    (log_params, server_params, llm_params, select_server, student, quiz) = return_config()
    print(llm_params["API_KEY_NAME"])
    print(os.environ.get(f"""{llm_params["API_KEY_NAME"]}"""))
    message = [
        {"role":"system","content": "你只会回复：我不好"},
        {"role": "user", "content": "hello"}
               ]
    result = openai_chat(message)
    print(result)
