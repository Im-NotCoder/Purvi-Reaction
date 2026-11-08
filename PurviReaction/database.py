# =======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @TheSigmaCoder
# =======================================================

import time
from motor.motor_asyncio import AsyncIOMotorClient
import config

if not config.MONGO_URL:
    raise SystemExit("MONGO_URL is not set.")

_db = AsyncIOMotorClient(config.MONGO_URL)[config.DB_NAME]

clones = _db.clonebotdb
chats = _db.served_chats
users = _db.served_users
settings = _db.reaction_off_groups

_known_chats = set()
_known_users = set()
_off = {}  

async def setup():
    await chats.create_index([("bot_id", 1), ("chat_id", 1)], unique=True)
    await users.create_index([("bot_id", 1), ("user_id", 1)], unique=True)
    await settings.create_index([("bot_id", 1), ("chat_id", 1)], unique=True)


async def add_chat(bot_id, chat_id):
    if (bot_id, chat_id) in _known_chats:
        return
    await chats.update_one(
        {"bot_id": bot_id, "chat_id": chat_id},
        {"$setOnInsert": {"added_at": int(time.time())}},
        upsert=True,
    )
    _known_chats.add((bot_id, chat_id))


async def remove_chat(bot_id, chat_id):
    _known_chats.discard((bot_id, chat_id))
    await chats.delete_one({"bot_id": bot_id, "chat_id": chat_id})


async def add_user(bot_id, user_id):
    if (bot_id, user_id) in _known_users:
        return
    await users.update_one(
        {"bot_id": bot_id, "user_id": user_id},
        {"$setOnInsert": {"added_at": int(time.time())}},
        upsert=True,
    )
    _known_users.add((bot_id, user_id))


async def remove_user(bot_id, user_id):
    _known_users.discard((bot_id, user_id))
    await users.delete_one({"bot_id": bot_id, "user_id": user_id})


async def get_chats(bot_id):
    return [d["chat_id"] async for d in chats.find({"bot_id": bot_id})]


async def get_users(bot_id):
    return [d["user_id"] async for d in users.find({"bot_id": bot_id})]


async def count_chats(bot_id):
    return await chats.count_documents({"bot_id": bot_id})


async def count_users(bot_id):
    return await users.count_documents({"bot_id": bot_id})


async def get_clones():
    return await clones.find().to_list(length=None)


async def get_clone(bot_id):
    return await clones.find_one({"bot_id": bot_id})


async def get_clone_by_token(token):
    return await clones.find_one({"token": token})


async def add_clone(details):
    await clones.update_one(
        {"bot_id": details["bot_id"]}, {"$set": details}, upsert=True
    )


async def delete_clone(bot_id):
    await clones.delete_many({"bot_id": bot_id})
    for col in (chats, users, settings):
        await col.delete_many({"bot_id": bot_id})
    _known_chats.difference_update({k for k in _known_chats if k[0] == bot_id})
    _known_users.difference_update({k for k in _known_users if k[0] == bot_id})
    _off.pop(bot_id, None)


async def delete_all_clones():
    for clone in await get_clones():
        await delete_clone(clone["bot_id"])


async def _disabled(bot_id):
    if bot_id not in _off:
        _off[bot_id] = {d["chat_id"] async for d in settings.find({"bot_id": bot_id})}
    return _off[bot_id]


async def reaction_enabled(bot_id, chat_id):
    return chat_id not in await _disabled(bot_id)


async def set_reaction(bot_id, chat_id, enabled):
    off = await _disabled(bot_id)
    key = {"bot_id": bot_id, "chat_id": chat_id}
    if enabled:
        off.discard(chat_id)
        await settings.delete_one(key)
    else:
        off.add(chat_id)
        await settings.update_one(key, {"$setOnInsert": {"off_at": int(time.time())}}, upsert=True)

# ======================================================
# ©️ 2025-26 All Rights Reserved by Purvi Bots (Im-Notcoder) 😎

# 🧑‍💻 Developer : t.me/TheSigmaCoder
# 🔗 Source link : GitHub.com/Im-Notcoder/Purvi-Reaction
# 📢 Telegram channel : t.me/Purvi_Bots
# =======================================================
