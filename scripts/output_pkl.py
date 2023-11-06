import json
import pickle

try:
    with open("cache_D2A.pkl", "rb") as cache_file:
        current_data = pickle.load(cache_file)
        print(f"The length of the data is {len(current_data)}")
        # If the data is a dictionary, print its keys
        if isinstance(current_data, dict):
            print("Keys in the pickle data:")
            for key in current_data.keys():
                print(key)

        # If the data is a list of dictionaries, print the keys of the first dictionary
        elif isinstance(current_data, list) and len(current_data) > 0 and isinstance(current_data[0], dict):
            print("Keys in the first item of the pickle data list:")
            for key in current_data[0].keys():
                print(key)
                print(f"Code: {current_data[0]['code']} end")
                print(f"Prompt: {current_data[0]['prompt']} end")
                print(f"Predicted: {current_data[0]['predicted']} end")
                print(f"Predicted flaw code: {current_data[0]['predicted_flaw_code']} end")

        # If the data is of other type, just print its type
        else:
            print("The data is a:", type(current_data))
        # with open("test_D2A_cache.json", "w") as file:
        #     file.write(json.dumps(current_data))
except FileNotFoundError:
    print("Cache file not found.")
