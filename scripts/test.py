from utils.ask import *
from model.prompt import *
from model.code import *


def judge(query, temperature: float = 0.01):
    system_prompt = make_msg('system', judgement_prompt)
    message = make_msg('user', query)
    content = openai_ask(message, model_name='gpt-4', history=system_prompt, temperature=temperature)
    print(f"判断结果：{content}")
    return content


def classify(query, temperature: float = 0.01):
    system_prompt = make_msg('system', classify_prompt)
    message = make_msg('user', query)
    content = openai_ask(message, model_name='gpt-4', history=system_prompt, temperature=temperature)
    print(f"分类结果：{content}")
    return content


def run(code_snippet, temperature: float = 0.01):
    judge_result = judge(code_snippet)
    if judge_result == 'True':
        classify_result = classify(code_snippet)
        print(f"最终结果：{classify_result}")


# run(snippet_1)
run(snippet_2)
# run(snippet_3)
