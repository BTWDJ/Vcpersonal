from pyrogram import Client
from pyrogram.types import Message
from helpers.command import commandpro
from config import call_py
from helpers.decorators import errors, sudo_users_only
from helpers.handlers import skip_current_song, skip_item
from helpers.queues import QUEUE, clear_queue


@Client.on_message(commandpro(["!skip", ".skip", "/skip", "/s", "S", "Skip"]))
@errors
@sudo_users_only
async def skip(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("**❌ ᴛʜᴇʀᴇ's ɴᴏᴛʜɪɴɢ ɪɴ ᴛʜᴇ ǫᴜᴇᴠᴇ ᴛᴏ sᴋɪᴘ**")
        elif op == 1:
            await m.reply("**ᴇᴍᴘᴛʏ ǫᴜᴇᴠᴇ ʟᴇᴀᴠɪɴɢ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ**")
        else:
            await m.reply(
                f"**⏩ sᴋɪᴘᴘᴇᴅ ᴘʟᴀʏʙᴀᴄᴋ** \n**🎶 ɴᴏᴡ ᴘʟᴀʏɪɴɢ** - [{op[0]}]({op[1]}) | `{op[2]}`",
                disable_web_page_preview=True,
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "**🗑️ ʀᴇᴍᴏᴠᴇᴅ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ sᴏɴɢ ғʀᴏᴍ ᴛʜᴇ ǫᴜᴇᴜᴇ: -**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#⃣{x}** - {hm}"
            await m.reply(OP)


@Client.on_message(commandpro(["!end", ".end", "/end", "!stop", ".stop", "/stop", "E", "End", "/e", "Stop"]))
@errors
@sudo_users_only
async def stop(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("**✅ ᴇɴᴅᴇᴅ ᴘʟᴀʏʙᴀᴄᴋ**")
        except Exception as e:
            await m.reply(f"**ᴇʀʀᴏʀ....** \n`{e}`")
    else:
        await m.reply("**❌ ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ**")


@Client.on_message(commandpro(["!pause", ".pause", "/pause", "pause"]))
@errors
@sudo_users_only
async def pause(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                f"**⏸ ᴘʟᴀʏʙᴀᴄᴋ ᴘᴀᴜsᴇᴅ**\n\nᴛᴏ ʀᴇsᴜᴍᴇ ᴘʟᴀʏʙᴀᴄᴋ ᴜsᴇ ᴛʜᴇ ᴄᴍᴅ » `!resume`"
            )
        except Exception as e:
            await m.reply(f"**ᴇʀʀᴏʀ.....** \n`{e}`")
    else:
        await m.reply("**❌ ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ**")


@Client.on_message(commandpro(["!resume", ".resume", "/resume", "resume"]))
@errors
@sudo_users_only
async def resume(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(
                f"**▶️ ᴘʟᴀʏʙᴀᴄᴋ ʀᴇsᴜᴍᴇᴅ**\n\nᴛᴏ ᴘᴀᴜsᴇ ᴘʟᴀʏʙᴀᴄᴋ ᴜsᴇ ᴛʜᴇ ᴄᴍᴅ » `!pause`"
            )
        except Exception as e:
            await m.reply(f"**ᴇʀʀᴏʀ....** \n`{e}`")
    else:
        await m.reply("**❌ ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ**")
