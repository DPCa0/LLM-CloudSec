"""
Analyse the completeness of datasets.
Consider data values which have missing information, i.e., truncation.
"""
import sys
import re
import pandas as pd
from dq_analysis.datasets.data import Data

if len(sys.argv) < 2:
    print("Usage: python dq_analysis/attributes/completeness.py [prepare/measure] <dataset>")
    exit()


def syntax_completeness(dataset):
    """
    Analyze code snippets that don't have a complete syntax.
    Either truncated at the START or END of the function.
    Return a list of IDs that have been truncated and the type of truncation.
    """

    data = Data(dataset)
    df = data.get_dataset()
    df1 = data.get_metadata()
    df = df.merge(df1, on=['ID', 'UID', 'Vulnerable'], how='left')

    # Function to check for type of truncation
    def check_truncation(func):
        ret = ''
        if func == '':
            return "NAN"

        # Check for truncation at START
        start = func.splitlines()[0]
        # Case 1: No space between function name and parameter list
        if ' (' not in start:
            space_base = 1
        # Case 2: Space between function name and parameter list
        else:
            space_base = 2
        if start.rsplit('(', 1)[0].count(' ') < space_base:
            ret += 'START'
        # Check for truncation at END
        # Remove any potential end comments
        func = re.sub('\/\*.+?\*\/', '', func)
        if not (func.rstrip().endswith('}') or func.rstrip().endswith('};')):
            ret += 'END'

        ret = 'NONE' if ret == '' else ret
        return ret

    # Get df containing truncated entries
    df['Truncation'] = df['Function'].astype(str).apply(check_truncation)
    df = df.drop(columns=['Function'])
    df = df[df.Truncation != 'NONE']

    # pure START warnings are false positives for D2A
    #     as it handles multi-line return_types correctly.
    if dataset == 'D2A':
        df = df[df.Truncation != 'START']

    df.to_csv(f'dq_analysis/datasets/{dataset}/truncation.csv', index=False)


def report_completeness(dataset):
    """
    Report the measured completeness for the selected datasets,
        based on automated syntax analysis.
    """
    incomplete = pd.read_csv(f'dq_analysis/datasets/{dataset}/truncation.csv')
    data = Data(dataset).get_dataset()
    print(f'{dataset} Completeness: {(len(data) - len(incomplete))/len(data)}')
    print(f'Start Truncation: {len(incomplete[incomplete.Truncation == "START"])}')
    print(f'End Truncation: {len(incomplete[incomplete.Truncation == "END"])}')
    print(f'Both Truncation: {len(incomplete[incomplete.Truncation == "STARTEND"])}')
    print(f'Nan functions: {len(incomplete[incomplete.Truncation == "NAN"])}')
    print('-'*10)


if __name__ == '__main__':
    if sys.argv[1] == 'prepare':
        syntax_completeness(sys.argv[2])
    elif sys.argv[1] == 'measure':
        report_completeness(sys.argv[2])
    else:
        print(f"ERROR: Unknown command line argument: \"{sys.argv[1]}\"")
