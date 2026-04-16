from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import AUTH_CHANNEL

async def get_fsub(bot, message):
    target_channel_id = AUTH_CHANNEL  
    user_id = message.from_user.id
    
    try:
        # Check if user is member of the channel
        await bot.get_chat_member(target_channel_id, user_id)
        return True  # User is already a member
        
    except UserNotParticipant:
        try:
            # Get channel invite link
            chat = await bot.get_chat(target_channel_id)
            channel_link = chat.invite_link or f"https://t.me/{chat.username}" if chat.username else None
            
            if not channel_link:
                # If no invite link, create one or use username
                channel_link = f"https://t.me/{chat.username}" if chat.username else "Channel invite link unavailable"
            
            join_button = InlineKeyboardButton("🔗 ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=channel_link)
            keyboard = [[join_button]]
            
            await message.reply(
                f"<b>🙌 Hey {message.from_user.mention()}!</b>\n\n"
                "<i>💡 Please join our channel first to unlock all features!</i>\n\n"
                "✅ After joining, use /start or /help again 🎉",
                reply_markup=InlineKeyboardMarkup(keyboard),
                quote=True  # Better UX
            )
            return False
            
        except Exception as e:
            # Fallback if can't get channel info
            await message.reply(
                "❌ Channel verification failed. Please contact admin.",
                quote=True
            )
            return False
