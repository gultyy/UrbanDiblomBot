from typing import List, Dict, Any
import pandas as pd
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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


def create_result_tbl(poll: Dict[str, Any]) -> List[str]:
    """
    Create a table of poll results and save it to an Excel file.

    :param poll: Poll data.
    :return: Path of the created Excel file.
    """
    # Create a .results directory for temporary storage of result files.
    d = os.path.join(os.getcwd(), '.results')
    if not os.path.exists(d):
        os.makedirs(d)
    tbl_filepath = os.path.join(d, f'{poll["name"]}.xlsx')
    visual_filepath = os.path.join(d, f'{poll["name"]}.png')
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
        tbl_filepath, sheet_name='Combined_Tables',
        index=False, header=False)
    # Create histograms
    fig = make_subplots(rows=1, cols=len(questions), subplot_titles=questions)
    for i, (question, opt, res) in enumerate(zip(questions, options, results)):
        fig.add_trace(go.Bar(x=opt, y=res, name=f'{question}'), row=1, col=i + 1)
    fig.update_layout(
        title='Результаты опросов',
        xaxis_title='Варианты',
        yaxis_title='Количество голосов',
        template='plotly_white'
    )
    # Write visualization to file
    fig.write_image(visual_filepath)
    return [tbl_filepath, visual_filepath]


def delete_result_tbl(filepaths: List[str]):
    """
    Delete existing files.

    :param filepaths: Paths of the files to be deleted.
    """
    for filepath in filepaths:
        if os.path.exists(filepath):
            os.remove(filepath)
