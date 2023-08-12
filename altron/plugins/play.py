import asyncio
import random
from helpers.command import commandpro
from helpers.handlers import bash
from helpers.decorators import errors, sudo_users_only
from pyrogram.types import Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio
from youtubesearchpython import VideosSearch
from config import client, call_py
from helpers.queues import QUEUE, add_to_queue, get_queue


# music player
def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            if len(r["title"]) > 34:
                songname = r["title"][:35] + "..."
            else:
                songname = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
            duration=r["duration"]
        return [songname, url,duration]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link: str):
    stdout, stderr = await bash(
        f'yt-dlp -g -f "best[height<=?720][width<=?1280]" {link}'
    )
    if stdout:
        return 1, stdout
    return 0, stderr


@client.on_message(commandpro(["!play", "/p", "!p", "$p", "/play", "P", "Play"]))
@errors
@sudo_users_only
async def play(client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    m.chat.title
    if replied:
        if replied.audio or replied.voice:
            await m.delete()
            huehue = await replied.reply("**🔄 ᴘʀᴏᴄᴇssɪɴɢ...**")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:35] + "..."
                else:
                    songname = replied.audio.file_name[:35] + "..."
            elif replied.voice:
                songname = "Voice Note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_text(f"""
**⃣ 𝑺𝒐𝒏𝒈 𝒊𝒏 𝒒𝒖𝒆𝒖𝒆 𝒕𝒐 {pos}
🖤 ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ: {m.from_user.mention}**
""",
                )
            else:
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(
                        dl,
                        HighQualityAudio(),
                    ),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_text(f"""
**▶ sᴛᴀʀᴛᴇᴅ ᴘʟᴀʏɪɴɢ sᴏɴɢ
🖤 ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ: {m.from_user.mention}
  sᴏɴɢ ɴᴀᴍᴇ:  {songname}
  **
""",
                )

    else:
        if len(m.command) < 2:
            await m.reply("💫 ʀᴇᴘʟʏ ᴛᴏ ᴀɴ ᴀᴜᴅɪᴏ ғɪʟᴇ ᴏʀ ᴘʀᴏᴠɪᴅᴇ ᴍᴇ ᴛᴏ sᴇᴀʀᴄʜ")
        else:
            await m.delete()
            huehue = await m.reply("🔎 sᴇᴀʀᴄʜɪɴɢ...")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await huehue.edit("`❌ ɴᴏᴛʜɪɴɢ ғᴏᴜɴᴅ`")
            else:
                songname = search[0]
                url = search[1]
                hm, ytlink = await ytdl(url)
                if hm == 0:
                    await huehue.edit(f"**𝒀𝑻𝑫𝑳 𝑬𝒓𝒓𝒐𝒓... ⚠️** \n\n`{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await huehue.delete()
                        # await m.reply_to_message.delete()
                        m.reply_text(f"""
**⃣ 𝑨𝒅𝒅𝒆𝒅 𝒊𝒏 𝒒𝒖𝒆𝒖𝒆 𝒂𝒕 {pos}
🖤 ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ: {m.from_user.mention}**
sᴏɴɢ ɴᴀᴍᴇ:  {songname}""",
                        )
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                    HighQualityAudio(),
                                ),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await huehue.delete()
                            # await m.reply_to_message.delete()
                            await m.reply_text(f"""
**▶ sᴛᴀʀᴛᴇᴅ ᴘʟᴀʏɪɴɢ sᴏɴɢ
🖤 ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ: {m.from_user.mention}**
sᴏɴɢ ɴᴀᴍᴇ:  {songname}""",
                            )
                        except Exception as ep:
                            await huehue.edit(f"`{ep}`")



@client.on_message(commandpro(["/pf", "!playfrom", "/playfrom", "PF", "!pf"]))
@errors
@sudo_users_only
async def playfrom(client, m: Message):
    chat_id = m.chat.id
    if len(m.command) < 2:
        await m.reply(
            f"**USE:** \n`!playfrom [chat_id/group_username]`"
        )
    else:
        args = m.text.split(maxsplit=1)[1]
        if ";" in args:
            chat = args.split(";")[0]
            limit = int(args.split(";")[1])
        else:
            chat = args
            limit = 10
            lmt = 9
        await m.delete()
        hmm = await m.reply(f"**🔎 𝑭𝒆𝒕𝒄𝒉𝒊𝒏𝒈 {limit} 𝒓𝒂𝒏𝒅𝒐𝒎 𝒔𝒐𝒏𝒈𝒔 𝒇𝒓𝒐𝒎 {chat}**")
        try:
            async for x in client.search_messages(chat, limit=limit, filter="audio"):
                location = await x.download()
                if x.audio.title:
                    songname = x.audio.title[:30] + "..."
                else:
                    songname = x.audio.file_name[:30] + "..."
                link = x.link
                if chat_id in QUEUE:
                    add_to_queue(chat_id, songname, location, link, "Audio", 0)
                else:
                    await call_py.join_group_call(
                        chat_id,
                        AudioPiped(location, HighQualityAudio()),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, songname, location, link, "Audio", 0)
                    # await m.reply_to_message.delete()
                    await m.reply_text(f"""
**▶ sᴛᴀʀᴛᴇᴅ ᴘʟᴀʏɪɴɢ sᴏɴɢ ғʀᴏᴍ: {chat}
🖤 ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ: {m.from_user.mention}**
""",
                    )
            await hmm.delete()
            await m.reply(
                f"➕ ᴀᴅᴅɪɴɢ {lmt} sᴏɴɢs ɪɴᴛᴏ ǫᴜᴇᴠᴇ\nᴄʟɪᴄᴋ `!playlist` ᴛᴏ ᴠɪᴇᴡ ᴘʟᴀʏʟɪsᴛ**"
            )
        except Exception as e:
            await hmm.edit(f"**ᴇʀʀᴏʀ....** \n`{e}`")


@client.on_message(commandpro(["/pl", "/playlist", "!playlist", "!pl", "pl", "/queue"]))
@errors
@sudo_users_only
async def playlist(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await m.delete()
            await m.reply(
                f"**🎵 ɴᴏᴡ ᴘʟᴀʏɪɴɢ:** \n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}`",
                disable_web_page_preview=True,
            )
        else:
            QUE = f"**🎵 ɴᴏᴡ ᴘʟᴀʏɪɴɢ:** \n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}` \n\n**⏯️ 𝑸𝒖𝒆𝒖𝒆 𝑳𝒊𝒔𝒕**"
            l = len(chat_queue)
            for x in range(1, l):
                hmm = chat_queue[x][0]
                hmmm = chat_queue[x][2]
                hmmmm = chat_queue[x][3]
                QUE = QUE + "\n" + f"**#{x}** - [{hmm}]({hmmm}) | `{hmmmm}`\n"
            await m.reply(QUE, disable_web_page_preview=True)
    else:
        await m.reply("**❌ ᴅᴏᴇsɴ'ᴛ ᴘʟᴀʏ ᴀɴʏᴛʜɪɴɢ**")
