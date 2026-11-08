# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

import config
from PurviReaction import database as db

async def is_bot_owner(bot_id, user_id):
    if user_id == config.OWNER_ID:
        return True
    clone = await db.get_clone(bot_id)
    return bool(clone and clone.get("user_id") == user_id)

def readable_time(seconds):
    days, rest = divmod(int(seconds), 86400)
    hours, rest = divmod(rest, 3600)
    minutes, secs = divmod(rest, 60)
    text = f"{hours}h {minutes}m {secs}s"
    return f"{days}d {text}" if days else text

def chunk_lines(header, lines, limit=4000):
    text = header
    for line in lines:
        if len(text) + len(line) + 1 > limit:
            yield text
            text = ""
        text += line + "\n"
    if text.strip():
        yield text

# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Purvi-Reaction
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
