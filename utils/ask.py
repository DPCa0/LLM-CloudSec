import config.configs as configs
import typing


from urllib3 import Retry
import sseclient
from requests.adapters import HTTPAdapter
import requests
import time
import json

openai_header = {'Content-Type': 'application/json',
                 "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, "
                               "like Gecko) Chrome/114.0.0.0 Safari/537.36"}
if openai_key := configs.config.get("openai_key"):
    openai_header["Authorization"] = f"Bearer {openai_key}"


def make_msg(role: str, content: str):
    """
    生成gpt消息
    :param role: str 消息角色 user/system
    :param content: str 消息内容
    """
    return [{'role': role, 'content': content}]


def openai_ask(
        messages: typing.List,model_name ='gpt-4', history: typing.List = [],
        temperature: float = 0.01, retry=100,
        custom_header: typing.Union[dict, None] = None,
):
    """
    使用session对openai进行问答，返回content(翻译成中文)
    :param messages: 提问序列
    :param temperature: temperature参数
    :param retry: 重试次数
    :param show: 是否打印log
    :return: content
    """
    api = configs.config.get("openai_host")
    model = configs.config.get("models", {}).get(model_name, model_name)
    if not isinstance(history, list):
        history = []
    params_gpt = {
        "model": model,
        "messages": history + messages,
        'temperature': temperature,
        "presence_penalty": 0,
        "stream": True,
    }
    retry_strategy = Retry(
        total=1,  # 最大重试次数（包括首次请求）
        backoff_factor=1,  # 重试之间的等待时间因子
        status_forcelist=[429, 500, 502, 503, 504],  # 需要重试的状态码列表
        allowed_methods=["POST"]  # 只对POST请求进行重试
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    # 创建会话并添加重试逻辑
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    for i in range(retry):
        try:
            headersq = openai_header.copy()
            if custom_header:
                headersq.update(custom_header)
            response = session.post(
                api, headers=headersq,
                proxies=configs.config.get("proxies", None), data=json.dumps(params_gpt),
                stream=True
            )
            sse = sseclient.SSEClient(response)
            result = ""
            for msg in sse.events():
                if msg.data != '[DONE]':
                    dd = json.loads(msg.data)['choices'][0]['delta'].get('content', '')
                    result+=dd
            break
        except Exception as e:
            import traceback
            traceback.print_exc()
            time.sleep(2)
            continue
    return result