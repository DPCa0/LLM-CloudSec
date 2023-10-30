"""
Analyse inconsistent class labels for a dataset.
"""
import random
import re
import sys
from dq_analysis.datasets.data import Data
from ast import literal_eval
random.seed(42)

if len(sys.argv) < 2:
    print("Usage: python dq_analysis/attributes/consistency.py [prepare/measure] <dataset>")
    exit()


def clean_code(content):
    """ Remove comments and empty lines from source code. """
    content = content.encode("utf-8", "replace").decode("utf-8")
    # Remove multi-line comments
    pattern = r"^\s*/\*(.*?)\*/"
    content = re.sub(pattern, "", content, flags=re.DOTALL | re.MULTILINE)
    # Remove inline comments within /* and */
    pattern = r"/\*(.*?)\*/"
    content = re.sub(pattern, "", content)
    # Remove single-line comments
    pattern = r"\s*//.*"
    content = re.sub(pattern, "", content, flags=re.MULTILINE)
    # Remove empty lines
    pattern = r"^\s*[\r\n]"
    content = re.sub(pattern, "", content, flags=re.MULTILINE)

    return content


def get_exact_matches(dataset):
    """
    Return a list of all duplicate clusters in a dataset.
    Use type 1 duplicates: exact matching after removing comments and whitespace.
    """

    data = Data(dataset).get_dataset()
    data.Function = data.Function.astype(str).apply(clean_code)
    seen_funcs = []
    dup_clusters = []

    # Get all clusters
    for index, row in data.iterrows():
        if index % 1000 == 0:
            print(index)

        # Skip already parsed functions
        if row['Function'] in seen_funcs:
            continue

        # Check for duplicates
        dups = data[data['Function'] == row['Function']]
        if len(dups) > 1:
            dup_clusters.append(dups.UID.tolist())
            seen_funcs.extend(dups.UID.tolist())

    # Save
    with open(f'dq_analysis/datasets/{dataset}/consistent_clusters.csv', 'w') as f:
        f.write(str(dup_clusters))


def get_inconsistent_clusters(dataset, return_clusters=False):
    """
    Get cross-class exact duplicates.
    """

    data = Data(dataset).get_dataset()
    data = data.set_index('UID')

    # Read type-1 exact duplicate matching output
    duplicates = open(f'dq_analysis/datasets/{dataset}/consistent_clusters.csv', 'r')
    clusters = literal_eval(duplicates.read())

    # Get cross-class duplicate clusters
    cross_duplicates = []
    cross_clusters = []
    for x in clusters:
        # Get the class labels
        labels = [data.at[int(id), 'Vulnerable'] for id in x]
        # Skip consistent clusters
        if not (0 in labels and 1 in labels):
            continue
        cross_clusters.append(x)
        # Count non-vulnerable samples as duplicates
        for c, id in enumerate(x):
            if labels[c] == 0:
                cross_duplicates.append(int(id))
    if return_clusters:
        return cross_clusters
    else:
        return cross_duplicates


def get_consistent_dataset(dataset):
    """
    Remove duplicates from a dataset, and store for later use.
    """

    df = Data(dataset).get_dataset()
    # Get cross-class duplicates
    cross_duplicates = get_inconsistent_clusters(dataset)
    # Remove any cross-class duplicates
    df = df[~df.UID.isin(cross_duplicates)]
    df = df.dropna()

    return df


def count_inconsistent(dataset):
    """
    Get inconsistent labels within a dataset.
      i.e., duplicate entries that have different classes.
    Use Type-1 duplicate exact matching.
    """
    # Load the dataset
    df = Data(dataset).get_dataset()[['ID', 'UID', 'Vulnerable']]

    # Get cross-class duplicates
    cross_clusters = get_inconsistent_clusters(dataset, return_clusters=True)
    inconsistent = len([x for y in cross_clusters for x in y])

    print('-'*3 + dataset + '-'*3)
    print(f'Inconsistent Labels: {inconsistent} / {len(df)} ( {100* (inconsistent/len(df))} %)')
    print(f'Consistency value: {1 - inconsistent/len(df)}')


if __name__ == '__main__':
    if sys.argv[1] == 'prepare':
        get_exact_matches(sys.argv[2])
    elif sys.argv[1] == 'measure':
        count_inconsistent(sys.argv[2])
    else:
        print(f"ERROR: Unknown command line argument: \"{sys.argv[1]}\"")
