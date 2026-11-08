# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import config

@Client.on_message(filters.incoming & filters.private, group=-2)
async def must_join_channel(client, message):
    channel = config.UPDATE_CHNL
    if not channel or not message.from_user:
        return
    try:
        await client.get_chat_member(channel, message.from_user.id)
    except UserNotParticipant:
        if str(channel).lstrip("-").isdigit():
            link = (await client.get_chat(channel)).invite_link
        else:
            link = f"https://t.me/{channel}"
        try:
            await message.reply_photo(
                photo="https://files.catbox.moe/6f9rgp.jpg",
                caption=(
                    f"**𝐇ᴇʟʟᴏ 𝐁ᴀʙʏ...{message.from_user.mention},**\n\n"
                    f"**• ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴊᴏɪɴ ᴛʜᴇ [sᴜᴘᴘᴏʀᴛ ᴄʜᴀɴɴᴇʟ]({link}) ᴛᴏ ᴄʜᴇᴀᴋ ᴍʏ ғᴇᴀᴛᴜʀᴇs.**\n\n"
                    "**» ᴀғᴛᴇʀ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ ʙᴀᴄᴋ ᴛᴏ ʙᴏᴛ & ᴛʏᴘᴇ /start ᴀɢᴀɪɴ**"
                ),
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=link)]]
                ),
            )
        except Exception:
            return
        message.stop_propagation()
    except Exception:
        return  

# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Purvi-Reaction
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
