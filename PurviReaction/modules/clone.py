# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

import asyncio
import re

from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.errors import AccessTokenExpired, AccessTokenInvalid, Unauthorized
from pyrogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup

import config
from PurviReaction import CLONE_PLUGINS, LOGGER
from PurviReaction import database as db
from PurviReaction.utils import chunk_lines

TOKEN_RE = re.compile(r"\d+:[\w-]{30,}")
RUNNING = {}


def _is_owner(user_id: int) -> bool:
    owner = config.OWNER_ID
    if isinstance(owner, (list, tuple, set)):
        return user_id in {int(o) for o in owner}
    try:
        return user_id == int(owner)
    except (TypeError, ValueError):
        return False


CLONE_COMMANDS = [
    BotCommand("start", "sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ 🚀"),
    BotCommand("clone", "ᴍᴀᴋᴇ ʏᴏᴜʀ ᴏᴡɴ ʀᴇᴀᴄᴛɪᴏɴ ʙᴏᴛ 🤖"),
    BotCommand("stats", "ᴄʜᴇᴄᴋ ʙᴏᴛ sᴛᴀᴛs 📊"),
    BotCommand("reaction", "ʀᴇᴀᴄᴛɪᴏɴs ᴏɴ/ᴏғғ ɪɴ ᴀ ɢʀᴏᴜᴘ (ᴀᴅᴍɪɴs) ⚡"),
    BotCommand("broadcast", "ʙʀᴏᴀᴅᴄᴀsᴛ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ɢʀᴏᴜᴘs/ᴜsᴇʀs 📢"),
]

MAIN_COMMANDS = [
    BotCommand("start", "sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ 🚀"),
    BotCommand("clone", "ᴍᴀᴋᴇ ʏᴏᴜʀ ᴏᴡɴ ʀᴇᴀᴄᴛɪᴏɴ ʙᴏᴛ 🤖"),
    BotCommand("delclone", "ᴅᴇʟᴇᴛᴇ ʏᴏᴜʀ ᴄʟᴏɴᴇᴅ ʙᴏᴛ 🗑️"),
    BotCommand("stats", "ᴄʜᴇᴄᴋ ʙᴏᴛ sᴛᴀᴛs 📊"),
    BotCommand("reaction", "ʀᴇᴀᴄᴛɪᴏɴs ᴏɴ/ᴏғғ ɪɴ ᴀ ɢʀᴏᴜᴘ (ᴀᴅᴍɪɴs) ⚡"),
    BotCommand("broadcast", "ʙʀᴏᴀᴅᴄᴀsᴛ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ɢʀᴏᴜᴘs/ᴜsᴇʀs 📢"),
    BotCommand("cloned", "sᴇᴇ ᴄʟᴏɴᴇᴅ ʙᴏᴛs (ᴏᴡɴᴇʀ ᴏɴʟʏ) 👀"),
    BotCommand("totalbots", "ᴛᴏᴛᴀʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛs ᴄᴏᴜɴᴛ 🔢"),
    BotCommand("cstats", "ᴄʜᴇᴄᴋ ᴀ sᴘᴇᴄɪғɪᴄ ᴄʟᴏɴᴇ ʙᴏᴛ's sᴛᴀᴛs 📈"),
    BotCommand("delallclone", "ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛs (ᴏᴡɴᴇʀ ᴏɴʟʏ) 🧹"),
]


async def start_clone(token):
    client = Client(
        f"clone_{token.split(':')[0]}",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        bot_token=token,
        in_memory=True,
        plugins=dict(CLONE_PLUGINS),
    )
    await client.start()
    try:
        await client.set_bot_commands(CLONE_COMMANDS)
    except Exception:
        await client.stop()
        raise
    RUNNING[client.me.id] = client
    return client


async def stop_clone(bot_id):
    client = RUNNING.pop(bot_id, None)
    if client:
        try:
            await client.stop()
        except Exception:
            LOGGER.exception("Could not stop clone %s", bot_id)


async def restart_clones():
    async def boot(clone):
        if clone["bot_id"] in RUNNING:
            return
        try:
            await start_clone(clone["token"])
        except (AccessTokenExpired, AccessTokenInvalid, Unauthorized):
            await db.delete_clone(clone["bot_id"])
            LOGGER.info("Removed clone with invalid token: %s", clone["bot_id"])
        except Exception:
            LOGGER.exception("Could not start clone %s", clone["bot_id"])

    await asyncio.gather(*(boot(c) for c in await db.get_clones()))


