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
    return [{'role': role, 'content': content}]


def openai_ask(
        messages: typing.List,model_name ='gpt-4', history: typing.List = [],
        temperature: float = 0.01, retry=100,
        custom_header: typing.Union[dict, None] = None,
):

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
        total=1,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
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