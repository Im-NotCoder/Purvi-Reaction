# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

import asyncio
from pyrogram import idle
import config
from PurviReaction import LOGGER, LOOP, app
from PurviReaction import database as db
from PurviReaction.modules import clone


async def main():
    await db.setup()
    await app.start()
    await app.set_bot_commands(clone.MAIN_COMMANDS)

    try:
        await app.send_message(
            config.OWNER_ID,
            f"**{app.me.mention} Is started ✅**",
        )
    except Exception:
        LOGGER.info(
            "@%s Started, Please Start The Bot From Owner Id.", app.me.username
        )

    LOGGER.info("@%s Started.", app.me.username)

    restarting = asyncio.create_task(clone.restart_clones())

    await restarting
    started = len(clone.RUNNING)
    try:
        await app.send_message(
            config.OWNER_ID,
            f"**🤖 ᴄʟᴏɴᴇs ʟᴏᴀᴅᴇᴅ ✅**\n\n"
            f"**• ᴀᴄᴛɪᴠᴇ ᴄʟᴏɴᴇs :** `{started}`",
        )
    except Exception:
        LOGGER.info("@%s: %s active clones loaded.", app.me.username, started)

    LOGGER.info("@%s: %s active clones loaded.", app.me.username, started)

    await idle()

    for bot_id in list(clone.RUNNING):
        await clone.stop_clone(bot_id)
    await app.stop()


if __name__ == "__main__":
    LOOP.run_until_complete(main())
    LOGGER.info("Stopping PurviReaction bot...")

# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Purvi-Reaction
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
