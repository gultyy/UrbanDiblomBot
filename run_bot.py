import asyncio
from create_bot import bot, dp, admins, set_commands
from handlers.admin_panel import admin_router
from handlers.user_panel import user_router
from db_handler.db_funk import get_all_polls


async def start_bot():
    """
    Notifies all admins about the startup.
    Called when the bot are startuped.
    """
    await set_commands()
    count_polls = await get_all_polls(count=True)
    try:
        for admin_id in admins:
            await bot.send_message(
                admin_id,
                'Pulsepoll запущен. '
                f'Сейчас в базе данных <b>{count_polls}</b> опросов.')
    except Exception:
        pass


async def stop_bot():
    """
    Notifies all admins about the bot's shutdown.
    Called when the bot is stopped.
    """
    try:
        for admin_id in admins:
            await bot.send_message(admin_id, 'Pulsepoll остановлен.')
    except Exception:
        pass


async def main():
    """
    The main function for starting the bot.
    """
    dp.include_router(admin_router)
    dp.include_router(user_router)

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot,
                               allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

# Run bot
if __name__ == "__main__":
    asyncio.run(main())
