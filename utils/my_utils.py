from typing import List, Dict, Any
import pandas as pd
import os


def list_str_to_string(string_list: List[str]) -> str:
    """

    :param string_list:
    :return:
    """
    return ','.join(string_list)


def string_to_list(input_string: str) -> List[str]:
    """

    :param input_string:
    :return:
    """
    return input_string.split(',')


def nested_list_str_to_string(nested_list: List[List[str]]):
    """

    :param nested_list:
    :return:
    """
    return '|'.join([','.join(group) for group in nested_list])


def string_to_nested_list_str(input_string: str) -> List[List[str]]:
    """

    :param input_string:
    :return:
    """
    return [group.split(',') for group in input_string.split('|')]


def nested_list_int_to_string(nested_list: List[List[int]]) -> str:
    """

    :param nested_list:
    :return:
    """
    return '|'.join([','.join(map(str, group)) for group in nested_list])


def string_to_nested_list_int(input_string: str) -> List[List[int]]:
    """

    :param input_string:
    :return:
    """
    return [list(map(int, group.split(','))) for group in input_string.split('|')]


def create_result_tbl(poll: Dict[str, Any]) -> str:
    """

    :param poll:
    :return:
    """
    d = os.path.join(os.getcwd(), '.results')
    if not os.path.exists(d):
        os.makedirs(d)
    filename = os.path.join(d, f'{poll["name"]}.xlsx')
    questions = string_to_list(poll['questions'])
    options = string_to_nested_list_str(poll['options'])
    results = string_to_nested_list_int(poll['results'])
    all_tables = []
    for i in range(len(questions)):
        df = pd.DataFrame([options[i], results[i]])
        title_row = pd.DataFrame([questions[i]])
        all_tables.append(title_row)
        all_tables.append(df)
        all_tables.append(pd.DataFrame([['', '']]))
    final_df = pd.concat(all_tables, ignore_index=True)
    final_df.to_excel(
        filename, sheet_name='Combined_Tables',
        index=False, header=False)
    return filename


def delete_result_tbl(filename: str):
    """

    :param filename:
    :return:
    """
    if os.path.exists(filename):
        os.remove(filename)
