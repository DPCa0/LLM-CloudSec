import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, recall_score, f1_score, confusion_matrix

# 1. Load and preprocess data
with open("test.json", "r") as file:
    data = json.load(file)

predicted_values = []
true_values = []
for key, value in data.items():
    # Extract the first numerical value from the predicted field
    try:
        predicted_num = int(value['predicted'].split(',')[0])
    except ValueError:
        # If not a number, assign a special value (-1)
        predicted_num = -1
    predicted_values.append(predicted_num)

    # Extract the numerical value from the CWE field
    true_num = int(value['CWE'].split('CWE')[1])
    true_values.append(true_num)

# 2. Calculate the metrics
accuracy = accuracy_score(true_values, predicted_values)
recall = recall_score(true_values, predicted_values, average='macro', zero_division=0)
f1 = f1_score(true_values, predicted_values, average='macro', zero_division=0)
conf_matrix = confusion_matrix(true_values, predicted_values)

# 3. Visualize the results
# Plotting Accuracy, Recall, and F1 Score
plt.figure(figsize=(10, 6))
metrics = [accuracy, recall, f1]
metric_names = ['Accuracy', 'Recall', 'F1 Score']
plt.bar(metric_names, metrics)
plt.ylim(0, 1)
for i, v in enumerate(metrics):
    plt.text(i, v + 0.01, f"{v:.2f}", ha='center', va='bottom', fontsize=10)
plt.title('Evaluation Metrics')
plt.show()

# Plotting the Confusion Matrix
plt.figure(figsize=(10, 10))
plt.imshow(conf_matrix, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Confusion Matrix')
plt.colorbar()
tick_marks = np.arange(len(set(true_values)))
plt.xticks(tick_marks, rotation=45)
plt.yticks(tick_marks)
plt.tight_layout()
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.show()
