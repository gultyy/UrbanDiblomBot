from create_bot import db_manager
import asyncio
from sqlalchemy import Integer, String, Text, Boolean
from typing import Dict, List, Union


async def create_polls_table(table_name: str = 'pulse_polls') -> None:
    """
    Create a table in the database.

    :param table_name: The name of the table being created.
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


async def get_all_polls(table_name: str = 'pulse_polls',
                        count: bool = False) -> Union[List[Dict], Dict, int]:
    """
    Get all polls data or the total number of polls.

    :param table_name: The name of the table to retrieve polls from.
    :param count: True - get total number of polls. False - get all polls data.
    :return: All polls data or total number of polls.
    """
    async with db_manager as client:
        all_polls = await client.select_data(table_name=table_name)
        if count:
            return len(all_polls)
        else:
            return all_polls


async def insert_poll(poll: dict, table_name: str = 'pulse_polls') -> None:
    """
    Insert the poll data to the table.

    :param poll: The poll that needs to be inserted to the table.
    :param table_name: The name of the table to which to insert the poll data.
    """
    async with db_manager as client:
        await client.insert_data_with_update(
            table_name=table_name,
            records_data=poll,
            conflict_column='name',
            update_on_conflict=False)


async def update_poll(poll: Dict, table_name: str = 'pulse_polls') -> None:
    """
    Update the poll data in the table.

    :param poll: Updating poll data.
    :param table_name: The name of the table to which to update the poll data.
    """
    async with db_manager as client:
        await client.update_data(
            table_name=table_name,
            where_dict={'id': poll['id']},
            update_dict=poll
        )


async def get_poll_by_name(poll_name: str, table_name='pulse_polls') -> Dict:
    """
    Get the poll from the table by the poll name.

    :param poll_name: Poll name.
    :param table_name: The name of the table from which to get the poll.
    :return: Poll dictionary.
    """
    async with db_manager as client:
        return await client.select_data(
            table_name=table_name,
            where_dict={'name': poll_name},
            one_dict=True
        )


async def get_poll_by_id(poll_id: int, table_name='pulse_polls') -> Dict:
    """
    Get the poll from the table by the poll ID.

    :param poll_id: Poll ID.
    :param table_name: The name of the table from which to get the poll.
    :return: Poll dictionary.
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
    Get all active and inactive polls data.

    :param table_name: The name of the table from
    which to get the data of polls.
    :param is_active: True - active polls. False - inactive polls.
    :return: All active or inactive polls.
    """
    async with db_manager as client:
        return await client.select_data(
            table_name=table_name,
            where_dict={'is_active': is_active})


async def delete_poll_by_name(poll_name: str,
                              table_name: str = 'pulse_polls') -> None:
    """
    Delete the poll data from the table by the poll ID.

    :param poll_name: Poll name.
    :param table_name: The name of the table
    from which to delete the poll data.
    """
    async with db_manager as client:
        return await client.delete_data(
            table_name=table_name,
            where_dict={'name': poll_name})


async def delete_poll_by_id(poll_id: int,
                            table_name: str = 'pulse_polls') -> None:
    """
    Delete the poll data from the table by the poll ID.

    :param poll_id: Poll ID.
    :param table_name: The name of the table
    from which to delete the poll data.
    """
    async with db_manager as client:
        return await client.delete_data(
            table_name=table_name,
            where_dict={'id': poll_id})

# Create polls table
asyncio.run(create_polls_table())
