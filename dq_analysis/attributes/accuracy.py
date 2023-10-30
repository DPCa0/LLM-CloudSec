"""
Analyse the label correctness of the datasets.
"""
import sys
import pandas as pd

if len(sys.argv) < 2:
    print("Usage: python dq_analysis/attributes/accuracy.py [prepare/measure] <dataset>")
    exit()


def report_accuracy(dataset):
    """
    Report the measured accuracy for the selected datasets,
        based on the manual samples.
    """
    sample = pd.read_csv(f"dq_analysis/datasets/{dataset}/sample.csv", encoding='ISO 8859-1')
    correct = len(sample[sample.Label == 1])
    print(f'{dataset} Accuracy: {correct/len(sample)}')


if __name__ == '__main__':
    if sys.argv[1] == 'prepare':
        print('No accuracy preparation.')
        exit()
    elif sys.argv[1] == 'measure':
        report_accuracy(sys.argv[2])
    else:
        print(f"ERROR: Unknown command line argument: \"{sys.argv[1]}\"")
