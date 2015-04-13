#This script cleans up the raw data.

import pandas as pd
import re

data = pd.read_csv('/Users/ilya/Projects/last_words_project/raw_data.csv')

#Replace cells that have any of the following with a missing data value (99):
# pull_error  -- also produce counts
# jpg_pull_error  -- also produce counts

def missing_val_replacer(columns, missing, datfile):
    """Replaces pull_error and jpg_pull_error with 99"""

    for column in columns:
        for value in missing:
            column.replace(to_replace = value, value = 99,
                regex = True, inplace = True)

missing_vals = [re.compile('jpg'), re.compile('pull_e')]

cols = [data.last_statements, data.occupations, data.records, data.summaries]

missing_val_replacer(cols, [missing_vals], data)

#Strip whitespace from outside of cells:

col_names = ['last_statements', 'occupations', 'records', 'summaries']
def whitespace_stripper(columns):
    for column in columns:
        data[column] = data[column].str.strip()

whitespace_stripper(col_names)

data.to_csv("/Users/ilya/Projects/last_words_project/clean_data.csv")