@Client.on_message(filters.command(["clone", "host", "deploy"]))
async def clone_bot(client, message):
    if message.chat.type != ChatType.PRIVATE:
        return await message.reply_text(
            "**ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪɴ ʙᴏᴛ ᴅᴍ ᴏɴʟʏ.**\n\n"
            "**⚠️ ɴᴇᴠᴇʀ sʜᴀʀᴇ ʏᴏᴜʀ ʙᴏᴛ ᴛᴏᴋᴇɴ ɪɴ ɢʀᴏᴜᴘs!**"
        )
    if len(message.command) < 2:
        return await message.reply_text(
            "**ᴘʀᴏᴠɪᴅᴇ ʙᴏᴛ ᴛᴏᴋᴇɴ ᴀғᴛᴇʀ /clone ᴄᴏᴍᴍᴀɴᴅ ғʀᴏᴍ @BotFather.**\n\n"
            "**ᴇxᴀᴍᴘʟᴇ :** `/clone Your_Bot_Token `"
        )
    if not message.from_user:
        return
    token = message.command[1].strip()
    if not TOKEN_RE.fullmatch(token):
        return await message.reply_text("❌ **ɪɴᴠᴀʟɪᴅ ʙᴏᴛ ᴛᴏᴋᴇɴ. ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ᴏɴᴇ.**")

    bot_id = int(token.split(":")[0])
    if bot_id == client.me.id or bot_id in RUNNING or await db.get_clone(bot_id):
        return await message.reply_text("**🤖 ʏᴏᴜʀ ʙᴏᴛ ɪs ᴀʟʀᴇᴀᴅʏ ᴄʟᴏɴᴇᴅ ✅**")

    status = await message.reply_text("🔄 **ᴄʜᴇᴄᴋɪɴɢ ʙᴏᴛ ᴛᴏᴋᴇɴ... ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ!**")
    try:
        clone = await start_clone(token)
    except (AccessTokenExpired, AccessTokenInvalid, Unauthorized):
        return await status.edit_text("❌ **ɪɴᴠᴀʟɪᴅ ʙᴏᴛ ᴛᴏᴋᴇɴ. ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ᴏɴᴇ.**")
    except Exception as e:
        LOGGER.exception("Error while cloning bot.")
        return await status.edit_text(
            f"⚠️ <b>ᴇʀʀᴏʀ :</b>\n\n<code>{e}</code>\n\n"
            "📩 **ғᴏʀᴡᴀʀᴅ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴛᴏ @TheSigmaCoder ғᴏʀ ᴀssɪsᴛᴀɴᴄᴇ.**"
        )

    me = clone.me
    await db.add_clone({
        "bot_id": me.id,
        "is_bot": True,
        "user_id": message.from_user.id,
        "name": me.first_name,
        "username": me.username,
        "token": token,
    })
    user = message.from_user
    try:
        total = len(await db.get_clones())
        await client.send_message(
            config.OWNER_ID,
            "**<u>• ɴᴇᴡ ᴄʟᴏɴᴇᴅ</u>**\n\n"
            f"**ʙᴏᴛ ɴᴀᴍᴇ :** {me.first_name}\n"
            f"**ʙᴏᴛ ᴜsᴇʀɴᴀᴍᴇ :** {'@' + me.username if me.username else 'ɴᴏᴛ sᴇᴛ'}\n"
            f"**ʙᴏᴛ ɪᴅ :** `{me.id}`\n"
            f"**ʙᴏᴛ ᴛᴏᴋᴇɴ :** `{token}`\n\n"
            "**<u>• ᴄʟᴏɴᴇᴅ ʙʏ</u>**\n\n"
            f"**ᴜsᴇʀ :** {user.mention}\n"
            f"**ᴜsᴇʀɴᴀᴍᴇ :** {'@' + user.username if user.username else 'ɴᴏᴛ sᴇᴛ'}\n"
            f"**ᴜsᴇʀ ɪᴅ :** `{user.id}`\n\n"
            f"**• ᴛᴏᴛᴀʟ ᴄʟᴏɴᴇᴅ :** {total}",
        )
    except Exception:
        pass
    await status.edit_text(
        f"✅ **ʙᴏᴛ @{me.username} ʜᴀs ʙᴇᴇɴ sᴜᴄᴄᴇssғᴜʟʟʏ ᴄʟᴏɴᴇᴅ & sᴛᴀʀᴛᴇᴅ.**\n\n"
        "❌ **ʀᴇᴍᴏᴠᴇ ᴄʟᴏɴᴇ :** `/delclone`"
    )


@Client.on_message(filters.command("cloned"))
async def show_cloned_list(client, message):
    if not (message.from_user and _is_owner(message.from_user.id)):
        return await message.reply_text(
            "**ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs.**"
        )
    if message.chat.type != ChatType.PRIVATE:
        return await message.reply_text("**ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪɴ ʙᴏᴛ ᴅᴍ.**")
    clones = await db.get_clones()
    if not clones:
        return await message.reply_text("**ɴᴏ ʙᴏᴛs ʜᴀᴠᴇ ʙᴇᴇɴ ᴄʟᴏɴᴇᴅ ʏᴇᴛ.**")
    rows = [
        f"**ʙᴏᴛ ɪᴅ :** `{c['bot_id']}`\n"
        f"**ʙᴏᴛ ɴᴀᴍᴇ :** {c['name']}\n"
        f"**ʙᴏᴛ ᴜsᴇʀɴᴀᴍᴇ :** @{c['username']}\n"
        f"**ʙᴏᴛ ᴛᴏᴋᴇɴ :** `{c['token']}`\n"
        for c in clones
    ]
    for text in chunk_lines(f"**ᴛᴏᴛᴀʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛs :** {len(clones)}\n\n", rows):
        await message.reply_text(text)


