from pyrogram.types import Message
import asyncio
import time
from pyrogram import filters, Client
from config import SUDO_USERS as SUDO_USER


@Client.on_message(filters.user(SUDO_USER) & filters.command(["delspam", "deletespam"], [".", "!", "/"]))
async def delspam(client: Client, message: Message):
    hero = await message.reply_text("😈 ᴜsᴀɢᴇ:\n !delspam 10 ᴅᴊ ᴏᴘ")
    quantity = message.command[1]
    spam_text = ' '.join(message.command[2:])
    quantity = int(quantity)
    await message.delete()
    for i in range(quantity):
        await hero.delete()
        msg = await client.send_message(message.chat.id, spam_text)
        await asyncio.sleep(1)
        await msg.delete()
        await asyncio.sleep(1)


@Client.on_message(filters.user(SUDO_USER) & filters.command(["spam", "spamming"], [".", "!", "/"]))
async def suspam(client: Client, message: Message):
    hero = await message.reply_text("😈 ᴜsᴀɢᴇ:\n !spam 10 ᴅᴊ ᴏᴘ")
    quantity = message.command[1]
    spam_text = ' '.join(message.command[2:])
    quantity = int(quantity)

    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id
        for _ in range(quantity):
            await client.send_message(message.chat.id, spam_text,
                                      reply_to_message_id=reply_to_id)
            await asyncio.sleep(0.01)
        return

    for _ in range(quantity):
        await hero.delete()
        await client.send_message(message.chat.id, spam_text)
        await asyncio.sleep(0.01)


@Client.on_message(filters.user(SUDO_USER) & filters.command(["fastspam", "fspam"], [".", "!", "/"]))
async def spspam(client: Client, message: Message):
    hero = await message.reply_text("😈 ᴜsᴀɢᴇ:\n !fspam 10 ᴅᴊ ᴏᴘ")
    quantity = message.command[1]
    spam_text = ' '.join(message.command[2:])
    quantity = int(quantity)
    
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id
        for _ in range(quantity):
            await client.send_message(message.chat.id, spam_text,
                                      reply_to_message_id=reply_to_id)
            await asyncio.sleep(0.001)
        return
    
    for _ in range(quantity):
        await hero.delete()
        await client.send_message(message.chat.id, spam_text)
        await asyncio.sleep(0.001)



@Client.on_message(filters.user(SUDO_USER) & filters.command(["slowspam", "dspam", "delayspam"], [".", "!", "/"]))
async def sperm(client: Client, message: Message):
    hero = await message.reply_text("⚡ ᴜsᴀɢᴇ:\n !slowspam 10 ᴅᴊ ᴏᴘ")
    quantity = message.command[1]
    spam_text = ' '.join(message.command[2:])
    quantity = int(quantity)

    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id
        for _ in range(quantity):
            await client.send_message(message.chat.id, spam_text,
                                      reply_to_message_id=reply_to_id)
            await asyncio.sleep(2)
        return

    for _ in range(quantity):
        await hero.delete()
        msg = await client.send_message(message.chat.id, spam_text)
        await asyncio.sleep(2)







@Client.on_message(filters.user(SUDO_USER) & filters.command(["sspam", "stkspam", "spamstk", "stickerspam"], [".", "!", "/"]))
async def pussy(client: Client, message: Message):
    if not message.reply_to_message:
       await message.edit_text(text="**ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ ᴡɪᴛʜ ᴀᴍᴏᴜɴᴛ ᴜ ᴡᴀɴᴛ ᴛᴏ sᴘᴀᴍ**")
     return
    if not message.reply_to_message.sticker:
        await message.edit_text(text="**ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ ᴡɪᴛʜ ᴀᴍᴍᴏᴜɴᴛ ᴜ ᴡᴀɴᴛ ᴛᴏ sᴘᴀᴍ**")
     return
    else:
        i=0
        times = message.command[1]
        if message.chat.type in ["supergroup", "group"]:
            for i in range(int(times)):
                sticker=message.reply_to_message.sticker.file_id
                await client.send_sticker(
                    message.chat.id,
                    sticker,
                )
                await asyncio.sleep(0.001)

        if message.chat.type == "private":
            for i in range(int(times)):
                sticker=message.reply_to_message.sticker.file_id
                await client.send_sticker(
                    message.chat.id, sticker
                )
                await asyncio.sleep(0.001)



@Client.on_message(filters.command('join', [".", "!", "/"]) & filters.user(SUDO_USER))
async def fuck(client: Client, message: Message):
    hero = message.text[6:]
    count = 0
    if not hero:
        return await message.reply_text("ɴᴇᴇᴅ ᴀ ᴄʜᴀᴛ ʟɪɴᴋ ᴏʀ ᴜsᴇʀɴᴀᴍᴇ ᴛᴏ ᴊᴏɪɴ.")
    if hero.isnumeric():
        return await message.reply_text("Can't join a chat with chat id. Give username or invite link.")
    try:
        await client.join_chat(hero)
        await message.reply_text(f"**ᴊᴏɪɴᴇᴅ ✅**")
    except Exception as ex:
        await message.reply_text(f"**ERROR:** \n\n{str(ex)}")


@Client.on_message(filters.command('leave', [".", "!", "/"]) & filters.user(SUDO_USER))
async def leftfuck(client: Client, message: Message):
    hero = message.text[6:]
    count = 0
    if not hero:
        return await message.reply_text("ɴᴇᴇᴅ ᴀ ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʟɪɴᴋ ᴛᴏ ʟᴇᴀᴠᴇ.")
    if hero.isnumeric():
        return await message.reply_text("Can't leave a chat with chat id. Give username or invite link.")
    try:
        await client.leave_chat(hero)
        await message.reply_text(f"**ʟᴇғᴛ ❌**")
    except Exception as ex:
        await message.reply_text(f"**ERROR:** \n\n{str(ex)}")
