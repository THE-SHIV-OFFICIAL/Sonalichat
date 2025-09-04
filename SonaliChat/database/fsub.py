from pyrogram.errors import UserNotParticipant, ChannelInvalid
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import AUTH_CHANNEL


async def get_fsub(bot, message):
    target_channel_id = AUTH_CHANNEL  # Yeh config.py se aa raha hai
    user_id = message.from_user.id

    try:
        # User channel 
        await bot.get_chat_member(target_channel_id, user_id)
        return True

    except UserNotParticipant:
    
        try:
            channel = await bot.get_chat(target_channel_id)
            
            channel_link = channel.invite_link or f"https://t.me/{channel.username}"
        except Exception as e:
            print(f"⚠️ Error fetching channel info: {e}")
            return False

        join_button = InlineKeyboardButton("ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=channel_link)
        keyboard = [[join_button]]

        await message.reply(
            f"<b>🙌 Hey {message.from_user.mention()}, You're Almost There.</b>\n\n"
            "<i>💡 Unlock the magic by joining our channel! Don't miss out on the fun and learning 🎉</i>",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return False

    except ChannelInvalid:
        # Agar AUTH_CHANNEL galat hai
        print(f"⚠️ Invalid AUTH_CHANNEL in config: {target_channel_id}")
        return False