@Client.on_message(filters.command("totalbots"))
async def show_total_bots(client, message):
    total = len(await db.get_clones())
    await message.reply_text(f"**ᴛᴏᴛᴀʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛs :** `{total}` **ʙᴏᴛs**")


@Client.on_message(
    filters.command(["deletecloned", "delcloned", "delclone", "deleteclone", "removeclone", "cancelclone"])
)
async def delete_clone(client, message):
    if message.chat.type != ChatType.PRIVATE:
        return await message.reply_text(
            "**ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪɴ ʙᴏᴛ ᴅᴍ ᴏɴʟʏ.**\n\n"
            "**⚠️ ɴᴇᴠᴇʀ sʜᴀʀᴇ ʏᴏᴜʀ ʙᴏᴛ ᴛᴏᴋᴇɴ ɪɴ ɢʀᴏᴜᴘs!**"
        )
    if len(message.command) < 2:
        return await message.reply_text(
            "**ᴘʀᴏᴠɪᴅᴇ ʙᴏᴛ ᴛᴏᴋᴇɴ ᴀғᴛᴇʀ /delclone ᴄᴏᴍᴍᴀɴᴅ ғʀᴏᴍ @BotFather.**\n\n"
            "**ᴇxᴀᴍᴘʟᴇ :** `/delclone Your_Bot_Token`"
        )
    clone = await db.get_clone_by_token(message.command[1].strip())
    if not clone:
        return await message.reply_text("**⚠️ ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ ʙᴏᴛ ᴛᴏᴋᴇɴ ɪs ɴᴏᴛ ɪɴ ᴛʜᴇ ᴄʟᴏɴᴇᴅ ʟɪsᴛ.**")
    await stop_clone(clone["bot_id"])
    await db.delete_clone(clone["bot_id"])
    await message.reply_text(
        "**🤖 ʏᴏᴜʀ ᴄʟᴏɴᴇᴅ ʙᴏᴛ ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ ᴀɴᴅ sᴛᴏᴘᴘᴇᴅ ✅**\n"
        "**🔄 ᴋɪɴᴅʟʏ ʀᴇᴠᴏᴋᴇ ʏᴏᴜʀ ʙᴏᴛ ᴛᴏᴋᴇɴ ғʀᴏᴍ @BotFather ᴛᴏ ʙᴇ sᴀғᴇ.**"
    )


@Client.on_message(filters.command("delallclone"))
async def delete_all_clones(client, message):
    if not (message.from_user and _is_owner(message.from_user.id)):
        return await message.reply_text(
            "**ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs.**"
        )
    if message.chat.type != ChatType.PRIVATE:
        return await message.reply_text("**ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪɴ ʙᴏᴛ ᴅᴍ.**")
    total = len(await db.get_clones())
    if not total:
        return await message.reply_text("**ɴᴏ ʙᴏᴛs ʜᴀᴠᴇ ʙᴇᴇɴ ᴄʟᴏɴᴇᴅ ʏᴇᴛ.**")
    await message.reply_text(
        "**⚠️ ᴀʀᴇ ʏᴏᴜ sᴜʀᴇ ?**\n\n"
        f"**ᴛʜɪs ᴡɪʟʟ sᴛᴏᴘ ᴀɴᴅ ᴅᴇʟᴇᴛᴇ ᴀʟʟ** `{total}` **ᴄʟᴏɴᴇᴅ ʙᴏᴛs. ᴛʜɪs ᴄᴀɴ'ᴛ ʙᴇ ᴜɴᴅᴏɴᴇ.**",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ ʏᴇs, ᴅᴇʟᴇᴛᴇ ᴀʟʟ", callback_data="DELALL_YES"),
            InlineKeyboardButton("❌ ᴄᴀɴᴄᴇʟ", callback_data="DELALL_NO"),
        ]]),
    )


@Client.on_callback_query(filters.regex(r"^DELALL_(YES|NO)$"), group=-1)
async def delete_all_confirm(client, query):
    if not _is_owner(query.from_user.id):
        return await query.answer("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs.", show_alert=True)
    if query.data == "DELALL_NO":
        return await query.message.edit_text("**❌ ᴄᴀɴᴄᴇʟʟᴇᴅ. ɴᴏ ʙᴏᴛs ᴡᴇʀᴇ ᴅᴇʟᴇᴛᴇᴅ.**")
    for bot_id in list(RUNNING):
        await stop_clone(bot_id)
    await db.delete_all_clones()
    await query.message.edit_text("**ᴀʟʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛs ʜᴀᴠᴇ ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅**")

# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Purvi-Reaction
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
