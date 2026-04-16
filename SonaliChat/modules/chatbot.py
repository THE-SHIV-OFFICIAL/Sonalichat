from SonaliChat.database.sonali import chatbot_api
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ChatMemberUpdated
from pyrogram.enums import ChatAction, ChatMemberStatus
from SonaliChat import app
from SonaliChat.database import (
    is_chatbot_enabled,
    enable_chatbot,
    disable_chatbot,
    chatbot_api,
    is_admins
)

# GROUP CHAT FILTER
async def text_filter(_, __, m: Message):
    return (
        bool(m.text)
        and len(m.text) <= 69
        and not m.text.startswith(("!", "/"))
        and (not m.reply_to_message or m.reply_to_message.from_user.id == m._client.me.id)
        and not (m.mentioned and (m.text.startswith("!") or m.text.startswith("/")))
    )

chatbot_filter = filters.create(text_filter)

# GROUP CHATBOT HANDLER
@app.on_message(
    (
        filters.text & filters.group & chatbot_filter
        & ~filters.regex(r"^[/!]")
    )
    & ~filters.bot
    & ~filters.sticker
)
async def chatbot(_, message: Message):
    chat_id = message.chat.id

    if not await is_chatbot_enabled(chat_id):
        return

    await app.send_chat_action(chat_id, ChatAction.TYPING)
    reply = chatbot_api.ask_question(message.text)
    await message.reply_text(reply or "❖ ᴄʜᴀᴛʙᴏᴛ ᴇʀʀᴏʀ. ᴄᴏɴᴛᴀᴄᴛ @betabot_support.")

# PRIVATE CHATBOT HANDLER
@app.on_message(filters.private & filters.text & ~filters.bot & ~filters.regex(r"^[/!]"))
async def chatbot_pm(_, message: Message):
    await app.send_chat_action(message.chat.id, ChatAction.TYPING)
    reply = chatbot_api.ask_question(message.text)
    await message.reply_text(reply or "❖ ᴄʜᴀᴛʙᴏᴛ ᴇʀʀᴏʀ. ᴄᴏɴᴛᴀᴄᴛ betabot_support.")

# /chatbot COMMAND WITH BUTTONS
@app.on_message(filters.command("chatbot") & filters.group & ~filters.bot)
@is_admins
async def chatbot_toggle(_, message: Message):
    chat_id = message.chat.id
    chat_title = message.chat.title

    status = await is_chatbot_enabled(chat_id)
    status_text = "ᴇɴᴀʙʟᴇᴅ" if status else "ᴅɪꜱᴀʙʟᴇᴅ"

    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("ᴇɴᴀʙʟᴇ", callback_data="chatbot_enable"),
            InlineKeyboardButton("ᴅɪꜱᴀʙʟᴇ", callback_data="chatbot_disable")
        ]]
    )

    await message.reply_text(
        f"❖ ᴄᴜʀʀᴇɴᴛʟʏ ᴄʜᴀᴛʙᴏᴛ ɪꜱ **{status_text}** ɪɴ **{chat_title}**.",
        reply_markup=keyboard
    )

# CALLBACK BUTTON HANDLER
@app.on_callback_query(filters.regex("chatbot_"))
@is_admins
async def chatbot_button_toggle(_, query):
    chat_id = query.message.chat.id
    user = query.from_user

    if query.data == "chatbot_enable":
        if await is_chatbot_enabled(chat_id):
            await query.answer("ᴄʜᴀᴛʙᴏᴛ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ.", show_alert=True)
            return
        await enable_chatbot(chat_id)
        await query.message.edit_text(
            f"❖ ᴄʜᴀᴛʙᴏᴛ ʜᴀꜱ ʙᴇᴇɴ **ᴇɴᴀʙʟᴇᴅ** ʙʏ {user.mention}."
        )
        await query.answer("ᴄʜᴀᴛʙᴏᴛ ᴇɴᴀʙʟᴇᴅ !!")

    elif query.data == "chatbot_disable":
        if not await is_chatbot_enabled(chat_id):
            await query.answer("ᴄʜᴀᴛʙᴏᴛ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴅɪꜱᴀʙʟᴇᴅ.", show_alert=True)
            return
        await disable_chatbot(chat_id)
        await query.message.edit_text(
            f"❖ ᴄʜᴀᴛʙᴏᴛ ʜᴀꜱ ʙᴇᴇɴ **ᴅɪꜱᴀʙʟᴇᴅ** ʙʏ {user.mention}."
        )
        await query.answer("ᴄʜᴀᴛʙᴏᴛ ᴅɪꜱᴀʙʟᴇᴅ !!")

# Before sending message
async def chat_handler(client, message):
    user_msg = message.text or message.caption or ""
    
    if not user_msg:
        return  # Skip empty messages
    
    # Get AI response
    ai_reply = await chatbot_api.ask_question(user_msg)
    
    # ✅ FINAL SAFETY CHECK
    if not ai_reply or len(ai_reply.strip()) < 2:
        ai_reply = "Hii babu! Kya baat karna chahte ho? 💕"
    
    # Send with error handling
    try:
        await message.reply_text(ai_reply)
    except Exception as e:
        print(f"Send Error: {e}")
        await message.reply_text("Message send nahi hua! Try again 💖")
