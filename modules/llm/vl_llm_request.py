from utils import *
from configs.my_prompt import *
from openai import OpenAI

def openai_chat(system_prompt, user_prompt):

    (log_params, server_params, llm_params, select_server, student, cat) = return_config()
    def anal_openai_chat(llm_output: str):
        result = None
        try:
            parsed_data = json.loads(llm_output)
            return parsed_data["choices"][0]["message"]["content"]
        except json.JSONDecodeError as e:
            print("JSON解析失败:", e)
            return result

    try:
        client = OpenAI(
            api_key=llm_params["API_KEY"],
            base_url=llm_params["BASE_URL"],
        )
        completion = client.chat.completions.create(
            model=llm_params["MODEL_NAME"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}]
        )
        response = completion.model_dump_json()
        return anal_openai_chat(response)
    except Exception as e:
        print("request llm Exception:{}".format(e))
        return None


if __name__ == '__main__':
    result = openai_chat(teacher_prompt, input_teacher_prompt)
    print(result)
