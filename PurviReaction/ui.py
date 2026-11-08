# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder)

# 🚀 This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️

# 📩 DM for permission : @TheSigmaCoder
# =======================================================

from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineKeyboardButton as Button

from PurviReaction import app

START_PHOTO = "https://files.catbox.moe/8vbfvp.jpg"
CLONE_PHOTO = "https://files.catbox.moe/rdfi4z.jpg"

HELP_READ = """**• ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ғᴏʀ ᴍᴏʀᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ.  

♦ ɪғ ʏᴏᴜ'ʀᴇ ғᴀᴄɪɴɢ ᴀɴʏ ᴘʀᴏʙʟᴇᴍ ʏᴏᴜ ᴄᴀɴ ᴀsᴋ ɪɴ [sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ](https://t.me/PURVI_UPDATES).

» ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : /**
"""

TOOLS_DATA_READ = """**<u>❖ ᴄᴏᴍᴍᴀɴᴅs ғᴏʀ ʀᴇᴀᴄᴛɪᴏɴ :</u>

• /start sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ !
──────────────
• /stats - ɢᴇᴛ ʙᴏᴛ sᴛᴀᴛs, ᴜᴘᴛɪᴍᴇ ᴀɴᴅ ᴘɪɴɢ
──────────────
• /reaction on|off - ᴛᴜʀɴ ʀᴇᴀᴄᴛɪᴏɴs ᴏɴ/ᴏғғ ɪɴ ᴀ ɢʀᴏᴜᴘ (ɢʀᴏᴜᴘ ᴀᴅᴍɪɴs + ʙᴏᴛ ᴏᴡɴᴇʀ). ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs. ᴅᴍ & ᴄʜᴀɴɴᴇʟs ᴀʟᴡᴀʏs ʀᴇᴀᴄᴛ
──────────────
• /broadcast ᴛᴇxᴛ - sᴇɴᴅ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴀʟʟ ᴄʜᴀᴛs ᴀɴᴅ ᴜsᴇʀs, ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴡɪᴛʜ /broadcast ᴛᴏ ғᴏʀᴡᴀʀᴅ ɪᴛ ᴀs ɪᴛ ɪs (ʙᴏᴛ ᴏᴡɴᴇʀ ᴏɴʟʏ)
──────────────
✦ ᴘᴏᴡᴇʀᴇᴅ ʙʏ : [ᴘᴜʀᴠɪ ʙᴏᴛs](t.me/PURVI_BOTS)**
"""

ALPHA_READ = """**<u>❖ ᴄᴏᴍᴍᴀɴᴅs ғᴏʀ ᴄʟᴏɴᴇ ғᴇᴀᴛᴜʀᴇs :</u>

• /clone [ ʙᴏᴛ ᴛᴏᴋᴇɴ ] - ᴍᴀᴋᴇ ʏᴏᴜʀ ᴏᴡɴ ʙᴏᴛ.
──────────────
• /cloned - sᴇᴇ ᴄʟᴏɴᴇᴅ ʙᴏᴛs ᴏɴʟʏ ᴏᴡɴᴇʀ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.
──────────────
• /totalbots - ɢᴇᴛ ᴛᴏᴛᴀʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛs ᴄᴏᴜɴᴛ.
──────────────
• /delclone - ʀᴇᴍᴏᴠᴇ ʏᴏᴜʀ ʙᴏᴛ ᴄʟᴏɴᴇ.
──────────────
• /delallclone - ʀᴇᴍᴏᴠᴇ ᴀʟʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛs ᴏɴʟʏ ᴏᴡɴᴇʀ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.
──────────────
✦ ᴘᴏᴡᴇʀᴇᴅ ʙʏ : [ᴘᴜʀᴠɪ ʙᴏᴛs](t.me/PURVI_BOTS)**
"""


