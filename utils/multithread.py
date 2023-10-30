import os.path
import time
import traceback

import pandas as pd
import json
from typing import Callable, Tuple, List
import concurrent.futures

from utils.logger import root_logger


def turbocharging(
        func: Callable, args: List[Tuple],
        workers: int,
        save_name="default", save_xlsx: bool = True, save_json: bool = True, desc: str = ""
):
    with concurrent.futures.ThreadPoolExecutor(workers) as executor:
        # futures = {: arg for arg in args}
        futures = {}
        i = 0
        for arg in args:
            futures[executor.submit(func, *arg)] = arg
            i += 1
            # if i <= workers:
            #     time.sleep(1)
        results = []
        # start_time = time.time()
        for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
            # arg = futures[future]
            try:
                res = future.result()
                cost = 0
                if isinstance(res, tuple) and len(res) == 2 and isinstance(res[1], (int, float)):
                    cost = res[1]
                    res = res[0]
                results.append(res)
                root_logger.notice(f'Task {desc} {i}/{len(args)}: -Done-, taking {cost:.2f} s')
            except Exception as e:
                root_logger.error(f'Task {i}/{len(args)}: -Skip-, because of {e}', backlevel=5)
                traceback.print_exc()
            if save_xlsx:
                output_df = pd.DataFrame(results)
                output_df.to_excel(save_name + "_cache.xlsx")
            if save_json:
                with open(save_name, 'w',
                          encoding='utf-8') as json_file:
                    json.dump(results, json_file, ensure_ascii=False, indent=2)
    return results
