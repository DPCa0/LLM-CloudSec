import inspect
import json
from utils.ask import openai_ask
import config.configs as configs
import os

class AutoFunctionGenerator:
    """
    AutoFunctionGenerator 类用于自动生成一系列功能函数的 JSON Schema 描述。
    该类通过调用 OpenAI API，采用 Few-shot learning 的方式来生成这些描述。

    属性:
    - functions_list (list): 一个包含多个功能函数的列表。
    - max_attempts (int): 最大尝试次数，用于处理 API 调用失败的情况。
    
    方法:
    - __init__ : 初始化 AutoFunctionGenerator 类。
    - generate_function_descriptions : 自动生成功能函数的 JSON Schema 描述。
    - _call_openai_api : 调用 OpenAI API。
    - auto_generate : 自动生成功能函数的 JSON Schema 描述，并处理任何异常。
    """
    
    def __init__(self, functions_list, max_attempts=3):
        """
        初始化 AutoFunctionGenerator 类。

        参数:
        - functions_list (list): 一个包含多个功能函数的列表。
        - max_attempts (int): 最大尝试次数。
        """
        self.functions_list = functions_list
        self.max_attempts = max_attempts

    def store_cache(self,function_name, function_inspect, function_description):
        cache = {"name": function_name, "inspect": function_inspect, "description": function_description}
        with open(os.getcwd()+'/result/beta/function_json_cache/function_json_cache_1013.json', 'a') as f:
            f.write(json.dumps(cache,ensure_ascii=False) + '\n')

    def read_cache(self, function_name, function_inspect):
        #切换到工作目录
        with open(os.getcwd()+'/result/beta/function_json_cache/function_json_cache_1013.json', 'r') as f:
            for line in f.readlines():
                cache = json.loads(line)
                if cache["name"] == function_name and cache["inspect"] == function_inspect:
                    return json.loads(cache["description"])
        return None
    
    def generate_function_descriptions(self):
        """
        自动生成功能函数的 JSON Schema 描述。

        返回:
        - list: 包含 JSON Schema 描述的列表。
        """
         # 创建空列表，保存每个功能函数的JSON Schema描述
        functions = []
        
        for function in self.functions_list:
            
            # 读取指定函数的函数说明
            function_description = inspect.getdoc(function)
            cache = self.read_cache(function.__name__, function_description)
            if cache is not None:
                functions.append(cache)
                continue
            # 读取函数的函数名
            function_name = function.__name__
            
            # 定义system role的Few-shot提示
            system_Q = "你是一位优秀的数据分析师，现在有一个函数的详细声明如下："
            system_A = "计算年龄总和的函数，该函数从一个特定格式的JSON字符串中解析出DataFrame，然后计算所有人的年龄总和并以JSON格式返回结果。\
                        \n:param input_json: 必要参数，要求字符串类型，表示含有个体年龄数据的JSON格式字符串 \
                        \n:return: 计算完成后的所有人年龄总和，返回结果为JSON字符串类型对象"
            
            
            # 定义user role的Few-shot提示
            user_Q = "请根据这个函数声明，为我生成一个JSON Schema对象描述。这个描述应该清晰地标明函数的输入和输出规范。具体要求如下：\
                      1. 提取函数名称：'calculate_total_age_function'，并将其用作JSON Schema中的'name'字段  \
                      2. 在JSON Schema对象中，设置函数的参数类型为'object'.\
                      3. 'properties'字段如果有参数，必须表示出字段的描述. \
                      4. 从函数声明中解析出函数的描述，并在JSON Schema中以中文字符形式表示在'description'字段.\
                      5. 识别函数声明中哪些参数是必需的，然后在JSON Schema的'required'字段中列出这些参数. \
                      6. 输出的应仅为符合上述要求的JSON Schema对象内容,不需要任何上下文修饰语句. "

            user_A = "{'name': 'calculate_total_age_function', \
                               'description': '计算年龄总和的函数，从给定的JSON格式字符串（按'split'方向排列）中解析出DataFrame，计算所有人的年龄总和，并以JSON格式返回结果。 \
                               'parameters': {'type': 'object', \
                                              'properties': {'input_json': {'description': '执行计算年龄总和的数据集', 'type': 'string'}}, \
                                              'required': ['input_json']}}"
            
            
            # 定义输入

            system_message = "你是一位优秀的数据分析师，现在有一个函数的详细声明如下：%s" % function_description
            user_message = "请根据这个函数声明，为我生成一个JSON Schema对象描述。这个描述应该清晰地标明函数的输入和输出规范。具体要求如下：\
                            1. 提取函数名称：%s，并将其用作JSON Schema中的'name'字段  \
                            2. 在JSON Schema对象中，设置函数的参数类型为'object'.\
                            3. 'properties'字段如果有参数，必须表示出字段的描述. \
                            4. 从函数声明中解析出函数的描述，并在JSON Schema中以中文字符形式表示在'description'字段.\
                            5. 识别函数声明中哪些参数是必需的，然后在JSON Schema的'required'字段中列出这些参数. \
                            6. 输出的应仅为符合上述要求的JSON Schema对象内容,不需要任何上下文修饰语句. "  % function_name
            
            messages=[
                        {"role": "system", "content": "Q:" +  system_Q + system_A + user_Q + "A:" + user_A },

                        {"role": "user", "content": 'Q:' + system_message + user_message+ "A:"}
            ]
            response = openai_ask(messages)
            self.store_cache(function_name, function_description, response.replace("\'", '\"'))
            functions.append(json.loads(response.replace("\'", '\"')))
        return functions

    def auto_generate(self):
        """
        自动生成功能函数的 JSON Schema 描述，并处理任何异常。

        返回:
        - list: 包含 JSON Schema 描述的列表。

        异常:
        - 如果达到最大尝试次数，将抛出异常。
        """
        attempts = 0
        while attempts < self.max_attempts:
            try:
                functions = self.generate_function_descriptions()
                return functions
            except Exception as e:
                attempts += 1
                print(f"Error occurred: {e}")
                if attempts >= self.max_attempts:
                    print("Reached maximum number of attempts. Terminating.")
                    raise
                else:
                    print("Retrying...")