# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

import asyncio
import time

import psutil
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import ChannelPrivate, FloodWait, InputUserDeactivated, UserIsBlocked
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import config
from PurviReaction import BOOT_TIME, app
from PurviReaction import database as db
from PurviReaction.utils import chunk_lines, is_bot_owner, readable_time

BROADCASTING = set()

@Client.on_message(filters.incoming, group=-1)
async def track(client, message):
    bot_id = client.me.id
    if message.chat.type == ChatType.PRIVATE:
        await db.add_user(bot_id, message.chat.id)
    else:
        await db.add_chat(bot_id, message.chat.id)


@Client.on_chat_member_updated()
async def my_status(client, update):
    new, old = update.new_chat_member, update.old_chat_member
    member = new or old
    if not member or member.user.id != client.me.id:
        return
    gone = new is None or new.status in (ChatMemberStatus.LEFT, ChatMemberStatus.BANNED)
    bot_id, chat = client.me.id, update.chat
    if chat.type == ChatType.PRIVATE:
        await (db.remove_user if gone else db.add_user)(bot_id, chat.id)
    else:
        await (db.remove_chat if gone else db.add_chat)(bot_id, chat.id)


@Client.on_message(filters.command(["stats", "ping"]))
async def stats(client, message):
    bot_id = client.me.id
    start = time.perf_counter()
    reply = await message.reply_text("ɢᴀᴛʜᴇʀɪɴɢ ꜱᴛᴀᴛꜱ...")
    ping = (time.perf_counter() - start) * 1000

    chats, users = await asyncio.gather(db.count_chats(bot_id), db.count_users(bot_id))
    cpu = await asyncio.to_thread(psutil.cpu_percent, 0.5)
    ram = psutil.virtual_memory().percent

    await reply.edit_text(
        f"📊 **<u>{client.me.mention}</u> ʙᴏᴛ ꜱᴛᴀᴛꜱ :**\n\n"
        f"🏘 **ᴛᴏᴛᴀʟ ᴄʜᴀᴛꜱ :** {chats}\n"
        f"👤 **ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ :** {users}\n"
        f"📈 **ᴛᴏᴛᴀʟ ʀᴇᴀᴄʜ :** {chats + users}\n\n"
        f"⏱ **ᴜᴘᴛɪᴍᴇ :** {readable_time(time.time() - BOOT_TIME)}\n"
        f"📡 **ᴘɪɴɢ :** {ping:.1f} ᴍꜱ\n\n"
        f"💾 **ʀᴀᴍ ᴜꜱᴀɢᴇ :** {ram}%\n"
        f"🖥 **ᴄᴘᴜ ᴜꜱᴀɢᴇ :** {cpu}%", 
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("✨ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url="https://t.me/Purvi_Bots")]]
        ),
    )


@Client.on_message(filters.command("cstats"))
async def cstats(client, message):
    if message.chat.type != ChatType.PRIVATE:
        return await message.reply_text(
            "**ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪɴ ʙᴏᴛ ᴅᴍ.**"
        )

    user = message.from_user
    if not user or user.id != config.OWNER_ID:
        return await message.reply_text(
            "**ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ.**"
        )

    clones = await db.get_clones()
    if not clones:
        return await message.reply_text("**ɴᴏ ᴄʟᴏɴᴇꜱ ꜰᴏᴜɴᴅ.**")

    rows, total_chats, total_users = [], 0, 0
    for clone in clones:
        chats, users = await asyncio.gather(
            db.count_chats(clone["bot_id"]), db.count_users(clone["bot_id"])
        )
        total_chats += chats
        total_users += users
        name = f"@{clone['username']}" if clone.get("username") else clone.get("name", clone["bot_id"])
        rows.append(f"• {name} : 🏘 {chats} | 👤 {users}")

    header = (
        f"**🤖 ᴄʟᴏɴᴇᴅ ʙᴏᴛꜱ : {len(clones)}**\n"
        f"🏘 ᴄʜᴀᴛꜱ : {total_chats} | 👤 ᴜꜱᴇʀꜱ : {total_users}\n\n"
    )
    for text in chunk_lines(header, rows):
        await message.reply_text(text)


async def deliver(client, target, source, text):
    for _ in range(2):
        try:
            if source:
                return await client.forward_messages(target, source.chat.id, source.id)
            return await client.send_message(target, text)
        except FloodWait as e:
            if e.value > 200:
                return None
            await asyncio.sleep(e.value)
    return None


async def send_all(client, targets, source, text, on_dead, dead_errors):
    sent = failed = 0
    for target in targets:
        try:
            if await deliver(client, target, source, text) is None:
                failed += 1
            else:
                sent += 1
        except dead_errors:
            await on_dead(client.me.id, target)
            failed += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.05)
    return sent, failed


@Client.on_message(filters.command(["broadcast", "gcast"]))
async def broadcast(client, message):
    bot_id = client.me.id
    if not (message.from_user and await is_bot_owner(bot_id, message.from_user.id)):
        return await message.reply_text(
            "**ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ.**"
        )
    if bot_id in BROADCASTING:
        return await message.reply_text("ᴀ ʙʀᴏᴀᴅᴄᴀꜱᴛ ɪꜱ ᴀʟʀᴇᴀᴅʏ ʀᴜɴɴɪɴɢ ᴏɴ ᴛʜɪꜱ ʙᴏᴛ. ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ.")

    source = message.reply_to_message
    raw = message.text or message.caption or ""
    text = raw.split(None, 1)[1].strip() if len(message.command) > 1 else ""
    if not source and not text:
        return await message.reply_text(
            "**ꜱᴇɴᴅ** `/broadcast ʏᴏᴜʀ ᴛᴇxᴛ` **ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴡɪᴛʜ** `/broadcast`."
        )

    BROADCASTING.add(bot_id)
    try:
        status = await message.reply_text("**ꜱᴛᴀʀᴛᴇᴅ ʙʀᴏᴀᴅᴄᴀꜱᴛɪɴɢ...**")
        chats = await db.get_chats(bot_id)
        users = await db.get_users(bot_id)
        chats_sent, chats_failed = await send_all(
            client, chats, source, text, db.remove_chat, (ChannelPrivate,)
        )
        users_sent, users_failed = await send_all(
            client, users, source, text, db.remove_user, (UserIsBlocked, InputUserDeactivated)
        )
        await status.edit_text(
            "**ʙʀᴏᴀᴅᴄᴀꜱᴛ ꜰɪɴɪꜱʜᴇᴅ ✅**\n\n"
            f"🏘 **ᴄʜᴀᴛꜱ :** ꜱᴇɴᴛ {chats_sent}, ꜰᴀɪʟᴇᴅ {chats_failed}\n"
            f"👤 **ᴜꜱᴇʀꜱ :** ꜱᴇɴᴛ {users_sent}, ꜰᴀɪʟᴇᴅ {users_failed}"
        )
    finally:
        BROADCASTING.discard(bot_id)
# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Purvi-Reaction
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
