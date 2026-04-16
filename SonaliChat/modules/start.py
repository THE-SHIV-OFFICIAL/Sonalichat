import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait

from config import STICKER, FSUB, IMG, LOGGER_GROUP_ID, BOT_USERNAME
from SonaliChat import app
from SonaliChat.database import add_user, add_chat, get_fsub, chatsdb
from SonaliChat.modules.helpers import (
    STBUTTON, HELP_BACK, ABOUT_BUTTON, START, HELP_READ, HELP_ABOUT,
)

# ✅ FSub Check Handler
@app.on_message(filters.command(["start", "aistart"]) & ~filters.bot)
async def start(client, m: Message):
    # FSub Check
    if FSUB and not await get_fsub(client, m):
        return

    bot_name = (await client.get_me()).first_name

    if m.chat.type == ChatType.PRIVATE:
        user_id = m.from_user.id
        await add_user(user_id, m.from_user.username)

        # Sticker Animation
        if STICKER and isinstance(STICKER, list):
            try:
                sticker_to_send = random.choice(STICKER)
                umm = await m.reply_sticker(sticker=sticker_to_send)
                await asyncio.sleep(1)
                await umm.delete()
            except FloodWait as e:
                await asyncio.sleep(e.value)

        # Logger
        try:
            log_msg = (
                f"**✦ ɴᴇᴡ ᴜsᴇʀ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ**\n\n"
                f"**➻ ᴜsᴇʀ:** [{m.from_user.first_name or 'Unknown'}](tg://user?id={user_id})\n"
                f"**➻ ɪᴅ:** `{user_id}`\n"
                f"**➻ ᴜsᴇʀɴᴀᴍᴇ:** @{m.from_user.username or 'None'}"
            )
            await client.send_message(LOGGER_GROUP_ID, log_msg, disable_web_page_preview=True)
        except Exception:
            pass  # Logger fail ho to ignore

        # Loading Animation
        accha = await m.reply_text("**Loading....🥀**")
        await asyncio.sleep(1)
        await accha.edit("**ᴘɪɴɢ ᴘᴏɴɢ...🍫**")
        await asyncio.sleep(0.5)
        await accha.edit("**sᴛᴀʀᴛᴇᴅ.....😱**")
        await asyncio.sleep(0.5)
        await accha.delete()

        # Start Photo
        try:
            await m.reply_photo(
                photo=random.choice(IMG),
                caption=START,
                reply_markup=InlineKeyboardMarkup(STBUTTON),
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)

# ✅ Group Add Handler
@app.on_message(filters.new_chat_members)
async def on_new_chat_members(client: Client, message: Message):
    bot_id = (await client.get_me()).id
    if bot_id in [user.id for user in message.new_chat_members]:
        chat_id = message.chat.id
        chat_title = message.chat.title or "Unknown Group"
        added_by = message.from_user.mention if message.from_user else "Unknown"
        chatusername = f"@{message.chat.username}" if message.chat.username else "Private Group"

        # Add to DB
        await add_chat(chat_id, chat_title)

        # Generate Invite Link
        invite_link = "https://t.me/betabot_hub"
        try:
            invite_link = await client.export_chat_invite_link(chat_id)
        except Exception:
            pass

        # Welcome Message
        await message.reply_photo(
            photo=random.choice(IMG),
            caption=(
                f"**✦ ʜᴇʟʟᴏ {message.chat.title}!**\n\n"
                f"**ᴍᴇ ʀᴇᴀᴅʏ ᴛᴏ ᴡᴏʀᴋ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ!**\n\n"
                f"**🔥 ᴀᴅᴍɪɴ ʀᴇǫᴜɪʀᴇᴅ:**\n"
                f"• Delete Messages\n"
                f"• Manage Video Chats\n"
                f"• Pin Messages\n"
                f"• Invite Users"
            ),
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🔗 ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ", url=f"https://t.me/{BOT_USERNAME}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users"),
                    InlineKeyboardButton("📢 sᴜᴘᴘᴏʀᴛ", url="https://t.me/betabot_support")
                ]
            ])
        )

        # Logger Message
        try:
            log_msg = (
                f"<b>✦ ʙᴏᴛ #ᴀᴅᴅᴇᴅ ɪɴ ɢʀᴏᴜᴘ</b>\n\n"
                f"**⚘ ɢʀᴏᴜᴘ:** {chat_title}\n"
                f"**⚘ ɪᴅ:** `{chat_id}`\n"
                f"**⚘ ᴜsᴇʀɴᴀᴍᴇ:** {chatusername}\n"
                f"**⚘ ʟɪɴᴋ:** [ᴛᴀᴘ]({invite_link})\n"
                f"**⚘ ᴀᴅᴅᴇᴅ ʙʏ:** {added_by}"
            )
            await app.send_photo(
                LOGGER_GROUP_ID,
                photo=random.choice(IMG),
                caption=log_msg,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔗 ɢʀᴏᴜᴘ", url=invite_link)]])
            )
        except Exception:
            pass

# ✅ Group Remove Handler
@app.on_message(filters.left_chat_member)
async def on_left_chat_member(client: Client, message: Message):
    bot_id = (await client.get_me()).id
    if bot_id == message.left_chat_member.id:
        chat_id = message.chat.id
        chat_title = message.chat.title or "Unknown Group"
        removed_by = message.from_user.mention if message.from_user else "Unknown"

        # Remove from DB
        await chatsdb.delete_one({"chat_id": chat_id})

        # Logger Message
        try:
            left_msg = (
                f"<b>✦ ʙᴏᴛ #ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ɢʀᴏᴜᴘ</b>\n\n"
                f"**⚘ ɢʀᴏᴜᴘ:** {chat_title}\n"
                f"**⚘ ɪᴅ:** `{chat_id}`\n"
                f"**⚘ ʀᴇᴍᴏᴠᴇᴅ ʙʏ:** {removed_by}"
            )
            await app.send_photo(
                LOGGER_GROUP_ID,
                photo=random.choice(IMG),
                caption=left_msg,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📢 sᴜᴘᴘᴏʀᴛ", url="https://t.me/betabot_support")]])
            )
        except Exception:
            pass

# ✅ Help Command
@app.on_message(filters.command("help"))
async def help_command(client, message):
    await message.reply_photo(
        photo=random.choice(IMG),
        caption=HELP_READ,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔗 ᴀᴅᴅ ᴍᴇ", url=f"https://t.me/{BOT_USERNAME}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users"),
                InlineKeyboardButton("📢 sᴜᴘᴘᴏʀᴛ", url="https://t.me/betabot_support")
            ]
        ])
    )

# ✅ Callback Handlers
@app.on_callback_query(filters.regex('help'))
async def help_button(client, callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(
        HELP_READ,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="back"),
                InlineKeyboardButton("📢 sᴜᴘᴘᴏʀᴛ", url="https://t.me/betabot_support")
            ]
        ])
    )

@app.on_callback_query(filters.regex('back'))
async def back_to_menu(client, callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_photo(
        photo=random.choice(IMG),
        caption=START,
        reply_markup=InlineKeyboardMarkup(STBUTTON),
    )

@app.on_callback_query(filters.regex('ABOUT'))
async def about_section(client, callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(
        HELP_ABOUT,
        reply_markup=ABOUT_BUTTON
    )

@app.on_callback_query(filters.regex('HELP_BACK'))
async def help_back(client, callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_photo(
        photo=random.choice(IMG),
        caption=START,
        reply_markup=InlineKeyboardMarkup(STBUTTON)
    )
