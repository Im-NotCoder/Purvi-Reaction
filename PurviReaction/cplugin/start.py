# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

from pyrogram import Client, filters
from PurviReaction import ui

@Client.on_message(filters.command("start"))
async def start(client, message):
    if message.from_user:
        await client.send_photo(
            chat_id=message.chat.id,
            photo=ui.CLONE_PHOTO,
            caption=ui.clone_start_caption(message.from_user),
            reply_markup=ui.clone_start_buttons(client),
        )

# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Purvi-Reaction
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
