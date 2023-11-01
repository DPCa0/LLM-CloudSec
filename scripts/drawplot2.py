import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, recall_score, f1_score, confusion_matrix

# 1. Load and preprocess data
with open("predicted.json", "r") as file:
    data = json.load(file)

for value in data:
    value["CWE"] = int(value['CWE'].split('CWE')[1])


