from pyrogram import Client, filters
import datetime
import time
import asyncio

from database.users import get_all_users, total_users_count, delete_user
from config import ADMINS
from utils import broadcast_messages

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
async def verupikkals(bot, message):
    users = get_all_users()                      # Motor cursor, no await
    b_msg = message.reply_to_message
    sts = await message.reply_text("Broadcasting your messages...")

    start_time = time.time()
    total_users = await total_users_count()
    done = blocked = deleted = failed = success = 0

    async for user in users:
        user_id = int(user["user_id"])
        pti, sh = await broadcast_messages(user_id, b_msg)

        if pti:
            success += 1
        else:
            if sh == "Blocked":
                blocked += 1
            elif sh == "Deleted":
                deleted += 1
                await delete_user(user_id)       # optional clean-up
            else:
                failed += 1

        done += 1
        await asyncio.sleep(2)

        if done % 20 == 0:
            await sts.edit(
                f"Broadcast in progress:\n\n"
                f"Total Users: {total_users}\n"
                f"Completed : {done} / {total_users}\n"
                f"Success   : {success}\n"
                f"Blocked   : {blocked}\n"
                f"Deleted   : {deleted}"
            )

    time_taken = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts.edit(
        f"Broadcast Completed:\n"
        f"Completed in {time_taken} seconds.\n\n"
        f"Total Users: {total_users}\n"
        f"Completed : {done} / {total_users}\n"
        f"Success   : {success}\n"
        f"Blocked   : {blocked}\n"
        f"Deleted   : {deleted}"
    )
    await sts.edit(f"Broadcast Completed:\nCompleted in {time_taken} seconds.\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")
