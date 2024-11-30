from typing import List, Dict, Any
import pandas as pd
import os


def list_str_to_string(string_list: List[str]) -> str:
    """
    Helper function that converts a list of strings
    into a string with a separator "," for list items.

    :param string_list: List of strings.
    :return: String with a separator ",".
    """
    return ','.join(string_list)


def string_to_list(input_string: str) -> List[str]:
    """
    Helper function that converts a string with a "," separator
    into a list of strings.

    :param input_string: String with a "," separator.
    :return: List of strings.
    """
    return input_string.split(',')


def nested_list_str_to_string(nested_list: List[List[str]]) -> str:
    """
    Helper function that converts nested lists of strings
    to a string with delimiters "," and "|" for all list items.
    Nested lists are separated by "|".
    Items of nested lists are separated by ",".

    :param nested_list: Nested lists of string.
    :return: Converted string.
    """
    return '|'.join([','.join(group) for group in nested_list])


def string_to_nested_list_str(input_string: str) -> List[List[str]]:
    """
    Helper function that converts a string with
    delimiters "," and "|" to nested lists strings.
    Nested lists are separated by "|".
    Items of nested lists are separated by ",".

    :param input_string: String with delimiters "," and "|".
    :return: Converted nested lists of strings.
    """
    return [group.split(',') for group in input_string.split('|')]


def nested_list_int_to_string(nested_list: List[List[int]]) -> str:
    """
    Helper function that converts nested lists of integers
    to a string with "," and "|" separators for all list items.
    Nested lists are separated by "|".
    Items of nested lists are separated by ",".

    :param nested_list: Nested lists of integers.
    :return: Converted string.
    """
    return '|'.join([','.join(map(str, group)) for group in nested_list])


def string_to_nested_list_int(input_string: str) -> List[List[int]]:
    """
    Helper function that converts a string with
    delimiters "," and "|" to nested lists integers.
    Nested lists are separated by "|".
    Items of nested lists are separated by ",".

    :param input_string: String with delimiters "," and "|".
    :return: Converted nested lists of integers.
    """
    return [list(map(int, group.split(',')))
            for group in input_string.split('|')]


def create_result_tbl(poll: Dict[str, Any]) -> str:
    """
    Create a table of poll results and save it to an Excel file.

    :param poll: Poll data.
    :return: Path of the created Excel file.
    """
    # Create a .results directory for temporary storage of result files.
    d = os.path.join(os.getcwd(), '.results')
    if not os.path.exists(d):
        os.makedirs(d)
    filepath = os.path.join(d, f'{poll["name"]}.xlsx')
    questions = string_to_list(poll['questions'])
    options = string_to_nested_list_str(poll['options'])
    results = string_to_nested_list_int(poll['results'])
    all_tables = []
    # Create table of results.
    for i in range(len(questions)):
        df = pd.DataFrame([options[i], results[i]])
        title_row = pd.DataFrame([questions[i]])
        all_tables.append(title_row)
        all_tables.append(df)
        all_tables.append(pd.DataFrame([['', '']]))
    final_df = pd.concat(all_tables, ignore_index=True)
    # Write table to Excel file.
    final_df.to_excel(
        filepath, sheet_name='Combined_Tables',
        index=False, header=False)
    return filepath


def delete_result_tbl(filepath: str):
    """
    Delete existing file.

    :param filepath: Path of the file to be deleted.
    """
    if os.path.exists(filepath):
        os.remove(filepath)
