import asyncio
from create_bot import bot, dp, admins, set_commands
from handlers.admin_panel import admin_router
from handlers.user_panel import user_router
# from work_time.time_func import send_time_msg



# Функция, которая выполнится когда бот запустится

async def start_bot():
    await set_commands()
    # count_users = await get_all_users(count=True)
    try:
        for admin_id in admins:
            await bot.send_message(admin_id, f'Я запущен🥳. Сейчас в базе данных <b>{0}</b> опросов.')
    except:
        pass

# Функция, которая выполнится когда бот завершит свою работу
async def stop_bot():
    try:
        for admin_id in admins:
            await bot.send_message(admin_id, 'Бот остановлен. За что?😔')
    except:
        pass

async def main():
    dp.include_router(admin_router)
    dp.include_router(user_router)

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())