def start_caption(user):
    return (
        f"**✦ ʜᴇʏ {user.mention}!**\n**✦ ɪ'ᴍ ʏᴏᴜʀ ᴀᴜᴛᴏ ʀᴇᴀᴄᴛɪᴏɴ ʙᴏᴛ !!**\n\n"
        "**• ɪ'ᴍ ʀᴇᴀᴄᴛ ᴛᴏ ᴇᴠᴇʀʏ ᴍᴇssᴀɢᴇ ɪɴ ɢʀᴏᴜᴘs, ᴄʜᴀɴɴᴇʟs & ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛs ᴡɪᴛʜ ᴀ ʀᴀɴᴅᴏᴍ ᴇᴍᴏᴊɪ..!!**\n\n"
        "**✦ ᴘᴏᴡᴇʀᴇᴅ ʙʏ : [⎯᪵፝֟፝֟⎯꯭𓆩꯭ ᴀ ꯭ʟ ꯭ᴘ ꯭ʜ꯭ ᴧ꯭⎯꯭꯭‌꯭🥂꯭༎꯭ 𓆪](t.me/TheSigmaCoder)**"
    )


def clone_start_caption(user):
    return (
        f"**✦ ʜᴇʏ {user.mention}!!**\n**◆ ɪ'ᴍ ʏᴏᴜʀ ᴄʟᴏɴᴇᴅ ᴀᴜᴛᴏ ʀᴇᴀᴄᴛɪᴏɴ ʙᴏᴛ !!**\n\n"
        "**• ɪ'ᴍ ʀᴇᴀᴄᴛ ᴛᴏ ᴇᴠᴇʀʏ ᴍᴇssᴀɢᴇ ɪɴ ɢʀᴏᴜᴘs, ᴄʜᴀɴɴᴇʟs & ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛs ᴡɪᴛʜ ᴀ ʀᴀɴᴅᴏᴍ ᴇᴍᴏᴊɪ..!!**\n\n"
        f"**◆ ɢᴏ & ᴄʟᴏɴᴇ ʏᴏᴜʀ ᴏᴡɴ ʙᴏᴛ :\n     @{app.me.username}**"
    )


def clone_info_caption():
    return (
        "**✦ ᴡᴀɴᴛ ʏᴏᴜʀ ᴏᴡɴ ʀᴇᴀᴄᴛɪᴏɴ ʙᴏᴛ ?**\n\n"
        "**• ɢᴏ ᴛᴏ ᴛʜᴇ ᴍᴀɪɴ ʙᴏᴛ & sᴇɴᴅ /clone ᴡɪᴛʜ ʏᴏᴜʀ ʙᴏᴛ ᴛᴏᴋᴇɴ.**\n\n"
        f"**◆ ᴍᴀɪɴ ʙᴏᴛ : @{app.me.username}**"
    )


def clone_info_buttons():
    return InlineKeyboardMarkup([
        [Button("ᴄʟᴏɴᴇ ʙᴏᴛ", url=f"https://t.me/{app.me.username}")]
    ])


def add_button(client):
    return [
        [
            Button(
                "✙ ᴀᴅᴅ ᴍᴇ ɪɴ ɢʀᴏᴜᴘ ✙",
                url=f"http://t.me/{client.me.username}?startgroup=true"
            )
        ],
        [
            Button(
                "✙ ᴀᴅᴅ ᴍᴇ ɪɴ ᴄʜᴀɴɴᴇʟ ✙",
                url=f"https://t.me/{client.me.username}?startchannel=new&admin=post_messages+invite_users"
            )
        ]
    ]


def start_buttons(client):
    return InlineKeyboardMarkup(
        add_button(client) + [
            [
                Button("sᴜᴘᴘᴏʀᴛ", url="https://t.me/PURVI_BOTS"),
                Button("sᴏᴜʀᴄᴇ", url="https://github.com/Im-NotCoder/Purvi-Reaction"),
            ],
            [Button("⌯ ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs ⌯", callback_data="HELP")],
        ]
    )


def clone_start_buttons(client):
    return InlineKeyboardMarkup(add_button(client))


def help_buttons():
    return InlineKeyboardMarkup([
        [
            Button("ᴄʟᴏɴᴇ", callback_data="ALPHA_CMD"),
            Button("ʀᴇᴀᴄᴛɪᴏɴ", callback_data="TOOLS_DATA"),
        ],
        [Button("ʙᴀᴄᴋ", callback_data="BACK")],
    ])


def back_buttons():
    return InlineKeyboardMarkup([[
        Button("ʙᴀᴄᴋ", callback_data="ALPHA_BACK"),
        Button("ᴄʟᴏsᴇ", callback_data="CLOSE"),
    ]])

# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎
# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Purvi-Reaction
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
