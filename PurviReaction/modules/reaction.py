# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

import asyncio
import random

from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import FloodWait

import config
from PurviReaction import database as db
from PurviReaction.utils import is_bot_owner

GROUPS = (ChatType.GROUP, ChatType.SUPERGROUP)


@Client.on_message(filters.incoming & ~filters.service & ~filters.regex(r"^/"), group=1)
async def react(client, message):
    if message.chat.type in GROUPS and not await db.reaction_enabled(client.me.id, message.chat.id):
        return
    try:
        await message.react(random.choice(config.REACTIONS))
    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception:
        pass


async def can_switch(client, message):
    if message.sender_chat and message.sender_chat.id == message.chat.id:
        return True
    user = message.from_user
    if not user:
        return False
    if await is_bot_owner(client.me.id, user.id):
        return True
    try:
        member = await client.get_chat_member(message.chat.id, user.id)
    except Exception:
        return False
    return member.status in (ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR)


@Client.on_message(filters.command("reaction") & (filters.private | filters.group))
async def reaction_switch(client, message):
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text(
            "**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs.**"
        )
    if not await can_switch(client, message):
        return await message.reply_text(
            "**ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs.**"
        )

    bot_id, chat_id = client.me.id, message.chat.id
    arg = message.command[1].lower() if len(message.command) > 1 else None
    if arg in ("on", "off"):
        await db.set_reaction(bot_id, chat_id, arg == "on")

    state = "ᴏɴ ✅" if await db.reaction_enabled(bot_id, chat_id) else "ᴏғғ ❌"
    text = f"**ʀᴇᴀᴄᴛɪᴏɴs ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ ᴀʀᴇ {state}.**"
    if arg not in ("on", "off"):
        text += "\n\n**ᴜsᴇ :** `/reaction on` ᴏʀ `/reaction off`."
    await message.reply_text(text)

# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Purvi-Reaction
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
