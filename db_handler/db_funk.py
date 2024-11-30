from create_bot import db_manager
import asyncio
from sqlalchemy import Integer, String, Text, Boolean
from typing import Dict, List, Union


async def create_table_polls(table_name: str = 'pulse_polls'):
    """

    :param table_name:
    :return:
    """
    async with db_manager as client:
        await client.create_table(table_name=table_name, columns=[
            {'name': 'id', 'type': Integer,
             'options': {'primary_key': True, 'autoincrement': True}},
            {'name': 'name', 'type': String},
            {'name': 'description', 'type': Text},
            {'name': 'type', 'type': String},
            {'name': 'is_active', 'type': Boolean},
            {'name': 'questions', 'type': Text},
            {'name': 'options', 'type': Text},
            {'name': 'results', 'type': Text},
            {'name': 'respondents_number', 'type': Integer},
        ])


async def get_all_polls(table_name: str = 'pulse_polls', count: bool = False):
    """

    :param table_name:
    :param count:
    :return:
    """
    async with db_manager as client:
        all_polls = await client.select_data(table_name=table_name)
        if count:
            return len(all_polls)
        else:
            return all_polls


async def insert_poll(user_data: dict, table_name: str = 'pulse_polls'):
    """

    :param user_data:
    :param table_name:
    :return:
    """
    async with db_manager as client:
        await client.insert_data_with_update(
            table_name=table_name,
            records_data=user_data,
            conflict_column='name',
            update_on_conflict=False)


async def update_poll(user_data: Dict, table_name: str = 'pulse_polls'):
    """

    :param user_data:
    :param table_name:
    :return:
    """
    async with db_manager as client:
        await client.update_data(
            table_name=table_name,
            where_dict={'id': user_data['id']},
            update_dict=user_data
        )


async def get_poll_by_name(poll_name: str, table_name='pulse_polls') -> Dict:
    """

    :param poll_name:
    :param table_name:
    :return:
    """
    async with db_manager as client:
        return await client.select_data(
            table_name=table_name,
            where_dict={'name': poll_name},
            one_dict=True
        )


async def get_poll_by_id(poll_id: int, table_name='pulse_polls') -> Dict:
    """

    :param poll_id:
    :param table_name:
    :return:
    """
    async with db_manager as client:
        return await client.select_data(
            table_name=table_name,
            where_dict={'id': poll_id},
            one_dict=True)


async def get_all_activity_polls(
        table_name: str = 'pulse_polls',
        is_active: bool = False) -> Union[List[Dict], Dict]:
    """

    :param table_name:
    :param is_active:
    :return:
    """
    async with db_manager as client:
        return await client.select_data(
            table_name=table_name,
            where_dict={'is_active': is_active})


async def delete_poll_by_name(poll_name: str, table_name: str = 'pulse_polls'):
    """

    :param poll_name:
    :param table_name:
    :return:
    """
    async with db_manager as client:
        return await client.delete_data(
            table_name=table_name,
            where_dict={'name': poll_name})


async def delete_poll_by_id(poll_id: int, table_name: str = 'pulse_polls'):
    """

    :param poll_id:
    :param table_name:
    :return:
    """
    async with db_manager as client:
        return await client.delete_data(
            table_name=table_name,
            where_dict={'id': poll_id})

asyncio.run(create_table_polls())
